#!/usr/bin/env python3
"""
Sistema di backup giornaliero automatico per Render
Salva ogni giorno con timestamp unico su Google Drive
"""
import os
import datetime
import shutil
from pathlib import Path
import json
from drive_config import save_to_drive, get_timestamp_filename, get_render_path

# Percorsi
LOCAL_SALVATAGGI = Path("salvataggi")  # Percorso relativo per Render
DRIVE_BASE = Path("H:/Il mio Drive/555")  # Base Drive (quando locale)

# Per Render, usa percorsi API o relativi
RENDER_MODE = os.getenv('RENDER') or os.getenv('RENDER_SERVICE_NAME')

def get_italy_timestamp():
    """Ottiene timestamp italiano"""
    import pytz
    italy_tz = pytz.timezone('Europe/Rome')
    return datetime.datetime.now(italy_tz)

def create_daily_folder_name():
    """Crea nome cartella per il giorno corrente"""
    now = get_italy_timestamp()
    return f"backup_{now.strftime('%Y%m%d')}"

def backup_daily_to_drive():
    """
    Esegue backup giornaliero con timestamp univoco
    Ogni giorno crea una cartella separata su Drive
    """
    now = get_italy_timestamp()
    daily_folder = create_daily_folder_name()
    
    print(f"🔄 [RENDER-BACKUP] Avvio backup giornaliero: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Se siamo su Render, usa API per caricare su Drive
    if RENDER_MODE:
        return backup_via_render_api(daily_folder)
    else:
        return backup_via_local_drive(daily_folder)

def backup_via_local_drive(daily_folder):
    """Backup quando siamo in locale con accesso a Drive"""
    daily_path = DRIVE_BASE / "daily_backups" / daily_folder
    daily_path.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_files = 0
    
    if LOCAL_SALVATAGGI.exists():
        for file_path in LOCAL_SALVATAGGI.glob("*"):
            if file_path.is_file():
                total_files += 1
                try:
                    # Copia con timestamp nel nome
                    dest_file = daily_path / f"{file_path.stem}_{daily_folder}{file_path.suffix}"
                    
                    if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.pkl']:
                        dest_file.write_bytes(file_path.read_bytes())
                    else:
                        dest_file.write_text(file_path.read_text(encoding='utf-8', errors='ignore'), encoding='utf-8')
                    
                    success_count += 1
                    print(f"✅ Salvato: {file_path.name} -> {dest_file.name}")
                except Exception as e:
                    print(f"❌ Errore: {file_path.name}: {e}")
    
    # Salva log giornaliero
    log_data = {
        "date": get_italy_timestamp().isoformat(),
        "files_backed_up": success_count,
        "total_files": total_files,
        "folder": str(daily_path),
        "render_mode": bool(RENDER_MODE)
    }
    
    log_file = daily_path / f"daily_log_{daily_folder}.json"
    log_file.write_text(json.dumps(log_data, indent=2), encoding='utf-8')
    
    print(f"📊 Backup giornaliero completato: {success_count}/{total_files} file")
    return success_count > 0

def backup_via_render_api(daily_folder):
    """Backup da Render usando API o servizi cloud"""
    print(f"🌐 [RENDER] Modalità Render attiva - backup via API")
    
    # Raccogli tutti i file da salvare
    files_to_backup = []
    
    if LOCAL_SALVATAGGI.exists():
        for file_path in LOCAL_SALVATAGGI.glob("*"):
            if file_path.is_file():
                try:
                    # Leggi contenuto
                    if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.pkl']:
                        content = file_path.read_bytes()
                        encoding = 'binary'
                    else:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        encoding = 'text'
                    
                    files_to_backup.append({
                        'name': f"{file_path.stem}_{daily_folder}{file_path.suffix}",
                        'content': content,
                        'encoding': encoding,
                        'size': file_path.stat().st_size
                    })
                    
                except Exception as e:
                    print(f"❌ Errore lettura {file_path.name}: {e}")
    
    # Invia a servizio di backup (GitHub, Pastebin, etc.)
    success_count = 0
    for file_data in files_to_backup:
        if send_to_backup_service(file_data, daily_folder):
            success_count += 1
    
    print(f"📊 [RENDER] Backup API completato: {success_count}/{len(files_to_backup)} file")
    return success_count > 0

def send_to_backup_service(file_data, daily_folder):
    """Invia file a servizio di backup esterno"""
    try:
        # Opzione 1: GitHub Gist
        if send_to_github_gist(file_data, daily_folder):
            return True
        
        # Opzione 2: Telegram come backup
        if send_to_telegram_backup(file_data, daily_folder):
            return True
        
        return False
    except Exception as e:
        print(f"❌ Errore backup service: {e}")
        return False

def send_to_github_gist(file_data, daily_folder):
    """Salva su GitHub Gist (gratuito, pubblico/privato)"""
    import requests
    
    # Token GitHub (da configurare)
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Imposta come variabile d'ambiente
    
    if not GITHUB_TOKEN:
        print("⚠️ GitHub token non configurato")
        return False
    
    gist_data = {
        "description": f"555 Backup {daily_folder} - {file_data['name']}",
        "public": False,  # Gist privato
        "files": {
            file_data['name']: {
                "content": file_data['content'] if file_data['encoding'] == 'text' else 
                          str(file_data['content'])  # Converti bytes a string per Gist
            }
        }
    }
    
    try:
        response = requests.post(
            'https://api.github.com/gists',
            headers={'Authorization': f'token {GITHUB_TOKEN}'},
            json=gist_data,
            timeout=30
        )
        
        if response.status_code == 201:
            gist_url = response.json().get('html_url', 'N/A')
            print(f"✅ [GITHUB] {file_data['name']} -> {gist_url}")
            return True
        else:
            print(f"❌ [GITHUB] Errore {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ [GITHUB] Errore: {e}")
        return False

def send_to_telegram_backup(file_data, daily_folder):
    """Invia file come backup su Telegram"""
    import requests
    
    TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
    TELEGRAM_CHAT_ID = "@abkllr"
    
    # Per file di testo piccoli, invia come messaggio
    if file_data['encoding'] == 'text' and file_data['size'] < 3000:
        message = f"🔄 BACKUP {daily_folder}\n📁 {file_data['name']}\n\n```\n{file_data['content'][:2000]}```"
        
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                data={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": message,
                    "parse_mode": "Markdown"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"✅ [TELEGRAM] {file_data['name']} inviato")
                return True
                
        except Exception as e:
            print(f"❌ [TELEGRAM] Errore: {e}")
    
    return False

def schedule_daily_backup():
    """Programma il backup giornaliero"""
    import schedule
    import time
    import threading
    
    def run_backup():
        print(f"🕐 Backup programmato avviato...")
        backup_daily_to_drive()
    
    # Programma backup alle 23:30 ogni giorno
    schedule.every().day.at("23:30").do(run_backup)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    # Avvia scheduler in thread separato
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("⏰ Backup giornaliero programmato alle 23:30")

# Funzione da chiamare dal sistema principale
def integrate_daily_backup():
    """Integra il backup giornaliero nel sistema 555"""
    
    # Esegui backup immediato se è passato più di 1 giorno
    last_backup_file = Path("last_backup.txt")
    today = get_italy_timestamp().strftime('%Y%m%d')
    
    should_backup = True
    if last_backup_file.exists():
        try:
            last_date = last_backup_file.read_text().strip()
            should_backup = last_date != today
        except:
            pass
    
    if should_backup:
        print(f"🔄 Eseguendo backup giornaliero per {today}")
        if backup_daily_to_drive():
            last_backup_file.write_text(today)
    else:
        print(f"✅ Backup già eseguito oggi ({today})")
    
    # Programma i prossimi backup
    schedule_daily_backup()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backup":
            backup_daily_to_drive()
        elif command == "schedule":
            schedule_daily_backup()
            print("Scheduler avviato... (Ctrl+C per fermare)")
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Scheduler fermato")
        else:
            print("Comandi:")
            print("  python render_daily_backup.py backup")
            print("  python render_daily_backup.py schedule")
    else:
        backup_daily_to_drive()
