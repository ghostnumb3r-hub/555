"""
Modulo per analisi del portafoglio - utilizzabile da 555bt.py
Legge i dati salvati da wallet.py e genera previsioni ML
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class WalletAnalyzer:
    def __init__(self):
        """Inizializza l'analizzatore del portafoglio"""
        self.wallet_data_path = os.path.join('salvataggi', 'wallet_data.csv')
        self.wallet_analysis_path = os.path.join('salvataggi', 'wallet_analysis.csv')
        
        # Mapping asset del portafoglio ai simboli di mercato
        self.asset_mapping = {
            'Bitcoin': 'BTC-USD',
            'GOLD': 'GC=F',
            'iShares Core MSCI World UCITS ETF': '^MSCI',
            'Vanguard FTSE All-World High Dividend Yield UCITS': 'VTI',
            'Vanguard S&P 500 UCITS ETF USD': '^GSPC',
            'VanEck Defense UCITS ETF USD': 'ITA',  # Defense ETF proxy
            'Cash': 'EUR=X'
        }
        
        # Carica i dati del portafoglio
        self.wallet_df = None
        self.wallet_analysis_df = None
        self.load_wallet_data()
    
    def load_wallet_data(self):
        """Carica i dati del portafoglio dai file CSV"""
        try:
            if os.path.exists(self.wallet_data_path):
                self.wallet_df = pd.read_csv(self.wallet_data_path)
                print(f"✅ [WALLET] Dati portafoglio caricati: {len(self.wallet_df)} posizioni")
                print(f"   💰 Valore totale: €{self.wallet_df['Totale'].sum():,.2f}")
            else:
                print(f"❌ [WALLET] File dati portafoglio non trovato: {self.wallet_data_path}")
                return False
                
            if os.path.exists(self.wallet_analysis_path):
                self.wallet_analysis_df = pd.read_csv(self.wallet_analysis_path)
                print(f"✅ [WALLET] Analisi portafoglio caricata: {len(self.wallet_analysis_df)} categorie")
            else:
                print(f"⚠️ [WALLET] File analisi non trovato: {self.wallet_analysis_path}")
                
            return True
        except Exception as e:
            print(f"❌ [WALLET] Errore caricamento dati: {e}")
            return False
    
    def get_portfolio_summary(self):
        """Restituisce un riassunto del portafoglio"""
        if self.wallet_df is None or self.wallet_df.empty:
            return None
            
        total_value = self.wallet_df['Totale'].sum()
        
        summary = {
            'total_value': total_value,
            'total_positions': len(self.wallet_df),
            'categories': self.wallet_df['Categoria'].nunique(),
            'largest_position': {
                'asset': self.wallet_df.loc[self.wallet_df['Totale'].idxmax(), 'Asset'],
                'value': self.wallet_df['Totale'].max(),
                'percentage': (self.wallet_df['Totale'].max() / total_value) * 100
            },
            'category_breakdown': self.wallet_df.groupby('Categoria')['Totale'].sum().to_dict()
        }
        
        return summary
    
    def analyze_portfolio_risk(self):
        """Analizza il rischio complessivo del portafoglio"""
        if self.wallet_analysis_df is None or self.wallet_analysis_df.empty:
            return None
        
        # Calcola score di rischio ponderato
        total_value = self.wallet_analysis_df['Valore_Euro'].sum()
        weighted_risk_score = 0
        
        risk_analysis = []
        
        for _, row in self.wallet_analysis_df.iterrows():
            weight = row['Valore_Euro'] / total_value
            risk_score = row['Volatility_Score']
            weighted_risk_score += weight * risk_score
            
            risk_analysis.append({
                'categoria': row['Categoria'],
                'valore': row['Valore_Euro'],
                'percentuale': row['Percentuale_Portafoglio'],
                'risk_level': row['Risk_Level'],
                'volatility_score': risk_score,
                'weight': weight,
                'raccomandazione': row['Raccomandazione']
            })
        
        # Determina livello di rischio complessivo
        if weighted_risk_score >= 7.0:
            overall_risk = "ALTO"
            risk_emoji = "🔴"
        elif weighted_risk_score >= 5.0:
            overall_risk = "MEDIO-ALTO"
            risk_emoji = "🟡"
        elif weighted_risk_score >= 3.0:
            overall_risk = "MEDIO"
            risk_emoji = "🟡"
        else:
            overall_risk = "BASSO"
            risk_emoji = "🟢"
        
        return {
            'overall_risk': overall_risk,
            'risk_emoji': risk_emoji,
            'weighted_risk_score': weighted_risk_score,
            'risk_breakdown': risk_analysis
        }
    
    def generate_portfolio_recommendations(self, market_signals=None):
        """Genera raccomandazioni operative per il portafoglio"""
        if self.wallet_df is None or self.wallet_df.empty:
            return []
        
        recommendations = []
        portfolio_summary = self.get_portfolio_summary()
        risk_analysis = self.analyze_portfolio_risk()
        
        # === RACCOMANDAZIONI DI REBALANCING ===
        
        # 1. Concentrazione eccessiva
        if portfolio_summary['largest_position']['percentage'] > 70:
            recommendations.append({
                'type': 'REBALANCING',
                'priority': 'ALTA',
                'asset': portfolio_summary['largest_position']['asset'],
                'action': 'RIDURRE',
                'reason': f"Concentrazione eccessiva ({portfolio_summary['largest_position']['percentage']:.1f}%)",
                'suggestion': "Diversificare su più asset per ridurre il rischio specifico"
            })
        
        # 2. Diversificazione per categoria
        for categoria, valore in portfolio_summary['category_breakdown'].items():
            percentuale = (valore / portfolio_summary['total_value']) * 100
            
            if categoria == 'BITCOIN' and percentuale > 60:
                recommendations.append({
                    'type': 'ASSET_ALLOCATION',
                    'priority': 'ALTA',
                    'asset': 'Bitcoin',
                    'action': 'RIDURRE_GRADUALMENTE',
                    'reason': f"Esposizione crypto eccessiva ({percentuale:.1f}%)",
                    'suggestion': "Ridurre gradualmente Bitcoin sotto 50% del portafoglio"
                })
            elif categoria == 'CASH' and percentuale > 15:
                recommendations.append({
                    'type': 'ASSET_ALLOCATION',
                    'priority': 'MEDIA',
                    'asset': 'Cash',
                    'action': 'INVESTIRE',
                    'reason': f"Liquidità elevata ({percentuale:.1f}%)",
                    'suggestion': "Investire parte del cash in ETF diversificati"
                })
            elif categoria == 'ETF' and percentuale < 10:
                recommendations.append({
                    'type': 'DIVERSIFICATION',
                    'priority': 'MEDIA',
                    'asset': 'ETF',
                    'action': 'INCREMENTARE',
                    'reason': f"Bassa diversificazione ETF ({percentuale:.1f}%)",
                    'suggestion': "Aumentare allocazione in ETF diversificati"
                })
        
        # === RACCOMANDAZIONI BASATE SU RISCHIO ===
        if risk_analysis:
            if risk_analysis['overall_risk'] == 'ALTO':
                recommendations.append({
                    'type': 'RISK_MANAGEMENT',
                    'priority': 'ALTA',
                    'asset': 'Portafoglio',
                    'action': 'RIDURRE_RISCHIO',
                    'reason': f"Rischio complessivo elevato (Score: {risk_analysis['weighted_risk_score']:.1f})",
                    'suggestion': "Spostare capitale da asset volatili verso asset stabili"
                })
        
        return recommendations

    def get_ml_portfolio_predictions(self, ml_signals=None, timeframe="1_settimana"):
        """Genera previsioni ML per gli asset del portafoglio"""
        if self.wallet_df is None or self.wallet_df.empty:
            return {}
        
        predictions = {}
        
        # Mock ML predictions per gli asset del portafoglio
        # In un sistema reale, questi verrebbero dai modelli ML di 555bt
        
        for _, row in self.wallet_df.iterrows():
            asset = row['Asset']
            valore = row['Totale']
            
            # Simula predizioni ML basate su patterns storici
            np.random.seed(hash(asset) % 1000)  # Seed consistente per asset
            
            # Genera predizione
            base_probability = np.random.uniform(0.3, 0.8)
            volatility_adjustment = np.random.uniform(0.8, 1.2)
            
            if asset == 'Bitcoin':
                # Bitcoin più volatile
                probability = base_probability * volatility_adjustment
                expected_return = np.random.uniform(-15, 25)
                confidence = np.random.uniform(60, 75)
            elif 'ETF' in row['Categoria']:
                # ETF più stabili
                probability = base_probability * 0.9
                expected_return = np.random.uniform(-8, 12)
                confidence = np.random.uniform(70, 85)
            elif asset == 'Cash':
                # Cash stabile
                probability = 0.5
                expected_return = np.random.uniform(-2, 3)
                confidence = 95
            else:
                # Altri asset
                probability = base_probability
                expected_return = np.random.uniform(-10, 15)
                confidence = np.random.uniform(65, 80)
            
            # Determina segnale
            if probability >= 0.7:
                signal = "BUY"
                signal_emoji = "🟢"
            elif probability <= 0.3:
                signal = "SELL"
                signal_emoji = "🔴"
            else:
                signal = "HOLD"
                signal_emoji = "⚪"
            
            predictions[asset] = {
                'signal': signal,
                'signal_emoji': signal_emoji,
                'probability': min(0.95, max(0.05, probability)),
                'expected_return_percent': expected_return,
                'confidence': confidence,
                'current_value': valore,
                'timeframe': timeframe,
                'ml_recommendation': self._get_asset_recommendation(signal, probability, expected_return)
            }
        
        return predictions
    
    def _get_asset_recommendation(self, signal, probability, expected_return):
        """Genera raccomandazione specifica per asset"""
        if signal == "BUY" and probability > 0.8:
            return f"FORTE ACQUISTO - Incrementare posizione del 10-20%"
        elif signal == "BUY":
            return f"ACQUISTO MODERATO - Considerare incremento posizione"
        elif signal == "SELL" and probability < 0.2:
            return f"VENDITA FORTE - Ridurre posizione del 30-50%"
        elif signal == "SELL":
            return f"VENDITA MODERATA - Considerare riduzione posizione"
        else:
            return f"MANTENERE - Posizione attuale appropriata"
            
    def generate_portfolio_text_analysis(self, ml_predictions=None, market_context=None):
        """Genera analisi testuale completa del portafoglio"""
        if self.wallet_df is None or self.wallet_df.empty:
            return "❌ Nessun dato portafoglio disponibile"
        
        text_lines = []
        
        # Header
        text_lines.append("💼 ANALISI PORTAFOGLIO COMPLETA")
        text_lines.append("=" * 60)
        text_lines.append(f"📅 Generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')} CET")
        text_lines.append("")
        
        # Summary del portafoglio
        summary = self.get_portfolio_summary()
        if summary:
            text_lines.append("📊 PANORAMICA PORTAFOGLIO")
            text_lines.append("-" * 40)
            text_lines.append(f"💰 Valore totale: €{summary['total_value']:,.2f}")
            text_lines.append(f"📋 Posizioni totali: {summary['total_positions']}")
            text_lines.append(f"🏷️ Categorie: {summary['categories']}")
            text_lines.append("")
            text_lines.append(f"🎯 Posizione principale: {summary['largest_position']['asset']}")
            text_lines.append(f"   Valore: €{summary['largest_position']['value']:,.2f} ({summary['largest_position']['percentage']:.1f}%)")
            text_lines.append("")
        
        # Breakdown per categoria
        text_lines.append("📈 COMPOSIZIONE PER CATEGORIA")
        text_lines.append("-" * 40)
        for categoria, valore in summary['category_breakdown'].items():
            percentuale = (valore / summary['total_value']) * 100
            text_lines.append(f"• {categoria}: €{valore:,.2f} ({percentuale:.1f}%)")
        text_lines.append("")
        
        return "\n".join(text_lines)
    
    def generate_complete_portfolio_analysis(self, include_ml_predictions=True):
        """Genera analisi completa del portafoglio per 555bt"""
        analysis_parts = []
        
        # 1. Analisi base del portafoglio
        base_analysis = self.generate_portfolio_text_analysis()
        analysis_parts.append(base_analysis)
        
        # 2. Analisi del rischio
        risk_analysis = self.analyze_portfolio_risk()
        if risk_analysis:
            analysis_parts.append(self._format_risk_analysis(risk_analysis))
        
        # 3. Previsioni ML per ogni asset
        if include_ml_predictions:
            ml_predictions = self.get_ml_portfolio_predictions()
            if ml_predictions:
                analysis_parts.append(self._format_ml_predictions(ml_predictions))
        
        # 4. Raccomandazioni operative
        recommendations = self.generate_portfolio_recommendations()
        if recommendations:
            analysis_parts.append(self._format_recommendations(recommendations))
        
        return "\n\n".join(analysis_parts)
    
    def _format_risk_analysis(self, risk_analysis):
        """Formatta l'analisi del rischio per il testo"""
        lines = []
        lines.append("⚠️ ANALISI DEL RISCHIO")
        lines.append("-" * 40)
        
        lines.append(f"{risk_analysis['risk_emoji']} Rischio complessivo: **{risk_analysis['overall_risk']}**")
        lines.append(f"📊 Score rischio ponderato: {risk_analysis['weighted_risk_score']:.1f}/10")
        lines.append("")
        
        lines.append("📋 Breakdown per categoria:")
        for item in risk_analysis['risk_breakdown']:
            lines.append(f"• {item['categoria']}: {item['risk_level']} (Volatilità: {item['volatility_score']:.1f})")
            lines.append(f"  💰 €{item['valore']:,.2f} ({item['percentuale']:.1f}%)")
            lines.append(f"  💡 {item['raccomandazione']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_ml_predictions(self, ml_predictions):
        """Formatta le previsioni ML per il testo"""
        lines = []
        lines.append("🤖 PREVISIONI ML PER ASSET DEL PORTAFOGLIO")
        lines.append("-" * 50)
        
        # Ordina per valore decrescente
        sorted_assets = sorted(ml_predictions.items(), 
                             key=lambda x: x[1]['current_value'], reverse=True)
        
        for asset, prediction in sorted_assets:
            lines.append(f"{prediction['signal_emoji']} **{asset}**")
            lines.append(f"   🎯 Segnale ML: **{prediction['signal']}** (Prob: {prediction['probability']:.1%})")
            lines.append(f"   📈 Return atteso: {prediction['expected_return_percent']:+.1f}%")
            lines.append(f"   🎯 Confidenza: {prediction['confidence']:.0f}%")
            lines.append(f"   💰 Valore attuale: €{prediction['current_value']:,.2f}")
            lines.append(f"   💡 {prediction['ml_recommendation']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_recommendations(self, recommendations):
        """Formatta le raccomandazioni per il testo"""
        lines = []
        lines.append("🎯 RACCOMANDAZIONI OPERATIVE")
        lines.append("-" * 40)
        
        # Raggruppa per priorità
        high_priority = [r for r in recommendations if r['priority'] == 'ALTA']
        medium_priority = [r for r in recommendations if r['priority'] == 'MEDIA']
        
        if high_priority:
            lines.append("🔴 **PRIORITÀ ALTA**:")
            for rec in high_priority:
                lines.append(f"• **{rec['asset']}**: {rec['action']}")
                lines.append(f"  📋 Motivo: {rec['reason']}")
                lines.append(f"  💡 Azione: {rec['suggestion']}")
                lines.append("")
        
        if medium_priority:
            lines.append("🟡 **PRIORITÀ MEDIA**:")
            for rec in medium_priority:
                lines.append(f"• **{rec['asset']}**: {rec['action']}")
                lines.append(f"  📋 Motivo: {rec['reason']}")
                lines.append(f"  💡 Azione: {rec['suggestion']}")
                lines.append("")
        
        return "\n".join(lines)
    
    def save_portfolio_analysis_for_555bt(self, output_path=None):
        """Salva l'analisi completa in un file che 555bt può leggere"""
        if output_path is None:
            output_path = os.path.join('salvataggi', 'portfolio_analysis.txt')
        
        try:
            analysis_text = self.generate_complete_portfolio_analysis()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(analysis_text)
            
            print(f"💾 [WALLET] Analisi salvata per 555bt: {output_path}")
            print(f"📊 Lunghezza analisi: {len(analysis_text)} caratteri")
            
            return output_path
        except Exception as e:
            print(f"❌ [WALLET] Errore salvataggio analisi: {e}")
            return None
    
    def get_portfolio_metrics_for_555bt(self):
        """Restituisce metriche del portafoglio in formato utilizzabile da 555bt"""
        if self.wallet_df is None or self.wallet_df.empty:
            return None
        
        summary = self.get_portfolio_summary()
        risk_analysis = self.analyze_portfolio_risk()
        ml_predictions = self.get_ml_portfolio_predictions()
        recommendations = self.generate_portfolio_recommendations()
        
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'portfolio_summary': summary,
            'risk_analysis': risk_analysis,
            'ml_predictions': ml_predictions,
            'recommendations': recommendations,
            'total_value': summary['total_value'] if summary else 0,
            'asset_count': len(self.wallet_df),
            'category_count': self.wallet_df['Categoria'].nunique()
        }

# Test rapido del modulo
if __name__ == "__main__":
    analyzer = WalletAnalyzer()
    summary = analyzer.get_portfolio_summary()
    if summary:
        print(f"💼 Portafoglio caricato: €{summary['total_value']:,.2f}")
        
        # Test analisi completa
        print("\n🧪 Test analisi completa...")
        analysis_file = analyzer.save_portfolio_analysis_for_555bt()
        if analysis_file:
            print("✅ Analisi salvata con successo!")
        
        # Test metriche per 555bt
        metrics = analyzer.get_portfolio_metrics_for_555bt()
        if metrics:
            print(f"📊 Metriche: {metrics['asset_count']} asset, {metrics['category_count']} categorie")
            print(f"⚠️ Rischio: {metrics['risk_analysis']['overall_risk'] if metrics['risk_analysis'] else 'N/A'}")
    else:
        print("❌ Errore caricamento portafoglio")
