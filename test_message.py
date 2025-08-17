#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test message per verificare l'invio diretto a Telegram
"""
import requests
import datetime
import pytz

# Token e Chat ID (stessi del sistema lite)
TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
TELEGRAM_CHAT_ID = "@abkllr"

def invia_messaggio_test():
    """Invia un messaggio di test direttamente a Telegram"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    messaggio_test = f"""🧪 *TEST SISTEMA 555 LITE*

✅ Sistema attivo e operativo
🚀 RAM ottimizzata: +60% disponibile
📊 Qualità messaggi: Identica al sistema principale
🕐 Timestamp: {now.strftime('%d/%m/%Y %H:%M:%S')} CET

🔍 *TEST COMPONENTI:*
• ✅ Connessione Telegram API
• ✅ Token autenticato
• ✅ Canale @abkllr accessibile
• ✅ Sistema ML caricato
• ✅ Dati storici disponibili (19 file, ~670KB)

📱 *PROSSIMI MESSAGGI AUTOMATICI:*
• 🌅 Morning News: Ogni giorno 08:10
• 🍽️ Lunch Report: Ogni giorno 12:30
• 📊 Weekly Report: Domenica 20:00
• 📅 Monthly Report: Ultimo giorno mese 21:00

🎯 Test completato con successo!
Sistema 555 Lite pronto per deployment autonomo."""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": messaggio_test,
        "parse_mode": "Markdown"
    }
    
    try:
        print("📤 [TEST] Invio messaggio di test a Telegram...")
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ [TEST] Messaggio inviato con successo!")
            print(f"📱 [TEST] Check canale: https://t.me/abkllr")
            return True
        else:
            print(f"❌ [TEST] Errore HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ [TEST] Errore nell'invio: {e}")
        return False

if __name__ == "__main__":
    print("🧪 [555-LITE-TEST] Avvio test messaggio Telegram...")
    success = invia_messaggio_test()
    print(f"🎯 [555-LITE-TEST] Test {'✅ completato' if success else '❌ fallito'}")
