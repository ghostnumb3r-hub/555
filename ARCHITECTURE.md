# 🛠️ ARCHITECTURE - Sistema 555

> **Documentazione Tecnica Completa dell'Architettura**

## 🔄 **FLUSSO DATI PRINCIPALE 2.0**

### **1. GOOGLE DRIVE SYNC - Architettura Aggiornata**
```
Render (Cloud) ↔️ sync_system.py ↔️ Google Drive/555/salvataggi/ ↔️ 555.py
```

**File sincronizzati automaticamente su Google Drive:**
- `analysis_text.txt` - Report backtest completo
- `segnali_tecnici.csv` - Indicatori tecnici correnti  
- `previsioni_ml.csv` - Previsioni ML correnti
- `weekly_report_enhanced.txt` - Report settimanale
- `portfolio_analysis.txt` - Analisi portafoglio
- `indicatori_cumulativo.csv` - Storico indicatori 
- `previsioni_cumulativo.csv` - Storico previsioni ML

**Configurazione sync:**
- Posizione Drive: `H:\Il mio Drive\555\`
- URL Render: `https://five55-c3xl.onrender.com`
- Backup Render: **17:05** ogni giorno (NUOVO ORARIO)
- Modalità: Auto (confronta timestamp, sincronizza il più recente)

### **2. CARICAMENTO DATI 555.py ALL'AVVIO DAL DRIVE**

#### **Sequenza di avvio:**
1. Avvio da `🚀 Lancia 555 Dashboard.bat` - Scorciatoia principale
2. `ensure_directories()` - Crea salvataggi/ su Google Drive se non esiste
3. `load_persistent_cache()` - Carica cache dati FRED/Crypto
4. Thread avvio applicazioni integrate (wallet.py su porta 8051) 

#### **Dati caricati automaticamente:**
- ✅ Cache persistente (salvataggi/data_cache.pkl)
- ✅ File CSV da Google Drive (tutti già in posizione corretta)
- ✅ Dati FRED e Crypto (lazy loading con cache)
- ✅ Tutti i file cumulativi e storici 

## 📂 **STRUTTURA DATI SALVATAGGI SU DRIVE**

### **File CSV Cumulativi (Storici):**
- `previsioni_cumulativo.csv` - Tutte le previsioni ML nel tempo
- `indicatori_cumulativo.csv` - Tutti gli indicatori tecnici nel tempo
- `notizie_cumulativo.csv` - Tutte le notizie analizzate nel tempo
- `daily_recommendations.csv` - Raccomandazioni giornaliere

### **File CSV Correnti (Sovrascrivibili):**
- `previsioni_ml.csv` - Previsioni ML attuali
- `segnali_tecnici.csv` - Indicatori tecnici attuali
- `notizie_export.csv` - Notizie attuali

### **File di Analisi:**
- `analysis_text.txt` - Report backtest completo (da 555bt.py)
- `weekly_report_enhanced.txt` - Report settimanale avanzato
- `portfolio_analysis.txt` - Analisi portafoglio

### **File di Stato e Flags:**
- `*_sent_*.flag` - Flags di tracking messaggi
- `backup_sent_*.flag` - Flags di tracking backup
- `data_cache.pkl` - Cache FRED/Crypto

## 🎯 **GENERAZIONE REPORT - ARCHITETTURA IBRIDA**

### **TIPO 1: Report con Dati LIVE** ⚡
**Funzioni che generano dati in tempo reale:**
- `generate_weekly_backtest_summary()` (riga 2167)
- `generate_unified_report()` (riga 5282)
- `get_all_signals_summary()` (riga 3690)

**Processo:**
1. Carica dati FRED/Crypto live
2. Calcola ML e indicatori fresh
3. Genera report immediato

### **TIPO 2: Report che LEGGONO dai Salvataggi** 📂
**Punti di lettura confermati:**

#### **Analysis Text:**
```python
# Riga 4999, 5861, 6148
analysis_file = os.path.join('salvataggi', 'analysis_text.txt')
with open(analysis_file, 'r', encoding='utf-8') as f:
    analysis_content = f.read().strip()
```

#### **CSV Cumulativi:**
```python
# Riga 4459 - Previsioni storiche
file_path = os.path.join('salvataggi', 'previsioni_cumulativo.csv')
df_old = pd.read_csv(file_path)

# Riga 6343 - Indicatori storici  
cumulative_path = os.path.join('salvataggi', 'indicatori_cumulativo.csv')
df_old = pd.read_csv(cumulative_path)

# Riga 6475 - Notizie storiche
cumulative_news_path = os.path.join('salvataggi', 'notizie_cumulativo.csv')
df_old_news = pd.read_csv(cumulative_news_path)
```

### **TIPO 3: Report IBRIDI** 🔄
**La maggior parte dei report combina:**
- ⚡ **Calcoli LIVE**: ML e indicatori in tempo reale
- 📂 **Dati STORICI**: Context e trend dai salvataggi
- 🔄 **Dati SYNC**: Content aggiornato da Render

## 🚀 **THREADING E AUTOMAZIONE**

