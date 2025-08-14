#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script per generazione manuale report Dashboard 555
"""

import sys
import os
import datetime
import pytz
import importlib.util

# Carica il modulo 555.py
spec = importlib.util.spec_from_file_location("dashboard555", "C:\\Users\\valen\\555\\555.py")
dashboard555 = importlib.util.module_from_spec(spec)
sys.modules["dashboard555"] = dashboard555
spec.loader.exec_module(dashboard555)

def main():
    print("🚀 GENERAZIONE REPORT MANUALE - INIZIO")
    print("=" * 50)
    
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    print(f"⏰ Orario corrente: {now.strftime('%H:%M:%S')} - {now.strftime('%d/%m/%Y')}")
    
    # 1. REPORT GIORNALIERO
    print("\n📊 GENERAZIONE REPORT GIORNALIERO...")
    try:
        result = dashboard555.generate_unified_report(report_type="manual", now=now)
        if result:
            print("✅ Report giornaliero generato e inviato con successo!")
        else:
            print("⚠️ Report giornaliero - problemi durante generazione")
    except Exception as e:
        print(f"❌ Errore report giornaliero: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. REPORT SETTIMANALE (solo se lunedì)
    if now.weekday() == 0:  # Lunedì
        print("\n📈 GENERAZIONE REPORT SETTIMANALE (LUNEDÌ)...")
        try:
            weekly_backtest = dashboard555.generate_weekly_backtest_summary()
            if weekly_backtest:
                weekly_message = f"📈 *REPORT SETTIMANALE MANUALE - {now.strftime('%d/%m/%Y %H:%M')}*\n\n{weekly_backtest}"
                
                # Gestione lunghezza messaggio
                if len(weekly_message) > 4000:
                    print(f"⚠️ Report settimanale lungo ({len(weekly_message)} caratteri), suddivisione...")
                    header = f"📈 *REPORT SETTIMANALE (parte 1) - {now.strftime('%d/%m/%Y %H:%M')}*\n\n"
                    content_chunks = [weekly_backtest[i:i+3500] for i in range(0, len(weekly_backtest), 3500)]
                    
                    for i, chunk in enumerate(content_chunks):
                        if i == 0:
                            message = header + chunk
                        else:
                            message = f"📈 *REPORT SETTIMANALE (parte {i+1})*\n\n{chunk}"
                        
                        result = dashboard555.invia_messaggio_telegram(message)
                        print(f"✅ Report settimanale parte {i+1}/{len(content_chunks)} inviato ({len(message)} caratteri)")
                        
                        if i < len(content_chunks) - 1:
                            import time
                            time.sleep(2)
                else:
                    result = dashboard555.invia_messaggio_telegram(weekly_message)
                    print(f"✅ Report settimanale inviato ({len(weekly_message)} caratteri)")
            else:
                print("⚠️ Nessun dato per il report settimanale")
        except Exception as e:
            print(f"❌ Errore report settimanale: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"\nℹ️ Oggi non è lunedì (giorno {now.weekday()}), salto report settimanale")
    
    print("\n🎯 GENERAZIONE REPORT MANUALE - COMPLETATA")
    print("=" * 50)

if __name__ == "__main__":
    main()
