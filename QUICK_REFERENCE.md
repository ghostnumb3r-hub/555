# 🔧 QUICK REFERENCE - Sistema 555

> **Riferimento Rapido per Sviluppatori e Operazioni**

## 📋 **QUICK START**

### **Avvio Sistema dal Google Drive:**
```bash
# 1. 🚀 METODO RACCOMANDATO: Scorciatoia
Doppio clic su "🚀 Lancia 555 Dashboard.bat"

# 2. Avvio manuale dal Drive
python "H:\Il mio Drive\555\555.py"

# 3. Avvia sync (automatico, già integrato)
# sync_system.py si avvia automaticamente

# 4. Wallet (automatico se locale)
# wallet.py si avvia automaticamente su porta 8051
```

### **URLs di accesso:**
- **Dashboard 555**: `http://localhost:8050`
- **Wallet 555BT**: `http://localhost:8051` 
- **Render Cloud**: `https://five55-dd08.onrender.com`

## 🔄 **ARCHITETTURA DATI AGGIORNATA**

### **Flusso Principale:**
```
Render Cloud ↔️ sync_system.py ↔️ Google Drive/555/salvataggi/ ↔️ 555.py Dashboard
```

### **Sincronizzazione Automatica:**
- ✅ **All'avvio**: Sync iniziale automatico (se configurato)
- ✅ **Google Drive**: Sincronizzazione automatica nativa
- ✅ **Render Backup**: 17:05 quotidiano
- ✅ **Bidirezionale**: Google Drive ↔️ Render (quando necessario)

## 📂 **STRUTTURA FILE CHIAVE (GOOGLE DRIVE)**

```
Google Drive/555/
├── 🚀 Lancia 555 Dashboard.bat  # ⭐ SCORCIATOIA PRINCIPALE
├── 555.py                        # Dashboard principale
├── 555-server.py                 # Server Render (backup 17:05)
├── sync_system.py               # Sistema sincronizzazione
├── wallet.py                    # Wallet dashboard (porta 8051)
├── 555bt.py                     # Sistema backtest
├── salvataggi/                  # ⭐ CARTELLA DATI PRINCIPALE (SU DRIVE)
│   ├── analysis_text.txt        # Report backtest completo
│   ├── previsioni_ml.csv        # Previsioni ML correnti
│   ├── segnali_tecnici.csv      # Indicatori tecnici correnti
│   ├── previsioni_cumulativo.csv     # ⏳ Storico previsioni
│   ├── indicatori_cumulativo.csv     # ⏳ Storico indicatori
│   ├── notizie_cumulativo.csv        # ⏳ Storico notizie
│   ├── daily_recommendations.csv     # ⏳ Raccomandazioni
│   ├── data_cache.pkl           # Cache FRED/Crypto
│   └── *.txt, *.csv             # Altri report e dati (tutti su Drive)
```

## 🎯 **FUNZIONI PRINCIPALI**

### **Report Generation:**
```python
# Report LIVE (genera dati freschi)
generate_weekly_backtest_summary()   # Riga 2167
generate_unified_report()           # Riga 5282
get_all_signals_summary()          # Riga 3690

# Report STORAGE (legge dai salvataggi)
analysis_file = 'salvataggi/analysis_text.txt'     # Righe 4999, 5861, 6148
df_old = pd.read_csv('salvataggi/previsioni_cumulativo.csv')  # Riga 4459
```

### **Data Loading:**
```python
# Cache e dati
load_persistent_cache()    # Riga 3286 - Carica cache all'avvio
load_data_fred()          # Riga 3344 - Dati economici
load_crypto_data()        # Riga 3410 - Dati crypto

# Sync system
sync.sync_files("auto")   # Sincronizza da/verso Render
```

### **ML & Indicators:**
```python
# Modelli disponibili (17 totali)
models = {
    "Random Forest", "Logistic Regression", "Gradient Boosting",
    "XGBoost", "SVM", "KNN", "Naive Bayes", "AdaBoost",
    "Extra Trees", "Neural Network", "Ensemble Voting",
    "LightGBM", "CatBoost", "LSTM", "GRU", "ARIMA", "GARCH"
}

# Indicatori tecnici (17 totali)
indicators = [
    "MAC", "RSI", "MACD", "Bollinger", "EMA", "SMA",           # Principali
    "Stochastic", "ATR", "CCI", "Momentum", "ROC", "ADX",      # Secondari  
    "OBV", "Ichimoku", "ParabolicSAR", "PivotPoints"          # Avanzati
]
```

