# ===== ANALYSIS TEXT SPLITTER - DIVISIONE IN 3 PARTI =====
# Divide analysis_text.txt in parti ottimizzate per Telegram

import os
import datetime
import pytz
import time
from typing import List, Dict, Tuple, Optional

class AnalysisTextSplitter:
    """Gestisce la divisione del file analysis_text.txt in parti ottimizzate"""
    
    def __init__(self, base_dir: str = "salvataggi"):
        self.base_dir = base_dir
        self.input_file = os.path.join(base_dir, "analysis_text.txt")
        self.timezone = pytz.timezone('Europe/Rome')  # Timezone italiana unificata
        
    def read_analysis_file(self) -> Optional[List[str]]:
        """Legge il file analysis_text.txt e restituisce le righe"""
        try:
            if not os.path.exists(self.input_file):
                print(f"❌ [SPLITTER] File {self.input_file} non trovato")
                return None
                
            with open(self.input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if not lines:
                print(f"⚠️ [SPLITTER] File {self.input_file} vuoto")
                return None
                
            print(f"✅ [SPLITTER] Letto file con {len(lines)} righe")
            return lines
            
        except Exception as e:
            print(f"❌ [SPLITTER] Errore lettura file: {e}")
            return None
    
    def identify_sections(self, lines: List[str]) -> Dict[str, Tuple[int, int]]:
        """Identifica le sezioni principali del file e i loro range di righe"""
        sections = {}
        current_section = None
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Identifica le sezioni principali
            if "BACKTEST ANALYZER" in line_clean or "ANALISI COMPLETA" in line_clean:
                sections["header"] = (0, i + 3)  # Include separatore
                
            elif "ANALISI SEGNALI TECNICI" in line_clean:
                current_section = "technical"
                sections["technical_start"] = i
                
            elif "ANALISI PREVISIONI MACHINE LEARNING" in line_clean:
                if "technical_start" in sections:
                    sections["technical"] = (sections["technical_start"], i - 1)
                current_section = "ml"
                sections["ml_start"] = i
                
            elif "CONFRONTO SEGNALI" in line_clean:
                if "ml_start" in sections:
                    sections["ml"] = (sections["ml_start"], i - 1)
                current_section = "comparison"
                sections["comparison_start"] = i
                
            elif "REPORT RIASSUNTIVO" in line_clean:
                if "comparison_start" in sections:
                    sections["comparison"] = (sections["comparison_start"], i - 1)
                current_section = "summary"
                sections["summary_start"] = i
        
        # Completa l'ultima sezione
        if "summary_start" in sections:
            sections["summary"] = (sections["summary_start"], len(lines) - 1)
            
        return sections
    
    def create_part_1(self, lines: List[str], sections: Dict[str, Tuple[int, int]]) -> str:
        """Crea la Parte 1: Header + Analisi Segnali Tecnici"""
        now = datetime.datetime.now(self.timezone)
        
        content = []
        content.append(f"📊 *ANALISI TECNICA - PARTE 1/3*")
        content.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)")
        content.append("=" * 50)
        content.append("")
        
        # Aggiungi header se disponibile
        if "header" in sections:
            start, end = sections["header"]
            for line in lines[start:end + 1]:
                content.append(line.rstrip())
        
        # Aggiungi analisi tecnica
        if "technical" in sections:
            start, end = sections["technical"]
            for line in lines[start:end + 1]:
                content.append(line.rstrip())
        
        content.append("")
        content.append("➡️ *Continua nella Parte 2/3: Machine Learning*")
        
        return "\n".join(content)
    
    def create_part_2(self, lines: List[str], sections: Dict[str, Tuple[int, int]]) -> str:
        """Crea la Parte 2: Machine Learning + Confronto Segnali"""
        now = datetime.datetime.now(self.timezone)
        
        content = []
        content.append(f"🤖 *ANALISI ML - PARTE 2/3*")
        content.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)")
        content.append("=" * 50)
        content.append("")
        
        # Aggiungi analisi ML
        if "ml" in sections:
            start, end = sections["ml"]
            for line in lines[start:end + 1]:
                content.append(line.rstrip())
        
        content.append("")
        
        # Aggiungi confronto segnali
        if "comparison" in sections:
            start, end = sections["comparison"]
            for line in lines[start:end + 1]:
                content.append(line.rstrip())
        
        content.append("")
        content.append("➡️ *Continua nella Parte 3/3: Report Finale*")
        
        return "\n".join(content)
    
    def create_part_3(self, lines: List[str], sections: Dict[str, Tuple[int, int]]) -> str:
        """Crea la Parte 3: Report Riassuntivo + Note"""
        now = datetime.datetime.now(self.timezone)
        
        content = []
        content.append(f"📋 *REPORT FINALE - PARTE 3/3*")
        content.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)")
        content.append("=" * 50)
        content.append("")
        
        # Aggiungi report riassuntivo
        if "summary" in sections:
            start, end = sections["summary"]
            for line in lines[start:end + 1]:
                content.append(line.rstrip())
        
        content.append("")
        content.append("✅ *Analisi completa inviata in 3 parti*")
        content.append(f"🕐 Generata alle {now.strftime('%H:%M')} (Italia)")
        
        return "\n".join(content)
    
    def split_analysis_text(self) -> Optional[List[str]]:
        """Divide il file analysis_text.txt in 3 parti e restituisce i contenuti"""
        lines = self.read_analysis_file()
        if not lines:
            return None
            
        sections = self.identify_sections(lines)
        
        if not sections:
            print("⚠️ [SPLITTER] Nessuna sezione identificata, invio file integrale")
            # Fallback: dividi semplicemente per lunghezza
            return self.split_by_length(lines)
        
        parts = []
        parts.append(self.create_part_1(lines, sections))
        parts.append(self.create_part_2(lines, sections))
        parts.append(self.create_part_3(lines, sections))
        
        print(f"✅ [SPLITTER] File diviso in {len(parts)} parti")
        for i, part in enumerate(parts, 1):
            print(f"   Parte {i}: {len(part)} caratteri")
            
        return parts
    
    def split_by_length(self, lines: List[str], max_chars: int = 3500) -> List[str]:
        """Fallback: divide il file per lunghezza massima caratteri"""
        all_text = "\n".join(line.rstrip() for line in lines)
        parts = []
        
        now = datetime.datetime.now(self.timezone)
        
        # Divide il testo in parti
        while len(all_text) > max_chars:
            # Trova l'ultimo '\n' prima del limite
            cut_point = all_text.rfind('\n', 0, max_chars)
            if cut_point == -1:
                cut_point = max_chars
            
            part_content = all_text[:cut_point]
            part_number = len(parts) + 1
            
            # Aggiungi header alla parte
            header = f"📊 *ANALISI TECNICA - PARTE {part_number}*\n"
            header += f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)\n"
            header += "=" * 50 + "\n\n"
            
            parts.append(header + part_content)
            all_text = all_text[cut_point:].lstrip()
        
        # Aggiungi l'ultima parte se c'è contenuto rimanente
        if all_text.strip():
            part_number = len(parts) + 1
            header = f"📊 *ANALISI TECNICA - PARTE {part_number} (FINALE)*\n"
            header += f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)\n"
            header += "=" * 50 + "\n\n"
            
            parts.append(header + all_text)
        
        return parts
    
    def save_parts_to_files(self, parts: List[str]) -> List[str]:
        """Salva le parti in file separati e restituisce i percorsi"""
        file_paths = []
        
        for i, part in enumerate(parts, 1):
            filename = f"analysis_text_part_{i}.txt"
            filepath = os.path.join(self.base_dir, filename)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(part)
                file_paths.append(filepath)
                print(f"✅ [SPLITTER] Salvata parte {i} in {filename}")
            except Exception as e:
                print(f"❌ [SPLITTER] Errore salvataggio parte {i}: {e}")
                
        return file_paths

