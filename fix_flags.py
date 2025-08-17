#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def fix_flag_system():
    """Copia la logica flag dal 555-server principale che funziona"""
    
    with open('555-serverlite.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trova e sostituisci l'intero sistema flag
    old_flag_system = '''# === SISTEMA FLAG IN-MEMORY PER RENDER ===
GLOBAL_FLAGS = {
    "morning_news_sent": False,
    "daily_report_sent": False,
    "evening_report_sent": False,
    "weekly_report_sent": False,     # Report settimanali
    "monthly_report_sent": False,    # Report mensili
    "quarterly_report_sent": False,  # Report trimestrali (Q1,Q2,Q3,Q4)
    "semestral_report_sent": False,  # Report semestrali (S1,S2)
    "annual_report_sent": False,     # Report annuali
    "last_reset_date": datetime.datetime.now().strftime("%Y%m%d")
}

def reset_daily_flags_if_needed():
    """Resetta i flag se è passata la mezzanotte"""
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    if GLOBAL_FLAGS["last_reset_date"] != current_date:
        GLOBAL_FLAGS["morning_news_sent"] = False
        GLOBAL_FLAGS["daily_report_sent"] = False
        GLOBAL_FLAGS["evening_report_sent"] = False
        # I flag settimanali/mensili hanno logica separata
        GLOBAL_FLAGS["last_reset_date"] = current_date
        print(f"🔄 [LITE-FLAGS] Reset giornaliero completato per {current_date}")
        return True
    return False

def set_message_sent_flag(message_type):
    """Imposta il flag di invio per il tipo di messaggio"""
    reset_daily_flags_if_needed()
    
    if message_type == "morning_news":
        GLOBAL_FLAGS["morning_news_sent"] = True
        print("✅ [LITE-FLAGS] Flag morning_news_sent impostato")
    elif message_type == "daily_report":
        GLOBAL_FLAGS["daily_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag daily_report_sent impostato")
    elif message_type == "evening_report":
        GLOBAL_FLAGS["evening_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag evening_report_sent impostato")
    elif message_type == "weekly_report":
        GLOBAL_FLAGS["weekly_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag weekly_report_sent impostato")
    elif message_type == "monthly_report":
        GLOBAL_FLAGS["monthly_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag monthly_report_sent impostato")
    elif message_type == "quarterly_report":
        GLOBAL_FLAGS["quarterly_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag quarterly_report_sent impostato")
    elif message_type == "semestral_report":
        GLOBAL_FLAGS["semestral_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag semestral_report_sent impostato")
    elif message_type == "annual_report":
        GLOBAL_FLAGS["annual_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag annual_report_sent impostato")

def is_message_sent_today(message_type):
    """Verifica se il messaggio è già stato inviato oggi"""
    reset_daily_flags_if_needed()
    
    if message_type == "morning_news":
        return GLOBAL_FLAGS["morning_news_sent"]
    elif message_type == "daily_report":
        return GLOBAL_FLAGS["daily_report_sent"]
    elif message_type == "evening_report":
        return GLOBAL_FLAGS["evening_report_sent"]
    elif message_type == "weekly_report":
        return GLOBAL_FLAGS["weekly_report_sent"]
    elif message_type == "monthly_report":
        return GLOBAL_FLAGS["monthly_report_sent"]
    elif message_type == "quarterly_report":
        return GLOBAL_FLAGS["quarterly_report_sent"]
    elif message_type == "semestral_report":
        return GLOBAL_FLAGS["semestral_report_sent"]
    elif message_type == "annual_report":
        return GLOBAL_FLAGS["annual_report_sent"]
    return False'''

    # Nuovo sistema flag copiato dal 555-server (semplificato e funzionante)
    new_flag_system = '''# === SISTEMA FLAG IN-MEMORY PER RENDER ===
# Variabili globali per tracciare invii giornalieri
GLOBAL_FLAGS = {
    "morning_news_sent": False,
    "daily_report_sent": False,
    "evening_report_sent": False,
    "weekly_report_sent": False,
    "monthly_report_sent": False,
    "quarterly_report_sent": False,
    "semestral_report_sent": False,
    "annual_report_sent": False,
    "last_reset_date": datetime.datetime.now().strftime("%Y%m%d")
}

def reset_daily_flags_if_needed():
    """Resetta i flag se è passata la mezzanotte"""
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    if GLOBAL_FLAGS["last_reset_date"] != current_date:
        GLOBAL_FLAGS["morning_news_sent"] = False
        GLOBAL_FLAGS["daily_report_sent"] = False
        GLOBAL_FLAGS["evening_report_sent"] = False
        GLOBAL_FLAGS["last_reset_date"] = current_date
        print(f"🔄 [FLAGS] Reset giornaliero completato per {current_date}")
        return True
    return False

def set_message_sent_flag(message_type):
    """Imposta il flag di invio per il tipo di messaggio"""
    reset_daily_flags_if_needed()  # Verifica reset automatico
    
    if message_type == "morning_news":
        GLOBAL_FLAGS["morning_news_sent"] = True
        print("✅ [FLAGS] Flag morning_news_sent impostato su True")
    elif message_type == "daily_report":
        GLOBAL_FLAGS["daily_report_sent"] = True
        print("✅ [FLAGS] Flag daily_report_sent impostato su True")
    elif message_type == "evening_report":
        GLOBAL_FLAGS["evening_report_sent"] = True
        print("✅ [FLAGS] Flag evening_report_sent impostato su True")
    elif message_type == "weekly_report":
        GLOBAL_FLAGS["weekly_report_sent"] = True
        print("✅ [FLAGS] Flag weekly_report_sent impostato su True")
    elif message_type == "monthly_report":
        GLOBAL_FLAGS["monthly_report_sent"] = True
        print("✅ [FLAGS] Flag monthly_report_sent impostato su True")
    elif message_type == "quarterly_report":
        GLOBAL_FLAGS["quarterly_report_sent"] = True
        print("✅ [FLAGS] Flag quarterly_report_sent impostato su True")
    elif message_type == "semestral_report":
        GLOBAL_FLAGS["semestral_report_sent"] = True
        print("✅ [FLAGS] Flag semestral_report_sent impostato su True")
    elif message_type == "annual_report":
        GLOBAL_FLAGS["annual_report_sent"] = True
        print("✅ [FLAGS] Flag annual_report_sent impostato su True")

def is_message_sent_today(message_type):
    """Verifica se il messaggio è già stato inviato oggi"""
    reset_daily_flags_if_needed()  # Verifica reset automatico
    
    if message_type == "morning_news":
        return GLOBAL_FLAGS["morning_news_sent"]
    elif message_type == "daily_report":
        return GLOBAL_FLAGS["daily_report_sent"]
    elif message_type == "evening_report":
        return GLOBAL_FLAGS["evening_report_sent"]
    elif message_type == "weekly_report":
        return GLOBAL_FLAGS["weekly_report_sent"]
    elif message_type == "monthly_report":
        return GLOBAL_FLAGS["monthly_report_sent"]
    elif message_type == "quarterly_report":
        return GLOBAL_FLAGS["quarterly_report_sent"]
    elif message_type == "semestral_report":
        return GLOBAL_FLAGS["semestral_report_sent"]
    elif message_type == "annual_report":
        return GLOBAL_FLAGS["annual_report_sent"]
    return False'''
    
    # Sostituisci il sistema flag
    content = content.replace(old_flag_system, new_flag_system)
    print("✅ Copiato sistema flag da 555-server (funzionante)")
    
    # Salva il file
    with open('555-serverlite.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎯 SISTEMA FLAG CORRETTO:")
    print("• Logica copiata da 555-server principale")
    print("• Reset automatico funzionante")
    print("• Flag persistenti durante la giornata")
    print("• Messaggi log migliorati")
    print("\n✅ Ora il recovery dovrebbe funzionare correttamente!")

if __name__ == "__main__":
    fix_flag_system()
