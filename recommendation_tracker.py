"""
📊 Recommendation Tracker - Sistema di valutazione accuracy raccomandazioni

Salva tutte le raccomandazioni storiche e calcola l'accuratezza settimanale/mensile
"""

import pandas as pd
import datetime
import os
import json
from pathlib import Path

class RecommendationTracker:
    """Tracker per valutare l'accuratezza delle raccomandazioni nel tempo"""
    
    def __init__(self, base_path="salvataggiwallet"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # File paths
        self.recommendations_file = self.base_path / "raccomandazioni_storiche.csv"
        self.performance_file = self.base_path / "performance_storiche.csv" 
        self.accuracy_file = self.base_path / "accuracy_reports.csv"
        
        print(f"📊 RecommendationTracker inizializzato in: {self.base_path}")
    
    def save_current_recommendations(self, recommendations_data, portfolio_data, market_data):
        """Salva le raccomandazioni attuali con timestamp"""
        timestamp = datetime.datetime.now()
        
        # Prepara i dati da salvare
        records = []
        for rec in recommendations_data:
            record = {
                'timestamp': timestamp,
                'date': timestamp.strftime('%Y-%m-%d'),
                'time': timestamp.strftime('%H:%M:%S'),
                'asset': rec.get('Asset', '').replace('🟠 ', '').replace('💵 ', '').replace('🥇 ', '').replace('📈 ', ''),
                'segnale': rec.get('Segnale', ''),
                'azione': rec.get('Azione', ''),
                'motivazione': rec.get('Motivazione', ''),
                'esposizione_attuale': rec.get('Esposizione Attuale', ''),
                'target_ideale': rec.get('Ribilanciamento Ideale', ''),
                'performance_1w': rec.get('Performance 1W', ''),
                'ml_probability': rec.get('ML Probability', ''),
                'categoria': rec.get('Categoria', ''),
                'rischio': rec.get('Rischio', '')
            }
            records.append(record)
        
        # Salva su CSV
        df_new = pd.DataFrame(records)
        
        if self.recommendations_file.exists():
            df_existing = pd.read_csv(self.recommendations_file)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        
        df_combined.to_csv(self.recommendations_file, index=False)
        print(f"✅ Salvate {len(records)} raccomandazioni in {self.recommendations_file}")
        
        return len(records)
    
    def calculate_accuracy_report(self, days_back=7):
        """Calcola l'accuratezza delle raccomandazioni degli ultimi N giorni"""
        if not self.recommendations_file.exists() or not self.performance_file.exists():
            print("⚠️ File storici non trovati per calcolo accuracy")
            return None
        
        # Carica dati storici
        df_rec = pd.read_csv(self.recommendations_file)
        df_perf = pd.read_csv(self.performance_file)
        
        # Converti date
        df_rec['timestamp'] = pd.to_datetime(df_rec['timestamp'])
        df_perf['timestamp'] = pd.to_datetime(df_perf['timestamp'])
        
        # Filtra ultimi N giorni
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_back)
        df_rec_recent = df_rec[df_rec['timestamp'] >= cutoff_date]
        
        if df_rec_recent.empty:
            print(f"⚠️ Nessuna raccomandazione negli ultimi {days_back} giorni")
            return None
        
        accuracy_results = []
        
        for _, rec_row in df_rec_recent.iterrows():
            asset = rec_row['asset']
            rec_date = rec_row['timestamp']
            segnale = rec_row['segnale']
            
            # Trova performance una settimana dopo la raccomandazione
            future_date = rec_date + datetime.timedelta(days=7)
            
            # Cerca performance più vicina a quella data
            asset_perf = df_perf[df_perf['asset'].str.contains(asset, na=False)]
            future_perf = asset_perf[asset_perf['timestamp'] >= future_date]
            
            if not future_perf.empty:
                actual_perf = future_perf.iloc[0]['performance_1w']
                
                # Valuta se la raccomandazione era corretta
                correct = False
                if segnale == 'BUY' and actual_perf > 0:
                    correct = True
                elif segnale == 'SELL' and actual_perf < 0:
                    correct = True
                elif segnale == 'HOLD' and abs(actual_perf) < 2:
                    correct = True
                
                accuracy_results.append({
                    'asset': asset,
                    'rec_date': rec_date.strftime('%Y-%m-%d'),
                    'segnale_dato': segnale,
                    'performance_reale': actual_perf,
                    'corretto': correct,
                    'giorni_analizzati': days_back
                })
        
        if not accuracy_results:
            print(f"📊 Nessuna valutazione possibile (serve più tempo per verificare)")
            return None
        
        # Calcola statistiche
        df_accuracy = pd.DataFrame(accuracy_results)
        total_recs = len(df_accuracy)
        correct_recs = df_accuracy['corretto'].sum()
        accuracy_pct = (correct_recs / total_recs) * 100
        
        # Salva report
        report = {
            'timestamp': datetime.datetime.now(),
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'giorni_analizzati': days_back,
            'totale_raccomandazioni': total_recs,
            'raccomandazioni_corrette': correct_recs,
            'accuracy_percentuale': accuracy_pct,
            'dettaglio_per_asset': df_accuracy.groupby('asset')['corretto'].agg(['count', 'sum']).to_dict()
        }
        
        # Salva su file accuracy
        df_report = pd.DataFrame([{
            'timestamp': report['timestamp'],
            'date': report['date'], 
            'giorni_analizzati': report['giorni_analizzati'],
            'totale_raccomandazioni': report['totale_raccomandazioni'],
            'corrette': report['raccomandazioni_corrette'],
            'accuracy_pct': report['accuracy_percentuale']
        }])
        
        if self.accuracy_file.exists():
            df_existing = pd.read_csv(self.accuracy_file)
            df_combined = pd.concat([df_existing, df_report], ignore_index=True)
        else:
            df_combined = df_report
        
        df_combined.to_csv(self.accuracy_file, index=False)
        
        print(f"🎯 Accuracy Report generato:")
        print(f"   📅 Periodo: ultimi {days_back} giorni")
        print(f"   📈 Raccomandazioni: {total_recs}")
        print(f"   ✅ Corrette: {correct_recs}")
        print(f"   🎯 Accuracy: {accuracy_pct:.1f}%")
        
        return report
    
    def save_market_performance(self, market_data):
        """Salva le performance di mercato attuali"""
        timestamp = datetime.datetime.now()
        
        records = []
        for asset, perf_dict in market_data.items():
            if isinstance(perf_dict, dict) and 'change' in perf_dict:
                record = {
                    'timestamp': timestamp,
                    'date': timestamp.strftime('%Y-%m-%d'),
                    'time': timestamp.strftime('%H:%M:%S'),
                    'asset': asset,
                    'performance_1w': perf_dict.get('change', 0),
                    'direction': perf_dict.get('direction', 'ND')
                }
                records.append(record)
        
        if not records:
            print("⚠️ Nessuna performance da salvare")
            return 0
        
        df_new = pd.DataFrame(records)
        
        if self.performance_file.exists():
            df_existing = pd.read_csv(self.performance_file)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        
        df_combined.to_csv(self.performance_file, index=False)
        print(f"✅ Salvate {len(records)} performance in {self.performance_file}")
        
        return len(records)
    
    def get_latest_accuracy_summary(self):
        """Ottiene un riepilogo dell'accuracy per la dashboard"""
        if not self.accuracy_file.exists():
            return None
        
        try:
            df_accuracy = pd.read_csv(self.accuracy_file)
            if df_accuracy.empty:
                return None
            
            # Prende il report più recente
            latest_report = df_accuracy.iloc[-1]
            
            return {
                'date': latest_report['date'],
                'giorni_analizzati': latest_report['giorni_analizzati'],
                'totale_raccomandazioni': latest_report['totale_raccomandazioni'],
                'corrette': latest_report['corrette'],
                'accuracy_pct': latest_report['accuracy_pct'],
                'total_reports': len(df_accuracy)
            }
        except Exception as e:
            print(f"❌ Errore caricamento accuracy: {e}")
            return None