# === FUNZIONI DI UTILITÀ PER INTEGRAZIONE CON 555.PY ===

def split_and_send_analysis_text(send_function, now=None):
    """Divide e invia analysis_text.txt in 3 parti usando la funzione di invio fornita"""
    if now is None:
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
    
    splitter = AnalysisTextSplitter()
    parts = splitter.split_analysis_text()
    
    if not parts:
        print("❌ [SPLITTER] Impossibile dividere il file analysis_text.txt")
        return False
    
    success_count = 0
    total_parts = len(parts)
    
    for i, part in enumerate(parts, 1):
        print(f"📤 [SPLITTER] Invio parte {i}/{total_parts}...")
        
        # Breve pausa tra i messaggi per evitare rate limiting
        if i > 1:
            time.sleep(2)
        
        if send_function(part):
            success_count += 1
            print(f"✅ [SPLITTER] Parte {i}/{total_parts} inviata con successo")
        else:
            print(f"❌ [SPLITTER] Errore invio parte {i}/{total_parts}")
    
    if success_count == total_parts:
        print(f"🎉 [SPLITTER] Tutte le {total_parts} parti inviate con successo!")
        return True
    else:
        print(f"⚠️ [SPLITTER] Inviate {success_count}/{total_parts} parti")
        return False

def get_analysis_parts_for_manual_send():
    """Restituisce le parti dell'analisi per invio manuale"""
    splitter = AnalysisTextSplitter()
    parts = splitter.split_analysis_text()
    return parts if parts else []

# === TEST FUNCTION ===
if __name__ == "__main__":
    import time
    
    def mock_send_function(message):
        """Funzione di test per simulare l'invio"""
        print(f"📤 MOCK SEND: {len(message)} caratteri")
        print("=" * 50)
        print(message[:200] + "..." if len(message) > 200 else message)
        print("=" * 50)
        return True
    
    print("🧪 [TEST] Testing Analysis Text Splitter...")
    success = split_and_send_analysis_text(mock_send_function)
    print(f"🧪 [TEST] Risultato: {'✅ Successo' if success else '❌ Fallito'}")
