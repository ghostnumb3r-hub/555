"""
Portfolio Bridge - Modulo di integrazione per 555bt
Questo modulo facilita l'integrazione dell'analisi del portafoglio in 555bt.py
senza modificare il file principale.
"""

import os
import sys
from datetime import datetime
from wallet_analyzer import WalletAnalyzer

class PortfolioBridge:
    def __init__(self):
        """Inizializza il bridge per l'analisi del portafoglio"""
        self.analyzer = WalletAnalyzer()
        self.analysis_file = os.path.join('salvataggi', 'portfolio_analysis.txt')
    
    def get_portfolio_section_for_555bt(self):
        """
        Genera una sezione di analisi del portafoglio pronta per essere 
        integrata nei report di 555bt.py
        """
        try:
            # Genera analisi completa e la salva
            analysis_path = self.analyzer.save_portfolio_analysis_for_555bt()
            
            if analysis_path and os.path.exists(analysis_path):
                with open(analysis_path, 'r', encoding='utf-8') as f:
                    portfolio_content = f.read()
                
                # Header di integrazione per 555bt
                integration_header = f"""
{'='*80}
🏦 ANALISI PORTAFOGLIO PERSONALE - INTEGRATA IN 555BT
{'='*80}
📊 Dati aggiornati da Google Sheets e processati con ML
🕐 Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} CET
"""
                
                return integration_header + "\n" + portfolio_content
            else:
                return self._get_error_section("Impossibile generare analisi portafoglio")
                
        except Exception as e:
            print(f"❌ [BRIDGE] Errore generazione sezione portafoglio: {e}")
            return self._get_error_section(f"Errore: {str(e)}")
    
    def _get_error_section(self, error_msg):
        """Restituisce una sezione di errore formattata"""
        return f"""
{'='*80}
❌ ERRORE ANALISI PORTAFOGLIO
{'='*80}
{error_msg}

Per risolvere:
1. Esegui 'python wallet.py' per aggiornare i dati del portafoglio
2. Verifica che i file in salvataggi/ siano presenti
3. Controlla le credenziali Google Sheets

{'='*80}
"""
    
    def get_portfolio_summary_stats(self):
        """Restituisce statistiche summary del portafoglio per dashboard"""
        summary = self.analyzer.get_portfolio_summary()
        risk_analysis = self.analyzer.analyze_portfolio_risk()
        
        if summary and risk_analysis:
            return {
                'total_value': f"€{summary['total_value']:,.2f}",
                'positions': summary['total_positions'],
                'categories': summary['categories'],
                'risk_level': risk_analysis['overall_risk'],
                'risk_score': f"{risk_analysis['weighted_risk_score']:.1f}/10",
                'largest_position': {
                    'name': summary['largest_position']['asset'],
                    'percentage': f"{summary['largest_position']['percentage']:.1f}%"
                }
            }
        return None
    
    def get_ml_signals_for_portfolio_assets(self):
        """
        Restituisce segnali ML per gli asset del portafoglio
        in formato compatibile con 555bt
        """
        ml_predictions = self.analyzer.get_ml_portfolio_predictions()
        
        if not ml_predictions:
            return {}
        
        # Converti in formato 555bt
        signals_555bt = {}
        for asset, prediction in ml_predictions.items():
            # Mappa gli asset ai simboli di mercato
            symbol = self.analyzer.asset_mapping.get(asset, asset)
            
            signals_555bt[symbol] = {
                'signal': prediction['signal'],
                'probability': prediction['probability'],
                'expected_return': prediction['expected_return_percent'],
                'confidence': prediction['confidence'],
                'portfolio_value': prediction['current_value'],
                'portfolio_asset_name': asset,
                'recommendation': prediction['ml_recommendation'],
                'source': 'PORTFOLIO_ML'
            }
        
        return signals_555bt
    
    def generate_portfolio_insights_text(self, max_length=1000):
        """Genera insights del portafoglio in formato breve per dashboard"""
        try:
            summary = self.analyzer.get_portfolio_summary()
            risk_analysis = self.analyzer.analyze_portfolio_risk()
            recommendations = self.analyzer.generate_portfolio_recommendations()
            
            if not summary:
                return "❌ Dati portafoglio non disponibili"
            
            insights = []
            
            # Insight principale
            insights.append(f"💼 Portafoglio: €{summary['total_value']:,.2f} in {summary['total_positions']} posizioni")
            
            # Alert concentrazione
            if summary['largest_position']['percentage'] > 70:
                insights.append(f"⚠️ ALERT: {summary['largest_position']['asset']} rappresenta {summary['largest_position']['percentage']:.1f}% del portafoglio")
            
            # Rischio
            if risk_analysis:
                insights.append(f"📊 Rischio: {risk_analysis['overall_risk']} (Score: {risk_analysis['weighted_risk_score']:.1f}/10)")
            
            # Raccomandazione principale
            high_priority_recs = [r for r in recommendations if r['priority'] == 'ALTA']
            if high_priority_recs:
                top_rec = high_priority_recs[0]
                insights.append(f"🎯 Azione prioritaria: {top_rec['action']} {top_rec['asset']}")
            
            # Unisci e tronca se necessario
            text = " | ".join(insights)
            if len(text) > max_length:
                text = text[:max_length-3] + "..."
            
            return text
            
        except Exception as e:
            return f"❌ Errore insights: {str(e)[:100]}"
    
    def save_integrated_analysis(self, output_dir='salvataggi'):
        """
        Salva un'analisi completa integrando portafoglio + mercato
        per uso in 555bt
        """
        try:
            # Genera la sezione portafoglio
            portfolio_section = self.get_portfolio_section_for_555bt()
            
            # Path del file integrato
            integrated_file = os.path.join(output_dir, 'portfolio_integrated_555bt.txt')
            
            # Salva
            with open(integrated_file, 'w', encoding='utf-8') as f:
                f.write(portfolio_section)
                f.write("\n\n")
                f.write("=" * 80)
                f.write("\n📋 FINE SEZIONE PORTAFOGLIO - PRONTO PER INTEGRAZIONE IN 555BT")
                f.write("\n" + "=" * 80)
            
            print(f"✅ [BRIDGE] Analisi integrata salvata: {integrated_file}")
            return integrated_file
            
        except Exception as e:
            print(f"❌ [BRIDGE] Errore salvataggio integrato: {e}")
            return None

