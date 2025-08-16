# 📊 Dashboard 555 - Sistema Analisi Finanziaria Completo

<div align="center">

![Dashboard 555](https://img.shields.io/badge/Dashboard-555-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Dash](https://img.shields.io/badge/Dash-Plotly-orange?style=for-the-badge&logo=plotly)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

**Sistema professionale di analisi finanziaria multi-asset con 17 indicatori tecnici, 19 modelli ML e report automatici su Telegram**

[🚀 Quick Start](#-quick-start) •
[📊 Features](#-features) •
[🔧 Deployment](#-deployment) •
[📱 PWA Mobile](#-pwa-mobile) •
[🛡️ Privacy](#-privacy-e-sicurezza)

</div>

---

## 🎯 Panoramica

Dashboard 555 è un'infrastruttura completa di analisi finanziaria che integra:

- **17 Indicatori Tecnici** con analisi su tutti i timeframe
- **19 Modelli Machine Learning** per previsioni di mercato con consenso cross-model  
- **Sistema di Report Multi-livello** (giornaliero, settimanale, mensile)
- **Analisi Intelligente Notizie** con ranking automatico TOP 10
- **Analisi ML Eventi Economici** con scoring predittivo automatico
- **Invio Automatico Telegram** con logica temporale ottimizzata
- **Dashboard Web Responsive** con supporto PWA mobile
- **Sistema Dual-Mode** (Locale + Render deployment)

### 🎯 **Asset Monitorati**
- **Dollar Index** (DXY) - Forza dollaro USA
- **S&P 500** - Mercato azionario USA  
- **Gold** - Oro spot USD
- **Bitcoin** - Criptovaluta principale

---

## 🚀 Quick Start

### **Prerequisiti**
- Python 3.8+ installato
- Connessione internet per API finanziarie
- Account Telegram Bot (opzionale per notifiche)

### **Installazione Rapida**

```bash
# 1. Clona il repository
git clone https://github.com/tuousername/dashboard-555.git
cd dashboard-555

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Avvia la dashboard locale (via Google Drive)
doppio clic su "🚀 Lancia 555 Dashboard.bat" 
# oppure manualmente:
python 555.py
```

La dashboard sarà disponibile su: **http://localhost:8050**

### **Prima Configurazione**

1. **Telegram (Opzionale)**:
   ```python
   # Modifica in 555.py o 555-server.py
   TELEGRAM_TOKEN = "il_tuo_bot_token"
   TELEGRAM_CHAT_ID = "@il_tuo_canale"
   ```

2. **API Keys**:
   - FRED API per dati economici (automatica)
   - CryptoCompare per dati crypto (automatica)

---

## ⚙️ Configurazione

### **File Principali**

| File | Descrizione | Uso |
|------|-------------|-----|
| `555.py` | Dashboard principale locale | Principale da Google Drive |
| `555-server.py` | Versione deploy Render | Produzione cloud |
| `555bt.py` | Modulo backtest | Analisi storiche |
| `wallet.py` | Dashboard portafoglio | Gestione wallet |
| `sync_system.py` | Sincronizzazione dati | Sync Drive-cloud |

### **Configurazioni Features**

```python
FEATURES_ENABLED = {
    "scheduled_reports": False,    # Report automatici (da Render)
    "manual_reports": False,       # Invii manuali (da Render)
    "backtest_reports": True,     # Report settimanali (attivi)
    "analysis_reports": False      # Analisi giornaliere (da Render)
}
```

### **Ottimizzazioni Performance**

```python
# performance_config.py
PERFORMANCE_CONFIG = {
    "cache_duration_minutes": 90,
    "max_workers": 6,
    "max_models_for_telegram": 4,
    "enable_parallel_ml": True
}
```

---

## 📁 Struttura Progetto

```
Google Drive/555/
├── 🚀 Lancia 555 Dashboard.bat    # ⭐ SCORCIATOIA PRINCIPALE
├── 555.py                          # 🖥️ Dashboard locale principale
├── 555-server.py                   # ☁️ Versione deploy Render  
├── 555bt.py                        # 📈 Modulo backtest
├── wallet.py                       # 💼 Dashboard portafoglio
├── sync_system.py                  # 🔄 Sistema sincronizzazione
├── performance_config.py           # ⚡ Configurazioni performance
├── twitter_config.py               # 🐦 Configurazioni social (disabilitato)
├── salvataggi/                     # 📁 Dati pubblici (sincronizzati su Drive)
│   ├── segnali_tecnici.csv         # Indicatori tecnici
│   ├── previsioni_ml.csv           # Previsioni ML
│   ├── indicatori_cumulativo.csv   # Storico indicatori
│   ├── previsioni_cumulativo.csv   # Storico previsioni
│   └── analysis_text.txt           # Report backtest
├── assets/                         # 🎨 Risorse statiche
└── requirements.txt                # 📋 Dipendenze Python
```

---

## 🔧 Deployment

### **Google Drive (Principale)**

```bash
# Avvia dashboard dal Drive (raccomandato)
Doppio clic su "🚀 Lancia 555 Dashboard.bat"

# Avvio manuale dal Drive
python H:\Il mio Drive\555\555.py
```

**URLs**:
- Dashboard: http://localhost:8050
- Wallet: http://localhost:8051

### **Render (Produzione Cloud)**

1. **Deploy su Render**:
   ```bash
   # Connetti repository GitHub a Render
   # Render rileverà automaticamente 555-server.py
   ```

2. **Variabili d'Ambiente**:
   ```bash
   PORT=10000
   RENDER_EXTERNAL_URL=https://tua-app.render.com
   TELEGRAM_TOKEN=il_tuo_token
   TELEGRAM_CHAT_ID=@il_tuo_canale
   ```

3. **URL Deploy**: L'app sarà disponibile all'URL fornito da Render

### **Sistema Dual-Mode**

Il sistema può operare simultaneamente in due modalità:

- **Google Drive**: Dashboard interattiva principale con backup automatico
- **Render**: Invio automatico report e monitoraggio continuo (17:05 backup quotidiano)

---

## 📊 Features

### **🔍 Indicatori Tecnici (17)**

| Categoria | Indicatori |
|-----------|------------|
| **Trend** | MAC, EMA, SMA, Ichimoku Cloud |
| **Momentum** | RSI, MACD, Stochastic, CCI, ROC |
| **Volatilità** | Bollinger Bands, ATR, Parabolic SAR |
| **Volume** | OBV, Volume Analysis |
| **Support/Resistance** | Pivot Points, ADX |

### **🤖 Modelli Machine Learning (19)**

| Categoria | Modelli |
|-----------|---------|
| **Ensemble** | Random Forest, Gradient Boosting, XGBoost, AdaBoost, Extra Trees |
| **Lineare** | Logistic Regression, LinearSVC, Ridge, Lasso, ElasticNet |
| **Probabilistico** | Naive Bayes, Bayesian Ridge |
| **Distanza** | K-Nearest Neighbors |
| **Alberi** | Decision Tree |
| **Reti Neurali** | MLP Neural Network |
| **Serie Temporali** | ARIMA, GARCH |
| **Meta** | Ensemble Voting |

### **📅 Sistema Report Automatici**

| Report | Orario | Contenuto |
|--------|--------|-----------|
| **Rassegna Stampa** | 09:00 | Notizie critiche + Analisi sentiment |
| **Report Giornaliero** | 13:00 | 17 indicatori + 19 modelli ML (4 parti) |
| **Report Settimanale** | Lunedì 13:05 | Analisi completa + TOP 10 news + ML calendar |
| **Report Mensile** | 1° mese 13:00 | Sintesi mensile + correlazioni cross-asset |

---

## 📱 PWA Mobile

Dashboard 555 include supporto **Progressive Web App** per uso mobile:

### **Installazione Mobile**

1. **Apri la dashboard** nel browser mobile
2. **Menu browser** → "Aggiungi alla schermata home"
3. **Icona app** apparirà come app nativa

### **Features PWA**

- ✅ **Offline Ready** - Funziona senza connessione
- ✅ **Installabile** - Come app nativa
- ✅ **Responsive Design** - Ottimizzata mobile
- ✅ **Fast Loading** - Cache intelligente
- ✅ **Push Notifications** - Notifiche sistema (futuro)

### **Ottimizzazioni Mobile**

```css
/* CSS Mobile Responsive incluso */
@media (max-width: 479px) {
    .dash-table { font-size: 12px; }
    .indicator-title { max-width: 80px; }
    /* Oltre 50 ottimizzazioni CSS mobile */
}
```

---

## 🔄 Sincronizzazione

### **Sistema Sync Locale-Cloud**

Il sistema include sincronizzazione automatica bidirezionale:

```python
# sync_system.py - Configurazione
sync = SalvataggieSync(
    render_url="https://tua-app.render.com",
    local_path="C:\\Users\\tuo_user\\555\\salvataggi"
)
```

### **Files Sincronizzati**
- `analysis_text.txt` - Analisi giornaliera
- `segnali_tecnici.csv` - Export indicatori
- `previsioni_ml.csv` - Export modelli ML
- `weekly_report_enhanced.txt` - Report settimanale

### **Modalità Sync**
- **Auto**: Sincronizza il file più recente
- **Upload**: Locale → Render
- **Download**: Render → Locale
- **Both**: Sincronizzazione bidirezionale

---

## 🛡️ Privacy e Sicurezza

### **Architettura Dual-Storage**

Dashboard 555 implementa separazione completa dei dati:

```
📁 salvataggi/          # Dati pubblici (condivisi)
   ├── analysis_text.txt
   ├── segnali_tecnici.csv
   └── previsioni_ml.csv

🔐 salvataggiwallet/    # Dati privati (solo locali)
   ├── raccomandazioni_storiche.csv
   ├── performance_storiche.csv
   └── wallet_data.csv
```

### **Calibrazione ML Privacy-Safe**

- ✅ **Dati privati** mai esposti pubblicamente
- ✅ **ML calibrato** con performance storiche personali
- ✅ **Doppio binario** analisi pubblica + calibrazione privata
- ✅ **Feedback loop** sistema apprende dalle performance passate

### **Sicurezza Credenziali**

```python
# Variabili d'ambiente per credenziali sensibili
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', 'default_value')
API_SECRET = os.environ.get('API_SECRET', 'default_value')
```

---

## 🐛 Troubleshooting

### **Problemi Comuni**

#### **1. Dashboard non si avvia**
```bash
# Verifica Python
python --version  # Richiede 3.8+

# Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

#### **2. Errori API dati**
```python
# Controlla connessione internet
# FRED API: automatica, nessuna configurazione
# Crypto API: automatica, rate limit gestito
```

#### **3. Telegram non funziona**
```python
# Verifica configurazione
TELEGRAM_TOKEN = "123456789:ABC..."  # Da BotFather
TELEGRAM_CHAT_ID = "@canale"         # Con @ iniziale
```

#### **4. Render deployment issues**
```bash
# Verifica variabili d'ambiente su Render dashboard:
PORT=10000
RENDER_EXTERNAL_URL=https://tua-app.render.com
```

#### **5. Errori modelli ML**
- **Memory Error**: Riduci `max_datapoints_ml` in performance_config.py
- **Timeout**: Aumenta timeout in `SPEED_TIMEOUTS`
- **Data Error**: Controlla connessione API e cache

### **Log e Debug**

```bash
# Debug dashboard locale
python 555.py --verbose

# Controlla log Render
# Dashboard Render → View Logs
```

### **Performance Issues**

```python
# Ottimizza in performance_config.py
PERFORMANCE_CONFIG = {
    "cache_duration_minutes": 120,  # Cache più lunga
    "max_workers": 4,               # Riduci per meno RAM
    "max_models_for_telegram": 3    # Meno modelli ML
}
```

---

## 🤝 Contributing

### **Come Contribuire**

1. **Fork** il repository
2. **Crea branch** per la tua feature: `git checkout -b feature/nuova-feature`
3. **Commit** le modifiche: `git commit -m 'Aggiunge nuova feature'`
4. **Push** al branch: `git push origin feature/nuova-feature`
5. **Crea Pull Request**

### **Linee Guida**

- ✅ **Testa** sempre le modifiche localmente
- ✅ **Documenta** nuove features nel README
- ✅ **Mantieni** compatibilità con sistema esistente
- ✅ **Segui** lo stile di codice esistente

### **Aree di Contribuzione**

- 🔧 **Nuovi indicatori tecnici**
- 🤖 **Modelli ML aggiuntivi**  
- 📊 **Dashboard UI miglioramenti**
- 📱 **Ottimizzazioni mobile**
- 🌐 **Nuove API finanziarie**
- 📈 **Sistema report avanzati**

---

## 📚 Documentazione

### **Guide Disponibili**

| Documento | Target | Contenuto |
|-----------|--------|-----------|
| **README.md** | 👥 Utenti/Developer | Features, installazione, deployment |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | 🔧 Sviluppatori | Comandi rapidi, configurazioni, debug |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 🏗️ Architettura | Flussi dati, threading, implementazione |

### **Percorso Consigliato**

1. **Primo utilizzo**: Inizia con questo README.md
2. **Sviluppo/Debug**: Usa QUICK_REFERENCE.md
3. **Comprensione sistema**: Consulta ARCHITECTURE.md

---

## 📜 License

Questo progetto è rilasciato sotto **MIT License**.

```
MIT License

Copyright (c) 2025 Dashboard 555

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🔗 Links Utili

- 📊 **Dashboard Demo**: [Live Demo](https://five55-7ozo.onrender.com)
- 📚 **Documentazione Completa**: `DOCUMENTAZIONE_COMPLETA_555.md`
- 🗺️ **Mappa Codice**: `MAPPA_CODICE_555.md`
- 📝 **Changelog**: `RIASSUNTO_555.txt`
- 🧹 **Pulizia Codice**: `APPUNTI_PULIZIA_CODICE.md`

## 📞 Supporto

- 🐛 **Issues**: [GitHub Issues](https://github.com/tuousername/dashboard-555/issues)
- 💬 **Discussioni**: [GitHub Discussions](https://github.com/tuousername/dashboard-555/discussions)
- 📧 **Email**: support@dashboard555.com

---

<div align="center">

**⭐ Se ti è utile, lascia una stella! ⭐**

**Fatto con ❤️ per la community finanziaria**

---

**📊 Dashboard 555** - *Sistema Analisi Finanziaria Completo*

![Footer](https://img.shields.io/badge/Made_with-Python_❤️-red?style=for-the-badge)

</div>
