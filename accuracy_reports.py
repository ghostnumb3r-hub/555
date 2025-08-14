#!/usr/bin/env python3
"""
🎯 Accuracy Reports Generator - Report automatizzati per valutare raccomandazioni

Genera report settimanali e mensili sull'accuratezza delle raccomandazioni.
Può essere eseguito manualmente o schedulato come task automatico.

Usage:
    python accuracy_reports.py --weekly
    python accuracy_reports.py --monthly  
    python accuracy_reports.py --custom 14  # ultimi 14 giorni
"""

import argparse
import datetime
import pandas as pd
from pathlib import Path
from recommendation_tracker import RecommendationTracker
import sys

def generate_detailed_report(tracker, days_back, report_type="Custom"):
    """Genera un report dettagliato di accuracy"""
    
    print(f"\n🎯 === ACCURACY REPORT {report_type.upper()} ({days_back} giorni) ===")
    print(f"📅 Generato il: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Calcola accuracy
    report = tracker.calculate_accuracy_report(days_back)
    
    if report is None:
        print("⚠️  Nessun dato sufficiente per generare il report.")
        print(f"💡 Servono almeno {days_back} giorni di dati storici per la valutazione.")
        return None
    
    # Statistiche generali
    print(f"\n📊 STATISTICHE GENERALI:")
    print(f"   📈 Periodo analizzato: {days_back} giorni")
    print(f"   🎯 Totale raccomandazioni: {report['totale_raccomandazioni']}")
    print(f"   ✅ Raccomandazioni corrette: {report['raccomandazioni_corrette']}")
    print(f"   🎯 Accuracy complessiva: {report['accuracy_percentuale']:.1f}%")
    
    # Valutazione performance
    accuracy_pct = report['accuracy_percentuale']
    if accuracy_pct >= 70:
        performance_rating = "🟢 ECCELLENTE"
        performance_comment = "Il sistema sta fornendo raccomandazioni molto affidabili!"
    elif accuracy_pct >= 60:
        performance_rating = "🟡 BUONA"
        performance_comment = "Performance solida, con margine di miglioramento."
    elif accuracy_pct >= 50:
        performance_rating = "🟠 MEDIA"
        performance_comment = "Performance nella media, necessari aggiustamenti."
    else:
        performance_rating = "🔴 DA MIGLIORARE"
        performance_comment = "Il sistema ha bisogno di calibrazione significativa."
    
    print(f"\n🎖️  VALUTAZIONE: {performance_rating}")
    print(f"💬 {performance_comment}")
    
    # Dettaglio per asset (se disponibile)
    if 'dettaglio_per_asset' in report and report['dettaglio_per_asset']:
        print(f"\n📊 BREAKDOWN PER ASSET:")
        for asset, stats in report['dettaglio_per_asset']['count'].items():
            total_asset = stats
            correct_asset = report['dettaglio_per_asset']['sum'].get(asset, 0)
            asset_accuracy = (correct_asset / total_asset) * 100 if total_asset > 0 else 0
            
            print(f"   • {asset}: {correct_asset}/{total_asset} ({asset_accuracy:.1f}%)")
    
    return report

def save_report_to_file(report, days_back, report_type):
    """Salva il report su file"""
    if report is None:
        return
    
    # Crea directory reports se non esiste
    reports_dir = Path("salvataggiwallet") / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Nome file con timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"accuracy_report_{report_type.lower()}_{days_back}d_{timestamp}.txt"
    filepath = reports_dir / filename
    
    # Scrive report su file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"🎯 ACCURACY REPORT {report_type.upper()}\n")
        f.write(f"Periodo: {days_back} giorni\n")
        f.write(f"Generato: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("📊 STATISTICHE:\n")
        f.write(f"   Totale raccomandazioni: {report['totale_raccomandazioni']}\n")
        f.write(f"   Raccomandazioni corrette: {report['raccomandazioni_corrette']}\n") 
        f.write(f"   Accuracy: {report['accuracy_percentuale']:.1f}%\n\n")
        
        # Valutazione
        accuracy_pct = report['accuracy_percentuale']
        if accuracy_pct >= 70:
            rating = "ECCELLENTE"
        elif accuracy_pct >= 60:
            rating = "BUONA"
        elif accuracy_pct >= 50:
            rating = "MEDIA"
        else:
            rating = "DA MIGLIORARE"
        
        f.write(f"🎖️  VALUTAZIONE: {rating}\n")
        f.write(f"📅 Data report: {report['date']}\n")
    
    print(f"\n💾 Report salvato in: {filepath}")
    
def check_data_availability(tracker, days_back):
    """Verifica se ci sono abbastanza dati storici"""
    if not tracker.recommendations_file.exists():
        print("❌ Nessun dato di raccomandazioni trovato.")
        print("💡 Esegui prima wallet.py e clicca 'Aggiorna Dati' per iniziare il tracking.")
        return False
    
    if not tracker.performance_file.exists():
        print("❌ Nessun dato di performance trovato.")
        return False
        
    # Controlla se ci sono dati recenti
    try:
        df_rec = pd.read_csv(tracker.recommendations_file)
        if df_rec.empty:
            print("❌ File raccomandazioni vuoto.")
            return False
            
        df_rec['timestamp'] = pd.to_datetime(df_rec['timestamp'])
        oldest_data = df_rec['timestamp'].min()
        days_available = (datetime.datetime.now() - oldest_data).days
        
        print(f"📊 Dati disponibili da: {oldest_data.strftime('%d/%m/%Y')}")
        print(f"📊 Giorni di storico: {days_available}")
        
        if days_available < days_back:
            print(f"⚠️  Servono almeno {days_back} giorni di dati per questo report.")
            print(f"💡 Attualmente hai {days_available} giorni di storico.")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Errore nel controllo dati: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Genera report accuracy raccomandazioni")
    parser.add_argument('--weekly', action='store_true', help='Report settimanale (7 giorni)')
    parser.add_argument('--monthly', action='store_true', help='Report mensile (30 giorni)')
    parser.add_argument('--custom', type=int, metavar='DAYS', help='Report personalizzato (n giorni)')
    parser.add_argument('--save', action='store_true', help='Salva report su file')
    parser.add_argument('--check', action='store_true', help='Controlla solo disponibilità dati')
    
    args = parser.parse_args()
    
    # Inizializza tracker
    print("📊 Inizializzazione RecommendationTracker...")
    tracker = RecommendationTracker()
    
    # Solo check dei dati
    if args.check:
        print("\n🔍 CONTROLLO DISPONIBILITA' DATI:")
        for days in [7, 14, 30]:
            print(f"\n📅 {days} giorni:")
            check_data_availability(tracker, days)
        return
    
    # Determina il tipo di report
    if args.weekly:
        days_back = 7
        report_type = "Weekly"
    elif args.monthly:
        days_back = 30
        report_type = "Monthly"
    elif args.custom:
        days_back = args.custom
        report_type = "Custom"
    else:
        # Default: report settimanale
        days_back = 7
        report_type = "Weekly"
        print("💡 Nessun parametro specificato, generando report settimanale.")
    
    # Controlla disponibilità dati
    if not check_data_availability(tracker, days_back):
        print("\n❌ Impossibile generare il report per mancanza di dati storici.")
        sys.exit(1)
    
    # Genera report
    print(f"\n🚀 Generazione report {report_type} ({days_back} giorni)...")
    report = generate_detailed_report(tracker, days_back, report_type)
    
    # Salva su file se richiesto
    if args.save and report:
        save_report_to_file(report, days_back, report_type)
    
    print("\n✅ Report completato!")

if __name__ == "__main__":
    main()
