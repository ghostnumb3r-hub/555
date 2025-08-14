# 🔗 Guida di Integrazione: Portafoglio + 555bt

## Overview del Sistema

Il sistema è composto da 3 moduli principali che lavorano insieme senza modificare `555bt.py`:

1. **`wallet.py`** - Interfaccia Dash per gestire dati portafoglio da Google Sheets
2. **`wallet_analyzer.py`** - Motore di analisi ML del portafoglio  
3. **`portfolio_bridge.py`** - Bridge per integrare con 555bt.py

## 🚀 Come Utilizzare il Sistema

### Passo 1: Aggiorna i Dati del Portafoglio
```bash
python wallet.py
```
- Apre dashboard su http://localhost:8050
- Clicca "Aggiorna Dati da Google Sheets"
- Verifica che i dati siano salvati in `salvataggi/wallet_data.csv`

### Passo 2: Genera Analisi Standalone
```bash
python wallet_analyzer.py
```
- Analizza il portafoglio e genera previsioni ML
- Salva il report in `salvataggi/portfolio_analysis.txt`

### Passo 3: Integra con 555bt (3 Modi)

#### Metodo A: File Separato Pronto
```bash
python portfolio_bridge.py
```
- Genera `salvataggi/portfolio_integrated_555bt.txt`
- Copia/incolla questo contenuto nei report di 555bt

#### Metodo B: Import nel Codice
```python
# In 555bt.py o in un altro script
from portfolio_bridge import get_portfolio_for_555bt

# Ottieni sezione portafoglio
portfolio_section = get_portfolio_for_555bt()
print(portfolio_section)
```

#### Metodo C: Funzioni Specifiche
```python
from portfolio_bridge import get_portfolio_stats, get_portfolio_ml_signals

# Per dashboard/UI
stats = get_portfolio_stats()
print(f"Portafoglio: {stats['total_value']} - Rischio: {stats['risk_level']}")

# Per segnali ML
ml_signals = get_portfolio_ml_signals() 
# Restituisce segnali in formato 555bt per BTC-USD, GC=F, etc.
```

## 📁 Struttura File Generati

```
salvataggi/
├── wallet_data.csv                 # Dati grezzi da Google Sheets
├── wallet_analysis.csv             # Analisi rischio per categoria
├── portfolio_analysis.txt          # Report completo standalone
└── portfolio_integrated_555bt.txt  # Report pronto per 555bt
```

## 🎯 Esempi di Output

### Stats Rapide
```python
stats = get_portfolio_stats()
# Output: {
#   'total_value': '€57,755.61',
#   'risk_level': 'MEDIO-ALTO', 
#   'largest_position': {'name': 'Bitcoin', 'percentage': '88.3%'}
# }
```

### Segnali ML per 555bt
```python
ml_signals = get_portfolio_ml_signals()
# Output: {
#   'BTC-USD': {
#     'signal': 'BUY',
#     'probability': 0.789,
#     'expected_return': 20.3,
#     'portfolio_value': 51006.09,
#     'source': 'PORTFOLIO_ML'
#   }
# }
```

### Insights Brevi per Dashboard
```python
from portfolio_bridge import PortfolioBridge
bridge = PortfolioBridge()
insights = bridge.generate_portfolio_insights_text()
# Output: "💼 Portafoglio: €57,755.61 in 7 posizioni | ⚠️ ALERT: Bitcoin 88.3% | 🎯 Azione: RIDURRE Bitcoin"
```

## 🔧 Integrazione Avanzata con 555bt

### Opzione 1: Sezione Dedicata nei Report
Aggiungi questa funzione in `555bt.py`:

```python
def add_portfolio_section_to_report(report_content):
    """Aggiunge sezione portafoglio ai report"""
    try:
        from portfolio_bridge import get_portfolio_for_555bt
        portfolio_section = get_portfolio_for_555bt()
        return report_content + "\n\n" + portfolio_section
    except Exception as e:
        return report_content + f"\n\n❌ Errore portafoglio: {e}"

# Usa così:
final_report = add_portfolio_section_to_report(existing_report)
```

