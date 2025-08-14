# ===== ANALYSIS TEXT SPLITTER ENHANCED - DIVISIONE INTELLIGENTE =====
# Gestisce file analysis_text.txt con 14 sezioni e 4000+ caratteri

import os
import datetime
import pytz
import time
import re
from typing import List, Dict, Tuple, Optional

class EnhancedAnalysisTextSplitter:
    """Gestisce la divisione intelligente del file analysis_text.txt enhanced"""
    
    def __init__(self, base_dir: str = "salvataggi"):
        self.base_dir = base_dir
        self.input_file = os.path.join(base_dir, "analysis_text.txt")
        self.timezone = pytz.timezone('Europe/Rome')  # Timezone italiana unificata
        self.max_chars_per_part = 3800  # Limite sicuro per Telegram
        
    def read_analysis_file(self) -> Optional[List[str]]:
        """Legge il file analysis_text.txt e restituisce le righe"""
        try:
            if not os.path.exists(self.input_file):
                print(f"❌ [ENHANCED-SPLITTER] File {self.input_file} non trovato")
                return None
                
            with open(self.input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if not lines:
                print(f"⚠️ [ENHANCED-SPLITTER] File {self.input_file} vuoto")
                return None
                
            print(f"✅ [ENHANCED-SPLITTER] Letto file con {len(lines)} righe")
            return lines
            
        except Exception as e:
            print(f"❌ [ENHANCED-SPLITTER] Errore lettura file: {e}")
            return None
    
    def identify_enhanced_sections(self, lines: List[str]) -> List[Dict]:
        """Identifica tutte le sezioni del file enhanced (14+ sezioni)"""
        sections = []
        current_section = None
        start_line = 0
        
        # Pattern per identificare le sezioni principali
        section_patterns = [
            # Sezioni originali
            (r"BACKTEST ANALYZER|ANALISI COMPLETA", "header", "🎯"),
            (r"ANALISI SEGNALI TECNICI", "technical_signals", "📊"),
            (r"ANALISI PREVISIONI MACHINE LEARNING|ANALISI ML", "ml_predictions", "🤖"),
            (r"CONFRONTO SEGNALI", "signal_comparison", "⚖️"),
            (r"REPORT RIASSUNTIVO", "summary_report", "📋"),
            
            # Sezioni enhanced aggiuntive
            (r"CALENDARIO ECONOMICO|EVENTI ECONOMICI", "economic_calendar", "📅"),
            (r"ANALISI SENTIMENT|NEWS SENTIMENT", "news_sentiment", "📰"),
            (r"CORRELAZIONI.*ASSET|CROSS.*ASSET", "correlations", "🔗"),
            (r"RACCOMANDAZIONI.*ML|ML.*RACCOMANDAZIONI", "ml_recommendations", "💡"),
            (r"OUTLOOK.*SETTIMANALE|WEEKLY.*OUTLOOK", "weekly_outlook", "📈"),
            (r"MONITORAGGIO.*MERCATI|MARKET.*MONITORING", "market_monitoring", "🚨"),
            (r"GESTIONE.*RISCHIO|RISK.*MANAGEMENT", "risk_management", "⚡"),
            (r"NOTE.*TECNICHE|TECHNICAL.*NOTES", "technical_notes", "💻"),
            (r"DISCLAIMER|AVVERTENZE", "disclaimer", "⚠️")
        ]
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Cerca pattern di sezione
            for pattern, section_type, emoji in section_patterns:
                if re.search(pattern, line_clean, re.IGNORECASE):
                    # Salva la sezione precedente se esiste
                    if current_section is not None:
                        current_section["end_line"] = i - 1
                        sections.append(current_section)
                    
                    # Inizia nuova sezione
                    current_section = {
                        "type": section_type,
                        "emoji": emoji,
                        "title": line_clean,
                        "start_line": i,
                        "end_line": None
                    }
                    break
        
        # Completa l'ultima sezione
        if current_section is not None:
            current_section["end_line"] = len(lines) - 1
            sections.append(current_section)
        
        print(f"✅ [ENHANCED-SPLITTER] Identificate {len(sections)} sezioni")
        for section in sections:
            line_count = section["end_line"] - section["start_line"] + 1
            print(f"   {section['emoji']} {section['type']}: righe {section['start_line']}-{section['end_line']} ({line_count} righe)")
        
        return sections
    
    def calculate_optimal_parts(self, lines: List[str], sections: List[Dict]) -> List[List[Dict]]:
        """Calcola la divisione ottimale in parti basata sulla lunghezza"""
        if not sections:
            # Fallback: divisione per lunghezza
            return self.fallback_length_division(lines)
        
        # Calcola dimensioni delle sezioni
        for section in sections:
            start, end = section["start_line"], section["end_line"]
            section_text = "\n".join(lines[start:end + 1])
            section["char_count"] = len(section_text)
            section["text"] = section_text
        
        # Raggruppa sezioni in parti ottimali
        parts = []
        current_part = []
        current_chars = 0
        
        for section in sections:
            section_chars = section["char_count"]
            
            # Se aggiungere questa sezione supera il limite
            if current_chars + section_chars > self.max_chars_per_part and current_part:
                # Salva parte corrente e inizia nuova parte
                parts.append(current_part)
                current_part = [section]
                current_chars = section_chars
            else:
                # Aggiungi sezione alla parte corrente
                current_part.append(section)
                current_chars += section_chars
        
        # Aggiungi l'ultima parte se non vuota
        if current_part:
            parts.append(current_part)
        
        print(f"✅ [ENHANCED-SPLITTER] File diviso in {len(parts)} parti ottimali")
        for i, part in enumerate(parts, 1):
            total_chars = sum(s["char_count"] for s in part)
            section_names = [s["type"] for s in part]
            print(f"   Parte {i}: {total_chars} caratteri, sezioni: {section_names}")
        
        return parts
    
    def create_enhanced_part(self, part_sections: List[Dict], part_number: int, total_parts: int) -> str:
        """Crea una parte con header enhanced e contenuto ottimizzato"""
        now = datetime.datetime.now(self.timezone)
        
        content = []
        
        # Header della parte
        part_emojis = [s["emoji"] for s in part_sections[:3]]  # Prime 3 emoji come identificativo
        emoji_string = "".join(part_emojis) if part_emojis else "📊"
        
        content.append(f"{emoji_string} *ANALISI COMPLETA - PARTE {part_number}/{total_parts}*")
        content.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)")
        content.append("=" * 50)
        content.append("")
        
        # Aggiungi tutte le sezioni della parte
        for section in part_sections:
            content.append(section["text"])
            content.append("")  # Spazio tra sezioni
        
        # Footer della parte
        if part_number < total_parts:
            content.append(f"➡️ *Continua nella Parte {part_number + 1}/{total_parts}*")
        else:
            content.append(f"✅ *Analisi completa - Parte finale {part_number}/{total_parts}*")
            content.append(f"🕐 Completata alle {now.strftime('%H:%M')} (Italia)")
        
        return "\n".join(content)
    
    def fallback_length_division(self, lines: List[str]) -> List[List[Dict]]:
        """Fallback: divisione semplice per lunghezza se non trova sezioni"""
        all_text = "\n".join(line.rstrip() for line in lines)
        parts = []
        
        while len(all_text) > self.max_chars_per_part:
            # Trova punto di taglio ottimale
            cut_point = all_text.rfind('\n', 0, self.max_chars_per_part)
            if cut_point == -1:
                cut_point = self.max_chars_per_part
            
            part_text = all_text[:cut_point]
            fake_section = {
                "type": f"fallback_part_{len(parts) + 1}",
                "emoji": "📄",
                "title": f"Sezione {len(parts) + 1}",
                "start_line": 0,
                "end_line": len(part_text.split('\n')) - 1,
                "char_count": len(part_text),
                "text": part_text
            }
            parts.append([fake_section])
            all_text = all_text[cut_point:].lstrip()
        
        # Ultima parte
        if all_text.strip():
            fake_section = {
                "type": f"fallback_part_{len(parts) + 1}",
                "emoji": "📄",
                "title": f"Sezione finale",
                "start_line": 0,
                "end_line": len(all_text.split('\n')) - 1,
                "char_count": len(all_text),
                "text": all_text
            }
            parts.append([fake_section])
        
        print(f"⚠️ [ENHANCED-SPLITTER] Usato fallback: {len(parts)} parti per lunghezza")
        return parts
    
    def split_enhanced_analysis_text(self) -> Optional[List[str]]:
        """Divide il file enhanced in parti ottimali e restituisce i contenuti"""
        lines = self.read_analysis_file()
        if not lines:
            return None
        
        # Identifica sezioni enhanced
        sections = self.identify_enhanced_sections(lines)
        
        # Calcola divisione ottimale
        parts_sections = self.calculate_optimal_parts(lines, sections)
        
        # Crea contenuto delle parti
        final_parts = []
        total_parts = len(parts_sections)
        
        for i, part_sections in enumerate(parts_sections, 1):
            part_content = self.create_enhanced_part(part_sections, i, total_parts)
            final_parts.append(part_content)
        
        # Statistiche finali
        total_chars = sum(len(part) for part in final_parts)
        avg_chars = total_chars // len(final_parts) if final_parts else 0
        
        print(f"🎉 [ENHANCED-SPLITTER] Divisione completata:")
        print(f"   📊 Parti totali: {len(final_parts)}")
        print(f"   📈 Caratteri totali: {total_chars}")
        print(f"   📉 Media per parte: {avg_chars}")
        
        for i, part in enumerate(final_parts, 1):
            print(f"   📄 Parte {i}: {len(part)} caratteri")
        
        return final_parts