## 🤖 **AUTOMAZIONE**

### **Thread Background:**
1. **Scheduler Thread**: Report automatici (09:00, 13:00, 13:05)
2. **Keep-Alive Thread**: Mantiene connessione attiva
3. **Sync Thread**: Sincronizzazione continua ogni 15min

### **Report Programmati:**
- **09:00** - Morning briefing giornaliero
- **13:00** - Unified report completo  
- **13:05** - Weekly report (solo lunedì)

## ⚙️ **CONFIGURAZIONI**

### **Variabili Chiave:**
```python
# Sync system
RENDER_URL = "https://five55-7ozo.onrender.com"
LOCAL_PATH = "C:\\Users\\valen\\555\\salvataggi"
SYNC_INTERVAL = 15  # minuti

# Features control
FEATURES_ENABLED = {
    "scheduled_reports": False,    # Report programmati
    "manual_reports": False,       # Report manuali
    "backtest_reports": True,      # Backtest settimanali
    "analysis_reports": False      # Analysis text
}

# Cache settings
CACHE_CONFIG = {
    "max_size": 50,
    "cache_duration_minutes": 60
}
```

### **Telegram:**
```python
TELEGRAM_TOKEN = "configurato_in_555.py"
TELEGRAM_CHAT_ID = "@abkllr"
```

## 📊 **DATI E ASSETS**

### **Asset Supportati:**
- **FRED**: Dollar Index, S&P 500, Gold ($/oz)
- **Crypto**: Bitcoin, Gold (PAXG)
- **Timeframes**: 1w, 1m, 6m, 1y

### **Fonti Dati:**
- **FRED**: Federal Reserve Economic Data
- **CryptoCompare**: Dati criptovalute
- **RSS Feeds**: Notizie finanziarie
- **Calendar Events**: Eventi economici

## 🔧 **DEBUG E TROUBLESHOOTING**

### **Log Chiave:**
```
🔄 [SYNC] - Operazioni sincronizzazione
📊 [UNIFIED] - Generazione report
🤖 [ML] - Previsioni machine learning
📈 [INDICATORS] - Calcoli indicatori
💾 [CACHE] - Operazioni cache
```

### **File di Debug:**
- Console output di 555.py
- File CSV in salvataggi/ per verification
- Cache pickle per performance check

### **Problemi Comuni:**
1. **Sync fails**: Controlla connessione Render
2. **Missing data**: Verifica cache e file CSV
3. **ML errors**: Controlla disponibilità dati FRED/Crypto
4. **Report empty**: Verifica salvataggi/analysis_text.txt

## 🚨 **COMMANDS RAPIDI**

### **Manual Operations:**
```python
# Sync manuale
sync = SalvataggieSync()
sync.sync_files("from_render")  # Solo download
sync.sync_files("to_render")    # Solo upload
sync.sync_files("auto")         # Bidirezionale

# Cache operations
load_persistent_cache()         # Ricarica cache
clean_expired_cache()          # Pulisci cache scadute

# Report generation
generate_unified_report("manual")
generate_weekly_backtest_summary()
```

### **Feature Control:**
```python
# Enable/disable features
enable_feature_temporarily("manual_reports")
disable_feature("scheduled_reports")

# Check status
is_feature_enabled("backtest_reports")
```

---

## 🏆 **CARATTERISTICHE PRINCIPALI**

- ✅ **Architettura Ibrida**: Live + Storica + Sync
- ✅ **17 Modelli ML** + **17 Indicatori Tecnici**
- ✅ **Sincronizzazione Automatica** Render ↔️ Locale
- ✅ **Multi-Threading** per performance
- ✅ **Cache Multi-Layer** per ottimizzazione
- ✅ **Report Programmati** automatici
- ✅ **Dashboard Multiple** (555 + Wallet)

---

**Versione:** 2.0  
**Ultima Modifica:** 16 Agosto 2025  
**Developed by:** Valen555  
**Tech Stack:** Python + Dash + Pandas + Scikit-learn + FRED API + CryptoCompare API
