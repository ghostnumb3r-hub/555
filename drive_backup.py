#!/usr/bin/env python3
"""
Sistema di backup automatico su Google Drive
Copia tutti i file di salvataggio su Drive per preservarli durante i restart di Render
"""
import os
import shutil
import datetime
import json
from pathlib import Path
from drive_config import save_to_drive, get_render_path, get_timestamp_filename

# Percorsi
LOCAL_SALVATAGGI = Path("C:/Users/valen/555/salvataggi")
DRIVE_SALVATAGGI = Path("H:/Il mio Drive/555/salvataggi")

def ensure_drive_salvataggi():
    """Crea la cartella salvataggi su Drive se non esiste"""
    DRIVE_SALVATAGGI.mkdir(parents=True, exist_ok=True)
    print(f"✅ Cartella Drive: {DRIVE_SALVATAGGI}")

def backup_file_to_drive(file_path, preserve_structure=True):
    """
    Copia un singolo file su Google Drive
    
    Args:
        file_path (Path): Percorso del file locale
        preserve_structure (bool): Mantiene la struttura delle cartelle
    
    Returns:
        bool: True se backup riuscito
    """
    try:
        if not file_path.exists():
            print(f"⚠️ File non trovato: {file_path}")
            return False
        
        # Determina il percorso di destinazione su Drive
        if preserve_structure:
            # Mantiene la stessa struttura (salvataggi/nome_file.ext)
            drive_path = DRIVE_SALVATAGGI / file_path.name
        else:
            # Usa il sistema di categorizzazione per tipo file
            extension = file_path.suffix.lower()
            if extension in ['.csv', '.txt', '.json']:
                folder_type = 'exports'
            elif extension in ['.png', '.jpg', '.jpeg', '.gif']:
                folder_type = 'images'
            else:
                folder_type = 'exports'
            
            folder_path = get_render_path(folder_type, use_cloud=True)
            drive_path = folder_path / file_path.name
        
        # Leggi e copia il file
        if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.pkl']:
            # File binari
            content = file_path.read_bytes()
        else:
            # File di testo
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Crea directory se necessaria
        drive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salva il file
        if isinstance(content, bytes):
            drive_path.write_bytes(content)
        else:
            drive_path.write_text(content, encoding='utf-8')
        
        print(f"✅ Backup: {file_path.name} -> {drive_path}")
        return True
        
    except Exception as e:
        print(f"❌ Errore backup {file_path.name}: {e}")
        return False

def backup_all_salvataggi():
    """Esegue il backup di tutti i file nella cartella salvataggi"""
    ensure_drive_salvataggi()
    
    if not LOCAL_SALVATAGGI.exists():
        print(f"⚠️ Cartella locale non trovata: {LOCAL_SALVATAGGI}")
        return False
    
    success_count = 0
    total_files = 0
    
    print(f"🔄 Avvio backup da: {LOCAL_SALVATAGGI}")
    print(f"🔄 Destinazione: {DRIVE_SALVATAGGI}")
    
    # Elenca tutti i file nella cartella salvataggi
    for file_path in LOCAL_SALVATAGGI.glob("*"):
        if file_path.is_file():  # Solo file, non cartelle
            total_files += 1
            if backup_file_to_drive(file_path, preserve_structure=True):
                success_count += 1
    
    print(f"\n📊 Backup completato: {success_count}/{total_files} file copiati")
    
    # Salva log del backup
    backup_log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "files_backed_up": success_count,
        "total_files": total_files,
        "success_rate": f"{(success_count/total_files*100):.1f}%" if total_files > 0 else "0%"
    }
    
    log_content = json.dumps(backup_log, indent=2)
    log_filename = get_timestamp_filename("backup_log", "json")
    save_to_drive(log_content, log_filename, 'exports', use_cloud=True)
    
    return success_count == total_files

def auto_backup_on_change():
    """Monitora la cartella e esegue backup automatico quando cambia qualcosa"""
    import time
    
    print("🔍 Avvio monitoraggio automatico salvataggi...")
    
    # Memorizza l'ultimo stato della cartella
    last_state = {}
    
    while True:
        try:
            current_state = {}
            
            if LOCAL_SALVATAGGI.exists():
                for file_path in LOCAL_SALVATAGGI.glob("*"):
                    if file_path.is_file():
                        current_state[file_path.name] = file_path.stat().st_mtime
            
            # Confronta con lo stato precedente
            changed_files = []
            for filename, mtime in current_state.items():
                if filename not in last_state or last_state[filename] != mtime:
                    changed_files.append(filename)
            
            # Se ci sono cambiamenti, esegui backup
            if changed_files:
                print(f"📁 Rilevati cambiamenti in: {', '.join(changed_files)}")
                backup_all_salvataggi()
            
            last_state = current_state
            time.sleep(30)  # Controlla ogni 30 secondi
            
        except KeyboardInterrupt:
            print("🛑 Monitoraggio interrotto dall'utente")
            break
        except Exception as e:
            print(f"❌ Errore nel monitoraggio: {e}")
            time.sleep(60)  # Aspetta di più in caso di errore

def restore_from_drive():
    """Ripristina i file da Google Drive alla cartella locale"""
    ensure_drive_salvataggi()
    LOCAL_SALVATAGGI.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_files = 0
    
    print(f"🔄 Ripristino da: {DRIVE_SALVATAGGI}")
    print(f"🔄 Destinazione: {LOCAL_SALVATAGGI}")
    
    if not DRIVE_SALVATAGGI.exists():
        print("⚠️ Nessun backup trovato su Drive")
        return False
    
    for drive_file in DRIVE_SALVATAGGI.glob("*"):
        if drive_file.is_file():
            total_files += 1
            try:
                local_file = LOCAL_SALVATAGGI / drive_file.name
                
                # Copia il file
                shutil.copy2(drive_file, local_file)
                success_count += 1
                print(f"✅ Ripristinato: {drive_file.name}")
                
            except Exception as e:
                print(f"❌ Errore ripristino {drive_file.name}: {e}")
    
    print(f"\n📊 Ripristino completato: {success_count}/{total_files} file ripristinati")
    return success_count == total_files

# Funzioni di integrazione per il sistema 555
def integrate_with_555():
    """Funzioni da chiamare dal sistema 555 per backup automatico"""
    
    def backup_after_save(filepath=None):
        """Chiama questa funzione dopo ogni salvataggio"""
        if filepath:
            file_path = Path(filepath)
            backup_file_to_drive(file_path)
        else:
            backup_all_salvataggi()
    
    def startup_restore():
        """Chiama questa all'avvio del sistema 555"""
        print("🔄 Controllo backup su Drive all'avvio...")
        if DRIVE_SALVATAGGI.exists() and any(DRIVE_SALVATAGGI.glob("*")):
            user_input = input("🔄 Trovato backup su Drive. Ripristinare? (y/n): ")
            if user_input.lower() in ['y', 'yes', 's', 'si']:
                restore_from_drive()
        else:
            print("📁 Nessun backup precedente trovato")
    
    return backup_after_save, startup_restore

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backup":
            backup_all_salvataggi()
        elif command == "restore": 
            restore_from_drive()
        elif command == "monitor":
            auto_backup_on_change()
        else:
            print("Comandi disponibili:")
            print("  python drive_backup.py backup   - Backup immediato")
            print("  python drive_backup.py restore  - Ripristina da Drive") 
            print("  python drive_backup.py monitor  - Monitoraggio automatico")
    else:
        # Test di default
        print("🔍 Test del sistema di backup...")
        backup_all_salvataggi()