# Funzioni di utilità per uso esterno
def get_portfolio_for_555bt():
    """Funzione rapida per ottenere sezione portafoglio"""
    bridge = PortfolioBridge()
    return bridge.get_portfolio_section_for_555bt()

def get_portfolio_stats():
    """Funzione rapida per ottenere stats portafoglio"""
    bridge = PortfolioBridge()
    return bridge.get_portfolio_summary_stats()

def get_portfolio_ml_signals():
    """Funzione rapida per ottenere segnali ML portafoglio"""
    bridge = PortfolioBridge()
    return bridge.get_ml_signals_for_portfolio_assets()

# Test del modulo
if __name__ == "__main__":
    print("🔗 Test Portfolio Bridge...")
    
    bridge = PortfolioBridge()
    
    # Test 1: Sezione completa
    print("\n1. Test sezione portafoglio...")
    section = bridge.get_portfolio_section_for_555bt()
    print(f"   Lunghezza sezione: {len(section)} caratteri")
    print(f"   Prime righe: {section[:200]}...")
    
    # Test 2: Stats summary
    print("\n2. Test statistiche summary...")
    stats = bridge.get_portfolio_summary_stats()
    if stats:
        print(f"   Valore: {stats['total_value']}")
        print(f"   Rischio: {stats['risk_level']}")
        print(f"   Posizione principale: {stats['largest_position']['name']}")
    
    # Test 3: ML signals
    print("\n3. Test segnali ML...")
    ml_signals = bridge.get_ml_signals_for_portfolio_assets()
    print(f"   Segnali generati per {len(ml_signals)} asset")
    
    # Test 4: Insights brevi
    print("\n4. Test insights brevi...")
    insights = bridge.generate_portfolio_insights_text()
    print(f"   Insights: {insights}")
    
    # Test 5: Salvataggio integrato
    print("\n5. Test salvataggio integrato...")
    integrated_file = bridge.save_integrated_analysis()
    if integrated_file:
        print(f"   ✅ File salvato: {integrated_file}")
    
    print("\n🎉 Test completati!")
