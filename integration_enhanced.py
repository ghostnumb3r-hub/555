# ===== INTEGRAZIONE ENHANCED PER 555.PY =====
# Sistema adattivo che usa enhanced splitter per file grandi, normale per file piccoli

from analysis_text_splitter_enhanced import (
    EnhancedAnalysisTextSplitter, 
    split_and_send_enhanced_analysis_text,
    get_enhanced_analysis_parts
)
from analysis_text_splitter import (
    AnalysisTextSplitter,
    split_and_send_analysis_text as basic_split_and_send
)
import datetime
import pytz
import os

class AdaptiveAnalysisSplitter:
    """Splitter adattivo che sceglie automaticamente la versione migliore"""
    
    def __init__(self):
        self.italy_tz = pytz.timezone('Europe/Rome')
        self.enhanced_threshold_chars = 3000  # Soglia per usare enhanced
        self.enhanced_threshold_sections = 10  # Soglia sezioni per enhanced
    
    def analyze_file_complexity(self):
        """Analizza il file per decidere quale splitter usare"""
        analysis_file = os.path.join('salvataggi', 'analysis_text.txt')
        
        try:
            if not os.path.exists(analysis_file):
                return "file_not_found", 0, 0
            
            with open(analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return "file_empty", 0, 0
            
            char_count = len(content)
            
            # Conta sezioni approssimativamente
            section_indicators = [
                'ANALISI', 'PREVISIONI', 'CONFRONTO', 'REPORT', 'CALENDARIO',
                'SENTIMENT', 'CORRELAZIONI', 'RACCOMANDAZIONI', 'OUTLOOK',
                'MONITORAGGIO', 'RISCHIO', 'NOTE', 'DISCLAIMER'
            ]
            
            section_count = 0
            for indicator in section_indicators:
                section_count += content.upper().count(indicator)
            
            # Decisione su quale splitter usare
            if char_count >= self.enhanced_threshold_chars or section_count >= self.enhanced_threshold_sections:
                return "use_enhanced", char_count, section_count
            else:
                return "use_basic", char_count, section_count
                
        except Exception as e:
            print(f"❌ [ADAPTIVE] Errore analisi file: {e}")
            return "error", 0, 0
    
    def split_and_send_adaptive(self, send_function, now=None):
        """Divide e invia usando il metodo adattivo migliore"""
        if now is None:
            now = datetime.datetime.now(self.italy_tz)
        
        # Analizza complessità del file
        decision, char_count, section_count = self.analyze_file_complexity()
        
        print(f"🔍 [ADAPTIVE] Analisi file: {char_count} caratteri, ~{section_count} sezioni")
        
        if decision == "file_not_found":
            error_msg = f"❌ *ANALISI TECNICA - {now.strftime('%d/%m/%Y %H:%M')}*\n\nFile analysis_text.txt non trovato."
            send_function(error_msg)
            return False
        
        elif decision == "file_empty":
            error_msg = f"⚠️ *ANALISI TECNICA - {now.strftime('%d/%m/%Y %H:%M')}*\n\nIl file analysis_text.txt è vuoto."
            send_function(error_msg)
            return False
        
        elif decision == "error":
            error_msg = f"❌ *ANALISI TECNICA - {now.strftime('%d/%m/%Y %H:%M')}*\n\nErrore nella lettura del file."
            send_function(error_msg)
            return False
        
        elif decision == "use_enhanced":
            print(f"🚀 [ADAPTIVE] Uso Enhanced Splitter per file complesso ({char_count} char, ~{section_count} sezioni)")
            return split_and_send_enhanced_analysis_text(send_function, now)
        
        elif decision == "use_basic":
            print(f"📊 [ADAPTIVE] Uso Basic Splitter per file semplice ({char_count} char, ~{section_count} sezioni)")
            return basic_split_and_send(send_function, now)
        
        else:
            print(f"❌ [ADAPTIVE] Decisione sconosciuta: {decision}")
            return False

# === FUNZIONI DI SOSTITUZIONE PER 555.PY ===

def replace_send_analysis_text_message_adaptive():
    """Sostituzione adattiva per send_analysis_text_message() in 555.py"""
    def new_send_analysis_text_message(now, invia_messaggio_telegram):
        """Implementazione adattiva che sceglie automaticamente il metodo migliore"""
        
        if now is None:
            italy_tz = pytz.timezone('Europe/Rome')
            now = datetime.datetime.now(italy_tz)
        
        print(f"📊 [ADAPTIVE-ANALYSIS] Avvio invio analysis_text.txt adattivo - {now.strftime('%H:%M:%S')}")
        
        # Usa splitter adattivo
        adaptive_splitter = AdaptiveAnalysisSplitter()
        success = adaptive_splitter.split_and_send_adaptive(invia_messaggio_telegram, now)
        
        if success:
            print(f"✅ [ADAPTIVE-ANALYSIS] Analysis text inviato con successo alle {now.strftime('%H:%M')}")
        else:
            print(f"❌ [ADAPTIVE-ANALYSIS] Errore nell'invio dell'analysis text alle {now.strftime('%H:%M')}")
            
        return success
    
    return new_send_analysis_text_message

def replace_backtest_manual_send_adaptive():
    """Sostituzione adattiva per il backtest manuale in 555.py"""
    def new_backtest_manual_send(invia_messaggio_telegram):
        """Implementazione backtest con splitter adattivo"""
        import os
        
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        try:
            # Messaggio di apertura
            opening_msg = f"🎯 *BACKTEST MANUALE ADATTIVO - {now.strftime('%d/%m/%Y %H:%M')}*\n"
            opening_msg += "Avvio analisi con sistema adattivo intelligente...\n\n"
            
            if invia_messaggio_telegram(opening_msg):
                print("✅ [BACKTEST-ADAPTIVE] Messaggio di apertura inviato")
                
                # Usa splitter adattivo per l'analysis_text.txt
                adaptive_splitter = AdaptiveAnalysisSplitter()
                success = adaptive_splitter.split_and_send_adaptive(invia_messaggio_telegram, now)
                
                if success:
                    # Messaggio finale di completamento
                    final_msg = f"🏁 *BACKTEST ADATTIVO COMPLETATO*\n"
                    final_msg += f"📊 Analisi inviata con sistema intelligente\n"
                    final_msg += f"🕐 Completato alle {now.strftime('%H:%M')} (Italia)"
                    
                    if invia_messaggio_telegram(final_msg):
                        print("✅ [BACKTEST-ADAPTIVE] Backtest completo inviato con successo")
                        return True
                
                print("❌ [BACKTEST-ADAPTIVE] Errore nell'invio dell'analysis text")
                return False
                
        except Exception as e:
            error_msg = f"❌ *BACKTEST MANUALE - ERRORE*\n{now.strftime('%d/%m/%Y %H:%M')}\n\nErrore: {str(e)}"
            invia_messaggio_telegram(error_msg)
            print(f"❌ [BACKTEST-ADAPTIVE] Errore backtest: {e}")
            return False
    
    return new_backtest_manual_send

def replace_unified_report_analysis_section_adaptive():
    """Sostituzione adattiva per la sezione analysis nel report unificato"""
    def get_unified_analysis_section():
        """Sezione analysis per report unificato con info adattiva"""
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        # Usa l'adaptive splitter per analizzare
        adaptive_splitter = AdaptiveAnalysisSplitter()
        decision, char_count, section_count = adaptive_splitter.analyze_file_complexity()
        
        section = f"📊 *SEZIONE 4 - ANALISI TECNICA ADATTIVA*\n"
        section += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if decision == "file_not_found":
            section += f"❌ File analysis_text.txt non trovato\n"
        elif decision == "file_empty":
            section += f"⚠️ File analysis_text.txt vuoto\n"
        elif decision == "error":
            section += f"❌ Errore nella lettura del file\n"
        elif decision in ["use_enhanced", "use_basic"]:
            splitter_type = "Enhanced" if decision == "use_enhanced" else "Basic"
            section += f"📄 Analysis disponibile ({char_count} caratteri)\n"
            section += f"🔧 Sistema: {splitter_type} Splitter (~{section_count} sezioni)\n"
            section += f"📤 Sarà inviato con divisione intelligente\n"
            section += f"🕐 Ultimo aggiornamento: {now.strftime('%H:%M')}\n"
        
        section += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        return section
    
    return get_unified_analysis_section

def create_manual_adaptive_buttons():
    """Crea pulsanti per l'invio manuale con sistema adattivo"""
    def send_adaptive_analysis(invia_messaggio_telegram):
        """Invia analysis con sistema adattivo"""
        adaptive_splitter = AdaptiveAnalysisSplitter()
        return adaptive_splitter.split_and_send_adaptive(invia_messaggio_telegram)
    
    def get_analysis_info(invia_messaggio_telegram):
        """Invia informazioni sul file analysis"""
        adaptive_splitter = AdaptiveAnalysisSplitter()
        decision, char_count, section_count = adaptive_splitter.analyze_file_complexity()
        
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        info_msg = f"🔍 *INFO ANALYSIS TEXT*\n"
        info_msg += f"📅 {now.strftime('%d/%m/%Y %H:%M')} (Ora Italiana)\n\n"
        info_msg += f"📊 Caratteri: {char_count}\n"
        info_msg += f"📄 Sezioni stimate: ~{section_count}\n"
        
        if decision == "use_enhanced":
            info_msg += f"🚀 Modalità: Enhanced Splitter\n"
            info_msg += f"📤 Parti previste: Multiple parti ottimizzate\n"
        elif decision == "use_basic":
            info_msg += f"📊 Modalità: Basic Splitter\n"
            info_msg += f"📤 Parti previste: Poche parti\n"
        else:
            info_msg += f"❌ Stato: {decision}\n"
        
        return invia_messaggio_telegram(info_msg)
    
    return {
        'send_adaptive_analysis': send_adaptive_analysis,
        'get_analysis_info': get_analysis_info
    }

# === ESEMPIO DI UTILIZZO ===
def example_adaptive_integration():
    """Esempio di come integrare il sistema adattivo"""
    print("📝 Esempio Integrazione Adattiva:")
    print("   ✅ Sistema che si adatta automaticamente alla complessità del file")
    print("   🔄 File piccoli (<3000 char, <10 sezioni) → Basic Splitter")
    print("   🚀 File grandi (≥3000 char, ≥10 sezioni) → Enhanced Splitter")
    print("   🎯 Decisioni intelligenti basate su contenuto reale")

if __name__ == "__main__":
    # Test del sistema adattivo
    def mock_send(msg):
        print(f"📤 ADAPTIVE MOCK: {len(msg)} caratteri")
        return True
    
    adaptive_splitter = AdaptiveAnalysisSplitter()
    print("🧪 [TEST] Testing Adaptive Analysis Splitter...")
    
    decision, chars, sections = adaptive_splitter.analyze_file_complexity()
    print(f"🔍 Decisione: {decision} ({chars} caratteri, ~{sections} sezioni)")
    
    success = adaptive_splitter.split_and_send_adaptive(mock_send)
    print(f"🧪 [TEST] Risultato Adattivo: {'✅ Successo' if success else '❌ Fallito'}")
    
    example_adaptive_integration()
