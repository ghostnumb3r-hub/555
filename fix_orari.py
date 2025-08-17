#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per correggere solo gli orari dei report nel sistema 555lite
"""

def fix_schedule_times():
    """Applica le modifiche agli orari nel file 555-serverlite.py"""
    
    file_path = "H:\\Il mio Drive\\555lite\\555-serverlite.py"
    
    # Leggi il file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Applica le sostituzioni degli orari
    replacements = [
        # Weekly report: da 19:00 a 18:00
        ('current_day == "Sunday" and current_time == "19:00" and not is_message_sent_today("weekly_report")', 
         'current_day == "Sunday" and current_time == "18:00" and not is_message_sent_today("weekly_report")'),
        
        # Monthly report: da 19:30 a 18:15
        ('is_month_end and current_time == "19:30" and not is_message_sent_today("monthly_report")', 
         'is_month_end and current_time == "18:15" and not is_message_sent_today("monthly_report")'),
    ]
    
    # Aggiungi i nuovi report trimestrali, semestrali e annuali
    scheduler_additions = '''
    # NUOVO - Report trimestrale (ultimo giorno del trimestre, 18:30)
    is_quarter_end = now.month in [3, 6, 9, 12] and is_month_end
    if is_quarter_end and current_time == "18:30" and not is_message_sent_today("quarterly_report"):
        print("📊 [SCHEDULER] Avvio report trimestrale...")
        result = genera_report_trimestrale()
        print(f"Quarterly report result: {result}")
    
    # NUOVO - Report semestrale (30 giugno e 31 dicembre, 18:45)
    is_semester_end = (now.month == 6 and now.day == 30) or (now.month == 12 and now.day == 31)
    if is_semester_end and current_time == "18:45" and not is_message_sent_today("semestral_report"):
        print("📊 [SCHEDULER] Avvio report semestrale...")
        result = genera_report_semestrale()
        print(f"Semestral report result: {result}")
    
    # NUOVO - Report annuale (31 dicembre, 19:00)
    is_year_end = now.month == 12 and now.day == 31
    if is_year_end and current_time == "19:00" and not is_message_sent_today("annual_report"):
        print("📊 [SCHEDULER] Avvio report annuale...")
        result = genera_report_annuale()
        print(f"Annual report result: {result}")'''
    
    # Applica le sostituzioni
    for old, new in replacements:
        content = content.replace(old, new)
        print(f"✅ Sostituito: {old[:50]}...")
    
    # Trova il punto dove aggiungere i nuovi scheduler (dopo monthly report)
    insertion_point = content.find('print(f"Monthly report result: {result}")')
    if insertion_point != -1:
        # Trova la fine della riga
        end_point = content.find('\n', insertion_point) + 1
        # Inserisci i nuovi scheduler
        content = content[:end_point] + scheduler_additions + content[end_point:]
        print("✅ Aggiunti nuovi scheduler per trimestre, semestre e anno")
    
    # Scrivi il file modificato
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎯 CORREZIONI APPLICATE:")
    print("• Weekly Report: Domenica 18:00")
    print("• Monthly Report: Fine mese 18:15")  
    print("• Quarterly Report: Fine trimestre 18:30")
    print("• Semestral Report: 30/6 e 31/12 alle 18:45")
    print("• Annual Report: 31/12 alle 19:00")
    print("\n✅ File 555-serverlite.py aggiornato con successo!")

if __name__ == "__main__":
    fix_schedule_times()