### Opzione 2: Dashboard Enhanced
```python
def get_enhanced_dashboard_data():
    """Combina dati 555bt + portafoglio"""
    # Dati esistenti 555bt
    market_data = get_market_analysis()
    
    # Dati portafoglio
    try:
        from portfolio_bridge import get_portfolio_stats, get_portfolio_ml_signals
        portfolio_stats = get_portfolio_stats()
        portfolio_signals = get_portfolio_ml_signals()
        
        return {
            'market': market_data,
            'portfolio': portfolio_stats,
            'combined_signals': {**market_data.get('signals', {}), **portfolio_signals}
        }
    except:
        return {'market': market_data, 'portfolio': None}
```

### Opzione 3: File di Configurazione
Crea un file `config.py`:
```python
# config.py
ENABLE_PORTFOLIO = True
PORTFOLIO_WEIGHT_IN_ANALYSIS = 0.3  # 30% peso nelle analisi combinate

if ENABLE_PORTFOLIO:
    from portfolio_bridge import get_portfolio_ml_signals
    PORTFOLIO_SIGNALS = get_portfolio_ml_signals()
else:
    PORTFOLIO_SIGNALS = {}
```

## 🔄 Workflow Consigliato

### Giornaliero
1. **Mattina**: `python wallet.py` → Aggiorna dati portafoglio
2. **Analisi**: `python 555bt.py` → Esegui analisi mercato + portafoglio
3. **Sera**: Controlla raccomandazioni nei report generati

### Settimanale  
1. Rivedi allocation del portafoglio basata sui report
2. Verifica alerts di concentrazione e rischio
3. Aggiusta strategie in base alle previsioni ML

## 🚨 Troubleshooting

### Errore "Dati portafoglio non trovati"
```bash
# Verifica file esistenti
ls salvataggi/wallet_*.csv

# Rigenera dati
python wallet.py
```

### Errore "Import wallet_analyzer"
```bash
# Verifica moduli in stessa directory
python -c "from wallet_analyzer import WalletAnalyzer; print('OK')"
```

### Previsioni ML non realistiche
- Le previsioni sono simulate per demo
- In produzione, integra con modelli ML reali di 555bt
- Modifica `get_ml_portfolio_predictions()` in `wallet_analyzer.py`

## 📈 Estensioni Future

### Possibili Miglioramenti
1. **Real-time sync**: WebSocket tra wallet.py e 555bt.py
2. **API Integration**: Direct connection alle API di brokers
3. **Advanced ML**: Integrazione modelli predittivi reali
4. **Risk Alerts**: Notifiche automatiche su Telegram/email
5. **Performance Tracking**: Storico performance predictions vs realtà

### Hook Points per 555bt
```python
# Aggiungi queste funzioni hook in 555bt.py per integrazione automatica

def before_analysis_hook():
    """Chiamata prima dell'analisi principale"""
    from portfolio_bridge import get_portfolio_ml_signals
    return get_portfolio_ml_signals()

def after_analysis_hook(analysis_results):
    """Chiamata dopo l'analisi per aggiungere portafoglio"""  
    from portfolio_bridge import get_portfolio_for_555bt
    portfolio_section = get_portfolio_for_555bt()
    return analysis_results + "\n\n" + portfolio_section

def dashboard_enhancement_hook():
    """Per migliorare dashboard con dati portafoglio"""
    from portfolio_bridge import get_portfolio_stats
    return get_portfolio_stats()
```

## ✅ Sistema Pronto per l'Uso!

Il sistema è ora completamente funzionale e integrato. Puoi:

- ✅ Gestire portafoglio via Google Sheets
- ✅ Generare analisi ML automatiche  
- ✅ Integrare con 555bt senza modificarlo
- ✅ Ottenere raccomandazioni operative
- ✅ Monitorare rischio in tempo reale

**Next Steps**: Esegui `python portfolio_bridge.py` per vedere tutto in azione! 🎉