### **Thread Attivi:**
1. **Scheduler Thread**: Report programmati
2. **Keep-Alive Thread**: Mantiene app attiva
3. **Sync Thread**: Sincronizzazione continua (se abilitato)

### **Report Automatici:**
- **09:00**: Morning briefing
- **13:00**: Unified report
- **13:05**: Weekly report (solo lunedì)

## 📈 **MODELLI ML E INDICATORI**

### **Modelli ML Disponibili:**
- Random Forest, Logistic Regression, Gradient Boosting
- XGBoost, Support Vector Machine, K-Nearest Neighbors
- Naive Bayes, AdaBoost, Extra Trees, Neural Network
- Ensemble Voting, LightGBM, CatBoost, LSTM, GRU
- ARIMA, GARCH, Reinforcement Learning

### **Indicatori Tecnici (17 totali):**
**Principali:** MAC, RSI, MACD, Bollinger, EMA, SMA
**Secondari:** Stochastic, ATR, CCI, Momentum, ROC, ADX  
**Avanzati:** OBV, Ichimoku, ParabolicSAR, PivotPoints

## 💾 **CACHE E PERFORMANCE**

### **Multi-Layer Cache:**
1. **L1 - Memory Cache**: Validità temporale (60 min default)
2. **L2 - LRU Cache**: Fino a 50 entries
3. **L3 - Persistent**: File pickle in salvataggi/

### **Ottimizzazioni:**
- Lazy loading dei modelli ML
- Cache automatica dati FRED/Crypto
- Pulizia cache scadute automatica
- Salvataggio cache ogni 3-5 nuovi caricamenti

## 🔧 **CONFIGURAZIONI CHIAVE**

### **URLs e Percorsi:**
- Render: `https://five55-c3xl.onrender.com`
- Render External URL: Configurabile tramite `RENDER_EXTERNAL_URL`
- Locale: `C:\Users\valen\555\salvataggi`
- Cache: `salvataggi/data_cache.pkl`

### **Telegram:**
- Token: Configurato in 555.py
- Chat: `@abkllr`
- Features controllabili via FEATURES_ENABLED dict

### **Timeframes Supportati:**
- 1 settimana (1w), 1 mese (1m), 6 mesi (6m), 1 anno (1y)
- Default per report: 1 giorno (1d)

## ⚙️ **STARTUP SEQUENCE COMPLETA (GOOGLE DRIVE)**

```
1. 🚀 Doppio click su "Lancia 555 Dashboard.bat"
2. cd "H:\Il mio Drive\555"
3. python 555.py
4. ensure_directories() → Crea cartella salvataggi su Drive se non esiste
5. load_persistent_cache() → Carica cache dati da Drive
6. sync_system inizializzazione → Se disponibile
7. Thread startup → Scheduler, keep-alive, sync (SOLO per locale, non report)
8. App startup → Dashboard su porta 8050
9. Multi-app → Avvia wallet.py su porta 8051 (locale)
10. Tutti i salvataggi → Google Drive/555/salvataggi/ (automatico)
```

## 🏗️ **ARCHITETTURA DUAL-MODE COMPLETA**

### **555.py (Google Drive - Principale)**
- ✅ **Dashboard interattiva** per analisi
- ✅ **Backtest manuali** e analisi real-time
- ✅ **Salvataggi automatici** su Google Drive
- ✅ **Cache performance** ottimizzata
- ✅ **Multi-app** (Dashboard + Wallet)
- ❌ **Report automatici disabilitati** (gestiti da Render)

### **555-server.py (Render - Automazione)**
- ✅ **Report automatici** (09:00, 13:00)
- ✅ **Backup quotidiano** (17:05 - NUOVO ORARIO)
- ✅ **Keep-alive** e monitoraggio 24/7
- ✅ **API endpoints** per sincronizzazione
- ❌ **Dashboard web** (focus su automazione)

### **Sistema di Sicurezza e Ridondanza**
- 🔄 **Doppio backup**: Google Drive + Render
- 📊 **File cumulativi** mantengono storico completo
- 🔐 **Separazione dati** pubblici/privati
- ⚡ **Failover automatico** se uno dei sistemi non è disponibile

## 🎯 **VANTAGGI ARCHITETTURA 2.0**

### **Performance**
- ⚡ **Cache locale veloce** su SSD Google Drive
- 🔄 **Sync automatico** senza intervento manuale
- 📊 **Elaborazione distribuita** (locale per analisi, cloud per automazione)

### **Affidabilità**
- 💾 **Backup triplo**: Drive + Render + File cumulativi
- 🔄 **Recovery automatico** in caso di problemi
- ⏰ **Scheduling robusto** con retry automatici

### **Scalabilità**
- 📈 **Facile espansione** con nuovi moduli
- 🔧 **Configurazione modulare** per features
- 🎛️ **Control granulare** su ogni componente

---

**Data documento:** 16 Agosto 2025  
**Versione architettura:** 2.0 (Google Drive)  
**Sistema analizzato:** 555.py (Drive) + 555-server.py (Render) + sync_system.py  
**Architettura:** Dual-Mode (Locale Drive + Cloud Render)
