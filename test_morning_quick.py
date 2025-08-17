#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pytz
import requests
import feedparser
import time

# === CONFIGURAZIONE TELEGRAM ===
TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
TELEGRAM_CHAT_ID = "@abkllr"

def invia_messaggio_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    clean_msg = msg.replace('**', '*')
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": clean_msg,
        "parse_mode": "Markdown"
    }
    
    try:
        r = requests.post(url, data=payload, timeout=10)
        success = r.status_code == 200
        print(f"📤 [TELEGRAM] Messaggio {len(msg)} caratteri: {'✅' if success else '❌'}")
        return success
    except Exception as e:
        print(f"❌ [TELEGRAM] Errore: {e}")
        return False

def test_morning_news():
    print("🌅 [TEST-MORNING] Avvio test Morning News (6 messaggi)...")
    print("=" * 60)
    
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    success_count = 0
    
    # MESSAGGIO 1: FINANZA
    msg1_parts = []
    msg1_parts.append("💰 *MORNING NEWS - FINANZA*")
    msg1_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 1/6")
    msg1_parts.append("─" * 35)
    msg1_parts.append("")
    msg1_parts.append("📊 **1.** *Fed maintains hawkish stance on inflation targets*")
    msg1_parts.append("📰 Reuters")
    msg1_parts.append("🔗 https://reuters.com/fed-hawkish...")
    msg1_parts.append("")
    msg1_parts.append("📊 **2.** *Wall Street futures point to mixed open*")
    msg1_parts.append("📰 MarketWatch")
    msg1_parts.append("🔗 https://marketwatch.com/futures...")
    msg1_parts.append("")
    msg1_parts.append("📊 **3.** *European banks rally on rate expectations*")
    msg1_parts.append("📰 Bloomberg")
    msg1_parts.append("🔗 https://bloomberg.com/banks-rally...")
    msg1_parts.append("")
    msg1_parts.append("─" * 35)
    msg1_parts.append("🤖 555 Lite • Finanza (3 notizie)")
    
    msg1 = "\n".join(msg1_parts)
    if invia_messaggio_telegram(msg1):
        success_count += 1
        print("✅ [TEST] Messaggio 1 (Finanza) inviato")
    time.sleep(2)
    
    # MESSAGGIO 2: CRIPTOVALUTE
    msg2_parts = []
    msg2_parts.append("₿ *MORNING NEWS - CRIPTOVALUTE*")
    msg2_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 2/6")
    msg2_parts.append("─" * 35)
    msg2_parts.append("")
    msg2_parts.append("📊 **1.** *Bitcoin consolidates above $42,000 support level*")
    msg2_parts.append("📰 CoinDesk")
    msg2_parts.append("🔗 https://coindesk.com/bitcoin-42k...")
    msg2_parts.append("")
    msg2_parts.append("📊 **2.** *Ethereum shows strength ahead of major upgrade*")
    msg2_parts.append("📰 CoinTelegraph")
    msg2_parts.append("🔗 https://cointelegraph.com/ethereum...")
    msg2_parts.append("")
    msg2_parts.append("📊 **3.** *Altcoins mixed as market seeks direction*")
    msg2_parts.append("📰 CryptoSlate")
    msg2_parts.append("🔗 https://cryptoslate.com/altcoins...")
    msg2_parts.append("")
    msg2_parts.append("─" * 35)
    msg2_parts.append("🤖 555 Lite • Criptovalute (3 notizie)")
    
    msg2 = "\n".join(msg2_parts)
    if invia_messaggio_telegram(msg2):
        success_count += 1
        print("✅ [TEST] Messaggio 2 (Crypto) inviato")
    time.sleep(2)
    
    # MESSAGGIO 3: GEOPOLITICA
    msg3_parts = []
    msg3_parts.append("🌍 *MORNING NEWS - GEOPOLITICA*")
    msg3_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 3/6")
    msg3_parts.append("─" * 35)
    msg3_parts.append("")
    msg3_parts.append("📊 **1.** *Global trade tensions ease as talks resume*")
    msg3_parts.append("📰 BBC World")
    msg3_parts.append("🔗 https://bbc.com/trade-tensions...")
    msg3_parts.append("")
    msg3_parts.append("📊 **2.** *European Union discusses new sanctions package*")
    msg3_parts.append("📰 Al Jazeera")
    msg3_parts.append("🔗 https://aljazeera.com/eu-sanctions...")
    msg3_parts.append("")
    msg3_parts.append("📊 **3.** *Oil markets watch Middle East developments*")
    msg3_parts.append("📰 Reuters World")
    msg3_parts.append("🔗 https://reuters.com/oil-markets...")
    msg3_parts.append("")
    msg3_parts.append("─" * 35)
    msg3_parts.append("🤖 555 Lite • Geopolitica (3 notizie)")
    
    msg3 = "\n".join(msg3_parts)
    if invia_messaggio_telegram(msg3):
        success_count += 1
        print("✅ [TEST] Messaggio 3 (Geopolitica) inviato")
    time.sleep(2)
    
    # MESSAGGIO 4: MERCATI EMERGENTI
    msg4_parts = []
    msg4_parts.append("🌟 *MORNING NEWS - MERCATI EMERGENTI*")
    msg4_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 4/6")
    msg4_parts.append("─" * 35)
    msg4_parts.append("")
    msg4_parts.append("📊 **1.** *Asian markets show mixed performance*")
    msg4_parts.append("📰 Nikkei Asia")
    msg4_parts.append("🔗 https://asia.nikkei.com/markets...")
    msg4_parts.append("")
    msg4_parts.append("📊 **2.** *Chinese manufacturing data beats expectations*")
    msg4_parts.append("📰 SCMP")
    msg4_parts.append("🔗 https://scmp.com/china-manufacturing...")
    msg4_parts.append("")
    msg4_parts.append("📊 **3.** *Latin American currencies gain against dollar*")
    msg4_parts.append("📰 Financial Times")
    msg4_parts.append("🔗 https://ft.com/latam-currencies...")
    msg4_parts.append("")
    msg4_parts.append("─" * 35)
    msg4_parts.append("🤖 555 Lite • Mercati Emergenti (3 notizie)")
    
    msg4 = "\n".join(msg4_parts)
    if invia_messaggio_telegram(msg4):
        success_count += 1
        print("✅ [TEST] Messaggio 4 (Mercati Emergenti) inviato")
    time.sleep(2)
    
    # MESSAGGIO 5: ANALISI ML
    msg5_parts = []
    msg5_parts.append("🧠 *MORNING NEWS - ANALISI ML*")
    msg5_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 5/6")
    msg5_parts.append("─" * 35)
    msg5_parts.append("")
    msg5_parts.append("📰 *RASSEGNA STAMPA ML*")
    msg5_parts.append("🟢 *Sentiment*: POSITIVE")
    msg5_parts.append("⚡ *Impatto Mercati*: MEDIUM")
    msg5_parts.append("")
    msg5_parts.append("💡 *RACCOMANDAZIONI OPERATIVE:*")
    msg5_parts.append("• 📈 **Finanza**: Fed policy supportive for banks")
    msg5_parts.append("• ₿ **Crypto**: BTC breakout watch above 44k")
    msg5_parts.append("• 🌍 **Geopolitica**: Risk-on sentiment improving")
    msg5_parts.append("")
    msg5_parts.append("🚨 *TOP 3 ALERT CRITICI GIORNATA:*")
    msg5_parts.append("⚠️ **1.** *Fed hawkish stance impacts bond yields*")
    msg5_parts.append("📂 Finanza • Impact: MEDIUM")
    msg5_parts.append("")
    msg5_parts.append("⚠️ **2.** *Bitcoin consolidation at key support*")
    msg5_parts.append("📂 Criptovalute • Impact: MEDIUM")
    msg5_parts.append("")
    msg5_parts.append("─" * 35)
    msg5_parts.append("🤖 555 Lite • Analisi ML & Alert Critici")
    
    msg5 = "\n".join(msg5_parts)
    if invia_messaggio_telegram(msg5):
        success_count += 1
        print("✅ [TEST] Messaggio 5 (ML) inviato")
    time.sleep(2)
    
    # MESSAGGIO 6: CALENDARIO E OUTLOOK
    msg6_parts = []
    msg6_parts.append("📅 *MORNING NEWS - CALENDARIO & ML OUTLOOK*")
    msg6_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 6/6")
    msg6_parts.append("─" * 35)
    msg6_parts.append("")
    msg6_parts.append("🧠 *RACCOMANDAZIONI ML CALENDARIO*")
    msg6_parts.append("")
    msg6_parts.append("💡 *TOP 5 STRATEGIE OGGI:*")
    msg6_parts.append("1. 📈 Monitor Fed policy impact on rates")
    msg6_parts.append("2. ₿ Crypto range trading 42-44k BTC")
    msg6_parts.append("3. 🌍 Watch geopolitical risk-on signals")
    msg6_parts.append("4. 🏦 Banks sector momentum on rate expectations")
    msg6_parts.append("5. 🌏 EM currencies strength vs USD")
    msg6_parts.append("")
    msg6_parts.append("🔮 *OUTLOOK MERCATI OGGI*")
    msg6_parts.append("• 🇺🇸 Wall Street: Apertura 15:30 CET - Watch tech earnings")
    msg6_parts.append("• 🇪🇺 Europa: Chiusura 17:30 CET - Banks & Energy focus")
    msg6_parts.append("• ₿ Crypto: 24/7 - BTC key levels 42k-45k")
    msg6_parts.append("• 🌍 Forex: London-NY overlap 14:00-17:00 CET")
    msg6_parts.append("")
    msg6_parts.append("✅ *RASSEGNA STAMPA COMPLETATA*")
    msg6_parts.append("📊 12 notizie analizzate")
    msg6_parts.append("🌍 4 categorie coperte")
    msg6_parts.append("🧠 5 raccomandazioni ML")
    msg6_parts.append("")
    msg6_parts.append("🔮 *PROSSIMI AGGIORNAMENTI:*")
    msg6_parts.append("• 🍽️ Daily Report: 14:10")
    msg6_parts.append("• 🌆 Evening Report: 20:10")
    msg6_parts.append("• 📊 Weekly Report: Domenica 19:00")
    msg6_parts.append("")
    msg6_parts.append("─" * 35)
    msg6_parts.append("🤖 555 Lite • Morning Briefing + ML Outlook")
    
    msg6 = "\n".join(msg6_parts)
    if invia_messaggio_telegram(msg6):
        success_count += 1
        print("✅ [TEST] Messaggio 6 (finale) inviato")
    
    print("=" * 60)
    print(f"📊 [TEST-MORNING] Risultato finale: {success_count}/6 messaggi inviati")
    print("🌅 [TEST-MORNING] Test Morning News completato!")
    
    return success_count

if __name__ == "__main__":
    test_morning_news()
