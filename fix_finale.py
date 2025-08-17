#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def fix_finale():
    """Fix finale del sistema 555lite"""
    
    with open('555-serverlite.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Keep-alive fino alle 24:00
    content = content.replace(
        '# Finestra keep-alive: 6:00 AM - 10:00 PM (22:00)',
        '# Finestra keep-alive: 6:00 AM - 12:00 AM (24:00)'
    )
    content = content.replace(
        'end_time = now.replace(hour=22, minute=0, second=0, microsecond=0)',
        'end_time = now.replace(hour=23, minute=59, second=0, microsecond=0)'
    )
    content = content.replace(
        '⏰ [KEEP-ALIVE] Ping ogni {keep_alive_interval_minutes} minuti (06:00-22:00)',
        '⏰ [KEEP-ALIVE] Ping ogni {keep_alive_interval_minutes} minuti (06:00-24:00)'
    )
    print("✅ Keep-alive esteso fino alle 24:00")
    
    # 2. Recovery Morning News - finestra 3 ore (08:10 + 3h = 11:10)
    old_morning_recovery = '''    # Controlla se il messaggio morning news è stato saltato (dopo le 8:10 e prima delle 12:30)
    if (now.hour > 8 or (now.hour == 8 and now.minute > 10)) and now.hour < 12 and \\
        (now.hour < 12 or (now.hour == 12 and now.minute < 30)) and \\
        not is_message_sent_today("morning_news"):'''
    
    new_morning_recovery = '''    # Recovery Morning News - 3 ore max (08:10 → 11:10)
    if (now.hour > 8 or (now.hour == 8 and now.minute > 10)) and \\
        (now.hour < 11 or (now.hour == 11 and now.minute <= 10)) and \\
        not is_message_sent_today("morning_news"):'''
    
    content = content.replace(old_morning_recovery, new_morning_recovery)
    print("✅ Morning recovery: 08:10 → 11:10 (3 ore)")
    
    # 3. Recovery Daily Lunch - finestra 3 ore (14:10 + 3h = 17:10)
    old_lunch_recovery = '''    # Controlla se il daily report è stato saltato (dopo le 14:10 e prima delle 20:00)
    if ((now.hour > 14 or (now.hour == 14 and now.minute > 10)) and now.hour < 20) and \\
        not is_message_sent_today("daily_report"):'''
    
    new_lunch_recovery = '''    # Recovery Daily Lunch - 3 ore max (14:10 → 17:10)
    if (now.hour > 14 or (now.hour == 14 and now.minute > 10)) and \\
        (now.hour < 17 or (now.hour == 17 and now.minute <= 10)) and \\
        not is_message_sent_today("daily_report"):'''
    
    content = content.replace(old_lunch_recovery, new_lunch_recovery)
    print("✅ Lunch recovery: 14:10 → 17:10 (3 ore)")
    
    # 4. Recovery Evening Report - finestra 3 ore (20:10 + 3h = 23:10)
    old_evening_recovery = '''    # Controlla se l'evening report è stato saltato (dopo le 20:10 e prima delle 23:59)
    if ((now.hour > 20 or (now.hour == 20 and now.minute > 10)) and now.hour < 24) and \\
        not is_message_sent_today("evening_report"):'''
    
    new_evening_recovery = '''    # Recovery Evening Report - 3 ore max (20:10 → 23:10)
    if (now.hour > 20 or (now.hour == 20 and now.minute > 10)) and \\
        (now.hour < 23 or (now.hour == 23 and now.minute <= 10)) and \\
        not is_message_sent_today("evening_report"):'''
    
    content = content.replace(old_evening_recovery, new_evening_recovery)
    print("✅ Evening recovery: 20:10 → 23:10 (3 ore)")
    
    # 5. Aggiorna i testi di recovery
    content = content.replace(
        'print("🔄 [RECUPERO] Morning news non inviate alle 08:10, recupero automatico...")',
        'print("🔄 [RECUPERO] Morning News mancate (08:10), recovery attivo fino alle 11:10...")'
    )
    content = content.replace(
        'print("🔄 [RECUPERO] Daily report non inviato alle 14:10, recupero automatico...")',
        'print("🔄 [RECUPERO] Daily Lunch mancato (14:10), recovery attivo fino alle 17:10...")'
    )
    content = content.replace(
        'print("🔄 [RECUPERO] Evening report non inviato alle 20:10, recupero automatico...")',
        'print("🔄 [RECUPERO] Evening Report mancato (20:10), recovery attivo fino alle 23:10...")'
    )
    print("✅ Testi recovery aggiornati")
    
    # Salva il file
    with open('555-serverlite.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎯 MODIFICHE FINALI APPLICATE:")
    print("• Keep-alive: 06:00 → 24:00 (18 ore)")
    print("• Recovery Morning: 08:10 → 11:10 (3 ore max)")  
    print("• Recovery Lunch: 14:10 → 17:10 (3 ore max)")
    print("• Recovery Evening: 20:10 → 23:10 (3 ore max)")
    print("\n🚀 Sistema 555lite COMPLETAMENTE PRONTO PER DEPLOY!")
    print("📱 Tutti i messaggi hanno recovery automatico a 3 ore")
    print("⚡ Keep-alive attivo quasi 24/7")

if __name__ == "__main__":
    fix_finale()
