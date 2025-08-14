# ===== INTEGRAZIONE ANALYSIS TEXT SPLITTER CON 555.PY =====
# Funzioni per integrare la divisione dell'analysis_text.txt nel sistema principale

from analysis_text_splitter import split_and_send_analysis_text, get_analysis_parts_for_manual_send
import datetime
import pytz

def replace_send_analysis_text_message_in_555():
    """
    Funzione sostitutiva per send_analysis_text_message() in 555.py
    Usa il nuovo sistema di divisione in 3 parti
    """
    def new_send_analysis_text_message(now, invia_messaggio_telegram):
        """Nuova implementazione che divide in 3 parti"""
        
        if now is None:
            italy_tz = pytz.timezone('Europe/Rome')
            now = datetime.datetime.now(italy_tz)
        
        print(f"📊 [ANALYSIS-SPLIT] Avvio invio analysis_text.txt diviso in parti - {now.strftime('%H:%M:%S')}")
        
        # Usa il nuovo splitter per inviare in 3 parti
        success = split_and_send_analysis_text(invia_messaggio_telegram, now)
        
        if success:
            print(f"✅ [ANALYSIS-SPLIT] Analysis text inviato con successo in 3 parti alle {now.strftime('%H:%M')}")
        else:
            print(f"❌ [ANALYSIS-SPLIT] Errore nell'invio dell'analysis text alle {now.strftime('%H:%M')}")
            
        return success
    
    return new_send_analysis_text_message


def replace_backtest_manual_send_in_555():
    """
    Funzione sostitutiva per il backtest manuale in 555.py
    Usa il nuovo sistema di divisione per analysis_text.txt
    """
    def new_backtest_manual_send(invia_messaggio_telegram):
        """Nuova implementazione backtest con divisione in parti"""
        import os
        
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        try:
            # Prima invia il messaggio di apertura backtest
            opening_msg = f"🎯 *BACKTEST MANUALE - {now.strftime('%d/%m/%Y %H:%M')}*\n"
            opening_msg += "Avvio analisi completa divisa in parti...\n\n"
            
            if invia_messaggio_telegram(opening_msg):
                print("✅ [BACKTEST-SPLIT] Messaggio di apertura inviato")
                
                # Poi invia l'analysis_text.txt diviso in 3 parti
                success = split_and_send_analysis_text(invia_messaggio_telegram, now)
                
                if success:
                    # Messaggio finale di completamento
                    final_msg = f"🏁 *BACKTEST COMPLETATO*\n"
                    final_msg += f"📊 Analisi completa inviata in 3 parti\n"
                    final_msg += f"🕐 Completato alle {now.strftime('%H:%M')} (Italia)"
                    
                    if invia_messaggio_telegram(final_msg):
                        print("✅ [BACKTEST-SPLIT] Backtest completo inviato con successo")
                        return True
                
                print("❌ [BACKTEST-SPLIT] Errore nell'invio delle parti analysis_text")
                return False
                
        except Exception as e:
            error_msg = f"❌ *BACKTEST MANUALE - ERRORE*\n{now.strftime('%d/%m/%Y %H:%M')}\n\nErrore: {str(e)}"
            invia_messaggio_telegram(error_msg)
            print(f"❌ [BACKTEST-SPLIT] Errore backtest: {e}")
            return False
    
    return new_backtest_manual_send


def replace_unified_report_analysis_section():
    """
    Funzione per sostituire la sezione analysis_text.txt nel report unificato
    Invece di allegare tutto il testo, crea un riferimento alle parti
    """
    def get_unified_analysis_section():
        """Restituisce la sezione analysis per il report unificato"""
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        # Controlla se il file esiste
        import os
        analysis_file = os.path.join('salvataggi', 'analysis_text.txt')
        
        if os.path.exists(analysis_file):
            try:
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if content:
                    # Conta le righe per stimare le parti
                    line_count = len(content.split('\n'))
                    estimated_parts = max(3, (line_count // 25) + 1)  # Stima parti
                    
                    section = f"📊 *SEZIONE 4 - ANALISI TECNICA*\n"
                    section += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    section += f"📄 Analysis text disponibile ({line_count} righe)\n"
                    section += f"📤 Sarà inviato separatamente in ~{estimated_parts} parti\n"
                    section += f"🕐 Ultimo aggiornamento: {now.strftime('%H:%M')}\n"
                    section += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    
                    return section
                else:
                    return "📊 *SEZIONE 4 - ANALISI TECNICA*\n━━━━━━━━━━━━━━━━━━━━━━━━━\n⚠️ File analysis_text.txt vuoto\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    
            except Exception as e:
                return f"📊 *SEZIONE 4 - ANALISI TECNICA*\n━━━━━━━━━━━━━━━━━━━━━━━━━\n❌ Errore lettura file: {str(e)}\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        else:
            return "📊 *SEZIONE 4 - ANALISI TECNICA*\n━━━━━━━━━━━━━━━━━━━━━━━━━\n❌ File analysis_text.txt non trovato\n━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    return get_unified_analysis_section


def create_manual_split_buttons():
    """
    Crea pulsanti per l'invio manuale delle parti dell'analysis_text
    Da integrare nella dashboard Dash
    """
    def send_part_1(invia_messaggio_telegram):
        """Invia solo la parte 1"""
        parts = get_analysis_parts_for_manual_send()
        if parts and len(parts) >= 1:
            return invia_messaggio_telegram(parts[0])
        return False
    
    def send_part_2(invia_messaggio_telegram):
        """Invia solo la parte 2"""
        parts = get_analysis_parts_for_manual_send()
        if parts and len(parts) >= 2:
            return invia_messaggio_telegram(parts[1])
        return False
    
    def send_part_3(invia_messaggio_telegram):
        """Invia solo la parte 3"""
        parts = get_analysis_parts_for_manual_send()
        if parts and len(parts) >= 3:
            return invia_messaggio_telegram(parts[2])
        return False
    
    def send_all_parts(invia_messaggio_telegram):
        """Invia tutte le parti in sequenza"""
        return split_and_send_analysis_text(invia_messaggio_telegram)
    
    return {
        'send_part_1': send_part_1,
        'send_part_2': send_part_2, 
        'send_part_3': send_part_3,
        'send_all_parts': send_all_parts
    }


# === ESEMPIO DI UTILIZZO ===
def example_integration():
    """Esempio di come integrare le nuove funzioni"""
    
    # 1. Sostituire send_analysis_text_message in 555.py
    print("📝 Esempio 1: Sostituire send_analysis_text_message")
    new_function = replace_send_analysis_text_message_in_555()
    print("   ✅ Usa new_function al posto della vecchia send_analysis_text_message")
    
    # 2. Sostituire il backtest manuale
    print("📝 Esempio 2: Sostituire backtest manuale")
    new_backtest = replace_backtest_manual_send_in_555()
    print("   ✅ Usa new_backtest per i pulsanti di backtest manuale")
    
    # 3. Modificare il report unificato
    print("📝 Esempio 3: Report unificato ottimizzato")
    unified_section = replace_unified_report_analysis_section()
    print("   ✅ Usa unified_section() per la sezione 4 del report unificato")
    
    # 4. Pulsanti manuali separati
    print("📝 Esempio 4: Pulsanti per parti separate")
    manual_buttons = create_manual_split_buttons()
    print("   ✅ Usa manual_buttons['send_part_1'] etc. per pulsanti individuali")

if __name__ == "__main__":
    example_integration()