# === FUNZIONI DI UTILITÀ ENHANCED ===

def split_and_send_enhanced_analysis_text(send_function, now=None):
    """Divide e invia analysis_text.txt enhanced usando la divisione intelligente"""
    if now is None:
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
    
    splitter = EnhancedAnalysisTextSplitter()
    parts = splitter.split_enhanced_analysis_text()
    
    if not parts:
        print("❌ [ENHANCED-SPLITTER] Impossibile dividere il file analysis_text.txt")
        return False
    
    success_count = 0
    total_parts = len(parts)
    
    # Messaggio di inizio invio
    intro_msg = f"🚀 *INVIO ANALISI COMPLETA ENHANCED*\n"
    intro_msg += f"📊 Invio in corso di {total_parts} parti ottimizzate...\n"
    intro_msg += f"⏰ {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)"
    
    if send_function(intro_msg):
        print("✅ [ENHANCED-SPLITTER] Messaggio di introduzione inviato")
        time.sleep(1)  # Breve pausa
    
    for i, part in enumerate(parts, 1):
        print(f"📤 [ENHANCED-SPLITTER] Invio parte {i}/{total_parts}...")
        
        # Pausa tra messaggi per evitare rate limiting
        if i > 1:
            time.sleep(2)
        
        if send_function(part):
            success_count += 1
            print(f"✅ [ENHANCED-SPLITTER] Parte {i}/{total_parts} inviata con successo")
        else:
            print(f"❌ [ENHANCED-SPLITTER] Errore invio parte {i}/{total_parts}")
    
    # Messaggio finale
    if success_count == total_parts:
        final_msg = f"🎉 *ANALISI COMPLETA INVIATA*\n"
        final_msg += f"✅ Tutte le {total_parts} parti inviate con successo\n"
        final_msg += f"🕐 Completato alle {now.strftime('%H:%M')} (Italia)"
        send_function(final_msg)
        
        print(f"🎊 [ENHANCED-SPLITTER] Tutte le {total_parts} parti inviate con successo!")
        return True
    else:
        error_msg = f"⚠️ *INVIO PARZIALE*\n"
        error_msg += f"📤 Inviate {success_count}/{total_parts} parti\n"
        error_msg += f"❌ {total_parts - success_count} parti fallite"
        send_function(error_msg)
        
        print(f"⚠️ [ENHANCED-SPLITTER] Inviate {success_count}/{total_parts} parti")
        return False

def get_enhanced_analysis_parts():
    """Restituisce le parti dell'analisi enhanced per invio manuale"""
    splitter = EnhancedAnalysisTextSplitter()
    parts = splitter.split_enhanced_analysis_text()
    return parts if parts else []

# === TEST FUNCTION ENHANCED ===
if __name__ == "__main__":
    def mock_send_function(message):
        """Funzione di test per simulare l'invio enhanced"""
        print(f"📤 ENHANCED MOCK SEND: {len(message)} caratteri")
        print("=" * 60)
        print(message[:300] + "..." if len(message) > 300 else message)
        print("=" * 60)
        return True
    
    print("🧪 [TEST] Testing Enhanced Analysis Text Splitter...")
    success = split_and_send_enhanced_analysis_text(mock_send_function)
    print(f"🧪 [TEST] Risultato Enhanced: {'✅ Successo' if success else '❌ Fallito'}")
