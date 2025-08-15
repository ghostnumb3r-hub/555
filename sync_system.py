# === SYNC SYSTEM - LOCALE <-> RENDER ===
"""
Sistema di sincronizzazione bidirezionale tra:
- Locale: C:/Users/valen/555/salvataggi/
- Render: /app/salvataggi/ (via API)
"""

import os
import requests
import json
import time
from datetime import datetime, timedelta
import pytz
from pathlib import Path

class SalvataggieSync:
    def __init__(self, render_url="https://tua-app.render.com", local_path=r"C:\Users\valen\555\salvataggi"):
        self.render_url = render_url
        self.local_path = Path(local_path)
        self.italy_tz = pytz.timezone('Europe/Rome')
        
        # Configurazione sync
        self.sync_interval_minutes = 15  # Sync ogni 15 minuti
        self.files_to_sync = [
            "analysis_text.txt",
            "segnali_tecnici.csv", 
            "previsioni_ml.csv",
            "weekly_report_enhanced.txt",
            "portfolio_analysis.txt"
        ]
        
    def get_local_files_info(self):
        """Ottieni info sui file locali (timestamp, size)"""
        files_info = {}
        
        for filename in self.files_to_sync:
            file_path = self.local_path / filename
            if file_path.exists():
                stat = file_path.stat()
                files_info[filename] = {
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime, self.italy_tz).isoformat(),
                    "exists": True
                }
            else:
                files_info[filename] = {"exists": False}
                
        return files_info
    
    def get_render_files_info(self):
        """Ottieni info sui file Render via API (da implementare in 555-server.py)"""
        try:
            # API endpoint da aggiungere a 555-server.py
            response = requests.get(f"{self.render_url}/api/files-info", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ [SYNC] Render API non disponibile: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ [SYNC] Errore connessione Render: {e}")
            return {}
    
    def download_file_from_render(self, filename):
        """Scarica file da Render → Locale"""
        try:
            response = requests.get(f"{self.render_url}/api/download/{filename}", timeout=30)
            if response.status_code == 200:
                local_file = self.local_path / filename
                with open(local_file, 'wb') as f:
                    f.write(response.content)
                print(f"⬇️ [SYNC] Downloaded: {filename}")
                return True
            else:
                print(f"❌ [SYNC] Download failed {filename}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ [SYNC] Download error {filename}: {e}")
            return False
    
    def upload_file_to_render(self, filename):
        """Upload file da Locale → Render"""
        try:
            local_file = self.local_path / filename
            if not local_file.exists():
                print(f"⚠️ [SYNC] File locale non esiste: {filename}")
                return False
                
            with open(local_file, 'rb') as f:
                files = {'file': (filename, f)}
                response = requests.post(f"{self.render_url}/api/upload", files=files, timeout=30)
                
            if response.status_code == 200:
                print(f"⬆️ [SYNC] Uploaded: {filename}")
                return True
            else:
                print(f"❌ [SYNC] Upload failed {filename}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ [SYNC] Upload error {filename}: {e}")
            return False
    
    def sync_files(self, direction="auto"):
        """
        Sincronizza file
        direction: "auto" | "to_render" | "from_render" | "both"
        """
        print(f"🔄 [SYNC] Inizio sincronizzazione - {datetime.now(self.italy_tz).strftime('%H:%M:%S')}")
        
        local_info = self.get_local_files_info()
        render_info = self.get_render_files_info()
        
        if not render_info and direction == "auto":
            print("⚠️ [SYNC] Render non disponibile, solo backup locale")
            return
            
        for filename in self.files_to_sync:
            local_exists = local_info.get(filename, {}).get("exists", False)
            render_exists = render_info.get(filename, {}).get("exists", False)
            
            if direction == "to_render" or (direction == "auto" and local_exists and not render_exists):
                # Locale → Render
                self.upload_file_to_render(filename)
                
            elif direction == "from_render" or (direction == "auto" and render_exists and not local_exists):
                # Render → Locale  
                self.download_file_from_render(filename)
                
            elif direction == "both" or direction == "auto":
                # Confronta timestamp per il più recente
                if local_exists and render_exists:
                    local_time = datetime.fromisoformat(local_info[filename]["modified"])
                    render_time = datetime.fromisoformat(render_info[filename]["modified"])
                    
                    if local_time > render_time:
                        self.upload_file_to_render(filename)
                    elif render_time > local_time:
                        self.download_file_from_render(filename)
                    else:
                        print(f"✅ [SYNC] {filename} già sincronizzato")
        
        print(f"✅ [SYNC] Sincronizzazione completata - {datetime.now(self.italy_tz).strftime('%H:%M:%S')}")
    
    def start_continuous_sync(self):
        """Avvia sync continuo in background"""
        print(f"🚀 [SYNC] Avvio sync continuo ogni {self.sync_interval_minutes} minuti")
        
        while True:
            try:
                self.sync_files("auto")
                time.sleep(self.sync_interval_minutes * 60)
            except KeyboardInterrupt:
                print("🛑 [SYNC] Sync interrotto dall'utente")
                break
            except Exception as e:
                print(f"❌ [SYNC] Errore nel loop: {e}")
                time.sleep(60)  # Riprova tra 1 minuto

# === USAGE ===
if __name__ == "__main__":
    # Inizializza sync system
    sync = SalvataggieSync(
        render_url="https://five55-mdye.onrender.com",  # URL RENDER NUOVO E FUNZIONANTE ✅
        local_path="C:\\Users\\valen\\555\\salvataggi"
    )
    
    print("🔄 SYNC SYSTEM - Dashboard 555")
    print("1. Sync una volta: sync.sync_files('auto')")  
    print("2. Sync continuo: sync.start_continuous_sync()")
    print("3. Solo upload: sync.sync_files('to_render')")
    print("4. Solo download: sync.sync_files('from_render')")
    
    # Test iniziale
    sync.sync_files("auto")
