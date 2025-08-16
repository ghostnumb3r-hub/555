#!/usr/bin/env python3
"""
Configurazione per il salvataggio di file su Google Drive
"""
import os
from pathlib import Path

# Percorso base di Google Drive (sia locale che drive diretto)
DRIVE_LOCAL_PATH = Path("C:/Users/valen/555")
DRIVE_CLOUD_PATH = Path("H:/Il mio Drive/555")

# Directory per i render
RENDERS_DIR = "renders"

# Percorsi completi per i render
RENDERS_LOCAL = DRIVE_LOCAL_PATH / RENDERS_DIR
RENDERS_CLOUD = DRIVE_CLOUD_PATH / RENDERS_DIR

# Sottocartelle per tipologie diverse
RENDER_FOLDERS = {
    'images': 'images',        # Screenshot, grafici, immagini generate
    'videos': 'videos',        # Registrazioni video, animazioni video
    'animations': 'animations', # GIF, animazioni procedurali
    'plots': 'plots',          # Grafici matplotlib, seaborn, plotly
    'exports': 'exports'       # File esportati, dump dati, report
}

def get_render_path(folder_type='exports', use_cloud=True):
    """
    Ottiene il percorso completo per salvare un file di render
    
    Args:
        folder_type (str): Tipo di cartella ('images', 'videos', 'animations', 'plots', 'exports')
        use_cloud (bool): Se True usa il percorso cloud H:\, altrimenti locale C:\
    
    Returns:
        Path: Percorso completo della cartella
    """
    base_path = RENDERS_CLOUD if use_cloud else RENDERS_LOCAL
    
    if folder_type not in RENDER_FOLDERS:
        folder_type = 'exports'  # Default fallback
    
    folder_path = base_path / RENDER_FOLDERS[folder_type]
    
    # Crea la cartella se non esiste
    folder_path.mkdir(parents=True, exist_ok=True)
    
    return folder_path

def save_to_drive(content, filename, folder_type='exports', use_cloud=True):
    """
    Salva un file nella cartella renders su Google Drive
    
    Args:
        content: Contenuto del file (string o bytes)
        filename (str): Nome del file
        folder_type (str): Tipo di cartella di destinazione
        use_cloud (bool): Se True salva su H:\, altrimenti su C:\
    
    Returns:
        Path: Percorso completo del file salvato
    """
    folder_path = get_render_path(folder_type, use_cloud)
    file_path = folder_path / filename
    
    # Determina il modo di apertura del file
    mode = 'wb' if isinstance(content, bytes) else 'w'
    encoding = None if isinstance(content, bytes) else 'utf-8'
    
    # Salva il file
    with open(file_path, mode, encoding=encoding) as f:
        f.write(content)
    
    print(f"✅ File salvato: {file_path}")
    return file_path

def get_timestamp_filename(base_name, extension, include_date=True):
    """
    Genera un nome file con timestamp
    
    Args:
        base_name (str): Nome base del file
        extension (str): Estensione del file (con o senza punto)
        include_date (bool): Se includere la data nel nome
    
    Returns:
        str: Nome file con timestamp
    """
    import datetime
    
    # Assicura che l'estensione inizi con un punto
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Crea timestamp
    now = datetime.datetime.now()
    if include_date:
        timestamp = now.strftime('%Y%m%d_%H%M%S')
    else:
        timestamp = now.strftime('%H%M%S')
    
    return f"{base_name}_{timestamp}{extension}"

# Esempi di utilizzo:
if __name__ == "__main__":
    # Test delle funzioni
    print("Percorsi configurati:")
    print(f"Locale: {RENDERS_LOCAL}")
    print(f"Cloud: {RENDERS_CLOUD}")
    
    print("\nCartelle disponibili:")
    for key, folder in RENDER_FOLDERS.items():
        path = get_render_path(key, use_cloud=True)
        print(f"  {key}: {path}")
    
    # Test salvataggio file di esempio
    test_content = "Test file salvato su Google Drive"
    test_filename = get_timestamp_filename("test", "txt")
    save_to_drive(test_content, test_filename, 'exports', use_cloud=True)
