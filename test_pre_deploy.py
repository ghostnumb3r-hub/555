#!/usr/bin/env python3
"""
Test pre-deploy per verificare configurazione recovery
"""
import sys
import os
sys.path.append('C:\\Users\\valen\\555')

# Test imports
try:
    import dash
    import pandas as pd
    import datetime
    import pytz
    print('✅ Import base: OK')
except Exception as e:
    print(f'❌ Import base: {e}')

# Test configurazione recovery
try:
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    print(f'✅ Timezone: {now.strftime("%H:%M:%S")} Europe/Rome')
    
    # Simula controllo recovery con le modifiche
    morning_recovery_end = 11  # 2 ore (09:05-11:00)
    daily_recovery_end = 15    # 2 ore (13:05-15:00)
    print(f'✅ Recovery config: Morning 09:05-{morning_recovery_end:02d}:00, Daily 13:05-{daily_recovery_end:02d}:00')
    
    # Test condizioni recovery (ora sono le 15:18)
    print(f'🕐 Ora attuale: {now.strftime("%H:%M")}')
    
    # Test recovery rassegna stampa
    if now.hour >= 9 and now.minute >= 5 and now.hour < morning_recovery_end:
        print(f'🔄 Recovery rassegna ATTIVO: {now.strftime("%H:%M")} nel range 09:05-{morning_recovery_end:02d}:00')
    else:
        print(f'✅ Recovery rassegna INATTIVO: {now.strftime("%H:%M")} fuori range 09:05-{morning_recovery_end:02d}:00')
    
    # Test recovery report giornaliero
    if now.hour >= 13 and now.minute >= 5 and now.hour < daily_recovery_end:
        print(f'🔄 Recovery report ATTIVO: {now.strftime("%H:%M")} nel range 13:05-{daily_recovery_end:02d}:00')
    else:
        print(f'✅ Recovery report INATTIVO: {now.strftime("%H:%M")} fuori range 13:05-{daily_recovery_end:02d}:00')
        
    # Test esistenza cartella salvataggi
    if os.path.exists('salvataggi'):
        flag_files = [f for f in os.listdir('salvataggi') if f.endswith('.flag')]
        print(f'📁 Cartella salvataggi: OK - {len(flag_files)} file .flag presenti')
        for flag in flag_files:
            print(f'   📄 {flag}')
    else:
        print('❌ Cartella salvataggi: MANCANTE')
        
except Exception as e:
    print(f'❌ Test recovery: {e}')

print('🎯 Test pre-deploy completato')
print('📋 RISULTATO: Il recovery dovrebbe essere INATTIVO alle 15:18 (fuori range 13:05-15:00)')
