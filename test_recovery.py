#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script per verificare il sistema di recovery e keep-alive del 555serverlite
"""

import datetime
import pytz

# Import delle funzioni dal 555serverlite
try:
    from importlib import import_module
    import sys
    import os
    
    # Aggiungi la directory corrente al path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Import del modulo (senza l'estensione .py)
    import importlib.util
    spec = importlib.util.spec_from_file_location("serverlite", "555-serverlite.py")
    serverlite = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(serverlite)
    
    print("✅ Modulo 555-serverlite caricato con successo!")
    
except Exception as e:
    print(f"❌ Errore nel caricamento del modulo: {e}")
    exit(1)

def test_recovery_logic():
    """Test della logica di recovery"""
    print("\n🧪 [TEST] Verifica logica recovery...")
    
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    current_time = now.strftime("%H:%M")
    
    print(f"⏰ Ora attuale: {current_time}")
    
    # Test condizioni recovery morning news
    morning_recovery_condition = (
        (now.hour > 8 or (now.hour == 8 and now.minute > 10)) and 
        now.hour < 12 and 
        (now.hour < 12 or (now.hour == 12 and now.minute < 30)) and
        not serverlite.is_message_sent_today("morning_news")
    )
    
    print(f"🌅 Condizione recovery morning news: {'✅ ATTIVA' if morning_recovery_condition else '❌ NON ATTIVA'}")
    
    if morning_recovery_condition:
        print("   → Il sistema dovrebbe recuperare il morning news ora!")
    else:
        if now.hour <= 8:
            print("   → Troppo presto per il recovery (prima delle 08:10)")
        elif now.hour >= 12:
            print("   → Troppo tardi per il recovery (dopo le 12:30)")
        elif serverlite.is_message_sent_today("morning_news"):
            print("   → Morning news già inviato oggi")
    
    # Test condizioni recovery daily report
    daily_recovery_condition = (
        ((now.hour > 12 or (now.hour == 12 and now.minute > 30)) and now.hour < 20) and
        not serverlite.is_message_sent_today("daily_report")
    )
    
    print(f"🍽️ Condizione recovery daily report: {'✅ ATTIVA' if daily_recovery_condition else '❌ NON ATTIVA'}")
    
    if daily_recovery_condition:
        print("   → Il sistema dovrebbe recuperare il daily report ora!")

def test_keep_alive():
    """Test del sistema keep-alive"""
    print("\n🔄 [TEST] Verifica sistema keep-alive...")
    
    is_active_time = serverlite.is_keep_alive_time()
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    print(f"⏰ Ora attuale: {now.strftime('%H:%M:%S')}")
    print(f"🚀 Keep-alive attivo: {'✅ SÌ' if is_active_time else '❌ NO'}")
    
    if is_active_time:
        print("   → L'app dovrebbe essere mantenuta attiva con ping ogni 5 minuti")
    else:
        print("   → L'app può andare in sleep (fuori finestra 06:00-22:00)")
    
    # Test URL keep-alive
    app_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:8000')
    print(f"🔗 URL per keep-alive: {app_url}")

def test_telegram_connection():
    """Test connessione Telegram"""
    print("\n📱 [TEST] Test connessione Telegram...")
    
    test_message = "🧪 TEST RECOVERY LOCALE\n\n✅ Sistema 555 Lite testato localmente\n🔄 Recovery e Keep-alive implementati\n📅 Pronto per deploy su Render\n\n🤖 Test completato!"
    
    print("📤 Invio messaggio di test...")
    
    try:
        success = serverlite.invia_messaggio_telegram(test_message)
        if success:
            print("✅ Messaggio di test inviato con successo!")
            print("📱 Controlla il canale Telegram: https://t.me/abkllr")
        else:
            print("❌ Invio messaggio fallito")
    except Exception as e:
        print(f"❌ Errore nell'invio: {e}")

def test_morning_news_generation():
    """Test generazione morning news"""
    print("\n🌅 [TEST] Test generazione morning news...")
    
    try:
        print("📰 Generazione eventi del giorno...")
        result = serverlite.genera_messaggio_eventi()
        print(f"📊 Risultato: {result}")
        
        if "✅" in result or "Messaggi eventi inviati" in result:
            print("✅ Morning news generato e inviato con successo!")
        else:
            print("⚠️ Possibili problemi nella generazione")
            
    except Exception as e:
        print(f"❌ Errore nella generazione morning news: {e}")

def main():
    """Esegue tutti i test"""
    print("🧪 [555-LITE-TEST] Avvio test sistema recovery e keep-alive")
    print("=" * 60)
    
    # Test logica recovery
    test_recovery_logic()
    
    # Test keep-alive
    test_keep_alive()
    
    # Test connessione Telegram (opzionale)
    user_input = input("\n📱 Vuoi testare l'invio di un messaggio Telegram? (y/n): ")
    if user_input.lower() in ['y', 'yes', 's', 'si']:
        test_telegram_connection()
    
    # Test generazione morning news (opzionale)
    user_input = input("\n🌅 Vuoi testare la generazione completa del morning news? (y/n): ")
    if user_input.lower() in ['y', 'yes', 's', 'si']:
        test_morning_news_generation()
    
    print("\n" + "=" * 60)
    print("🎯 [TEST] Test completati!")
    print("✅ Se tutti i test sono passati, il sistema è pronto per il deploy su Render")

if __name__ == "__main__":
    main()
