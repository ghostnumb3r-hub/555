# MAPPA DETTAGLIATA DEL CODICE 555.PY
*Guida di riferimento rapido con numerazione righe - Aggiornato al 09/08/2025*

## 📑 INDICE RAPIDO

- [🔧 CONFIGURAZIONI](#configurazioni) (Righe 1-200)
- [📰 NOTIZIE E EVENTI](#notizie-eventi) (Righe 200-500)  
- [🤖 ANALISI ML](#analisi-ml) (Righe 500-1200)
- [📊 REPORT SETTIMANALE](#report-settimanale) (Righe 1200-1400)
- [📈 INDICATORI TECNICI](#indicatori-tecnici) (Righe 1400-2600)
- [🤖 MODELLI ML](#modelli-ml) (Righe 1800-2900)
- [🎨 INTERFACCIA DASH](#interfaccia-dash) (Righe 2900-4900)
- [⏰ SCHEDULER TELEGRAM](#scheduler-telegram) (Righe 5300-5413)

---

## 🔧 CONFIGURAZIONI
### Righe 1-200: Setup e Configurazioni Base

```python
# Riga 1-15: Import principali
# Riga 16-30: Ottimizzazioni performance CIAO4
# Riga 31-48: Configurazione Twitter (disabilitata)
# Riga 50-63: Funzione creazione cartelle
# Riga 65-72: Setup Dash e Telegram
# Riga 74-79: ⭐ FEATURES_ENABLED - CONTROLLO FUNZIONI PRINCIPALI
# Riga 81-129: Funzioni controllo features e override temporaneo
# Riga 130-172: ⭐ FUNZIONE INVIO TELEGRAM PRINCIPALE
# Riga 174-198: Setup eventi base
```

**🎯 PUNTI CHIAVE:**
- **Riga 74**: `FEATURES_ENABLED` - On/Off per tutte le funzioni
- **Riga 130**: `invia_messaggio_telegram()` - Funzione invio principale
- **Riga 69-70**: Token e Chat ID Telegram

---

## 📰 NOTIZIE E EVENTI  
### Righe 200-500: Sistema Notizie e Feed RSS

```python
# Riga 200-246: ⭐ RSS_FEEDS - Configurazione feed notizie
# Riga 248-356: ⭐ get_notizie_critiche() - Recupero notizie critiche
# Riga 358-495: genera_messaggio_eventi() - Creazione messaggi eventi
# Riga 496-550: genera_messaggio_eventi_legacy() - Versione legacy
```

**🎯 PUNTI CHIAVE:**
- **Riga 200**: `RSS_FEEDS` - Tutti i feed RSS per categoria
- **Riga 248**: `get_notizie_critiche()` - Engine notizie critiche
- **Riga 262**: Keywords per notizie critiche (lista completa)
- **Riga 389**: `genera_messaggio_eventi()` - Formattazione eventi

---

## 🤖 ANALISI ML
### Righe 500-1200: Machine Learning e Analisi Intelligente

```python
# Riga 552-700: ⭐ analyze_calendar_events_with_ml() - ML Calendario
# Riga 702-862: generate_ml_comment_for_event() - Commenti ML eventi
# Riga 864-962: generate_ml_comment_for_news() - Commenti ML notizie  
# Riga 963-1166: ⭐ analyze_news_sentiment_and_impact() - Sentiment Analysis
```

**🎯 PUNTI CHIAVE:**
- **Riga 552**: Analisi ML calendario economico completa
- **Riga 702**: Generatore commenti ML per eventi
- **Riga 963**: Analisi sentiment notizie con ML
- **Riga 987**: Keywords sentiment (positive/negative)

---

## 📊 REPORT SETTIMANALE
### Righe 1200-1400: Sistema Report Settimanale Avanzato

```python
# Riga 1168-1356: ⭐ generate_weekly_backtest_summary() - REPORT SETTIMANALE PRINCIPALE
#   Riga 1177-1223: Sezione Indicatori Tecnici (17 indicatori)
#   Riga 1227-1330: Sezione Modelli ML (19 modelli)
#   Riga 1334-1380: ⭐ TOP 10 Notizie Critiche con Ranking
#   Riga 1382-1400: ⭐ Analisi ML Eventi Calendario Economico
```

**🎯 PUNTI CHIAVE:**
- **Riga 1168**: `generate_weekly_backtest_summary()` - FUNZIONE PRINCIPALE
- **Riga 1334**: TOP 10 notizie con ranking automatico  
- **Riga 1382**: Analisi ML eventi con scoring di impatto
- **Riga 1189**: Lista completa 17 indicatori tecnici

---

## 📈 INDICATORI TECNICI
### Righe 1400-2600: Sistema Completo Indicatori Tecnici

```python
# Riga 1465-1483: Callback aggiornamento tabelle
# Riga 1880-1937: ⭐ CONFIGURAZIONE ML - Modelli e orizzonti
# Riga 1938-1957: Initialize model functions
# Riga 2145-2175: Helper functions date
# Riga 2176-2245: ⭐ SISTEMA CACHE AVANZATO
# Riga 2246-2363: Load data functions (FRED/Crypto)
# Riga 2364-2590: ⭐ CALCOLO TUTTI I 17 INDICATORI TECNICI
#   Riga 2385: calculate_sma()
#   Riga 2395: calculate_mac() 
#   Riga 2405: calculate_rsi()
#   Riga 2418: calculate_macd()
#   Riga 2430: calculate_bollinger_bands()
#   Riga 2442: calculate_stochastic_oscillator()
#   Riga 2454: calculate_atr()
#   Riga 2465: calculate_ema()
#   Riga 2475: calculate_cci()
#   Riga 2487: calculate_momentum()
#   Riga 2496: calculate_roc()
#   Riga 2505: calculate_adx()
#   Riga 2519: calculate_obv()
#   Riga 2531: calculate_ichimoku()
#   Riga 2553: calculate_parabolic_sar()
#   Riga 2576: calculate_pivot_points()
```

**🎯 PUNTI CHIAVE:**
- **Riga 2364**: `calculate_technical_indicators()` - Funzione master
- **Riga 2385-2576**: Tutte le 17 funzioni indicatori singoli
- **Riga 2611**: `get_all_signals_summary()` - Riassunto segnali
- **Riga 2176**: Sistema cache per performance

---

## 🤖 MODELLI ML
### Righe 1800-2900: Sistema Machine Learning Completo

```python
# Riga 1879: ⭐ CONFIGURAZIONE ML PRINCIPALE
# Riga 1880-1937: Simboli, orizzonti, export config
# Riga 1938-2144: ⭐ DEFINIZIONE 19 MODELLI ML
#   RandomForest, XGBoost, Gradient Boosting, Logistic Regression,
#   SVM, KNN, Naive Bayes, AdaBoost, Extra Trees, Neural Network,
#   Ensemble Voting, LSTM, GRU, ARIMA, GARCH
# Riga 2596-2610: Feature engineering ML
# Riga 2647-2856: ⭐ train_model() - FUNZIONE TRAINING PRINCIPALE
```

**🎯 PUNTI CHIAVE:**
- **Riga 1879**: Configurazione completa modelli ML
- **Riga 1938**: Dizionario con tutti i 19 modelli
- **Riga 2647**: `train_model()` - Funzione training universale
- **Riga 2596**: `calculate_ml_features()` - Feature engineering

---

## 🎨 INTERFACCIA DASH
### Righe 2900-4900: Interface Utente e Dashboard

```python
# Riga 2891-3092: ⭐ LAYOUT PRINCIPALE DASH
# Riga 3093-3207: Callback tab principali (Calendario/Notizie)
# Riga 3208-3261: Toggle collapse sections
# Riga 3262-3305: Update dashboard indicatori
# Riga 3306-3771: ⭐ update_all() - CALLBACK PRINCIPALE ML
# Riga 3772-3795: Callback Telegram buttons
# Riga 3796-4018: ⭐ send_backtest_manual() - BACKTEST MANUALE
# Riga 4020-4036: send_unified_report_manual() - REPORT MANUALE
# Riga 4037-4884: ⭐ generate_unified_report() - GENERATORE REPORT UNIFICATO
# Riga 4885-4935: send_analysis_text_message() - Invio analysis.txt
```

**🎯 PUNTI CHIAVE:**
- **Riga 2891**: Layout completo dashboard Dash
- **Riga 3306**: `update_all()` - Callback principale per ML
- **Riga 3796**: `send_backtest_manual()` - Pulsante backtest
- **Riga 4037**: `generate_unified_report()` - Report giornaliero 12:30

---

## ⏰ SCHEDULER TELEGRAM
### Righe 5300-5413: Sistema Invii Automatici

```python
# Riga 5310-5402: ⭐ schedule_telegram_reports() - SCHEDULER PRINCIPALE
#   Riga 5320-5360: Invio report settimanale (Lunedì 12:45)
#   Riga 5362-5375: Invio report mensile (1° mese 13:00) 
#   Riga 5377-5401: ⭐ Invio report giornaliero (12:30)
# Riga 5403-5413: Avvio thread scheduler e server
```

**🎯 PUNTI CHIAVE:**
- **Riga 5310**: `schedule_telegram_reports()` - SCHEDULER MASTER
- **Riga 5320**: Report settimanale Lunedì 12:45
- **Riga 5377**: Report giornaliero 12:30 (trigger principale)
- **Riga 5404**: Avvio thread scheduler

---

## 🔍 FUNZIONI DI RICERCA RAPIDA

### Per trovare velocemente:

**🎯 Configurazioni principali:**
- `FEATURES_ENABLED` → Riga 74
- `RSS_FEEDS` → Riga 200
- `models` (19 modelli ML) → Riga 1938

**🎯 Funzioni invio Telegram:**
- `invia_messaggio_telegram()` → Riga 130
- `generate_unified_report()` → Riga 4037
- `send_backtest_manual()` → Riga 3796

**🎯 Analisi e ML:**
- `analyze_calendar_events_with_ml()` → Riga 552
- `analyze_news_sentiment_and_impact()` → Riga 963
- `generate_weekly_backtest_summary()` → Riga 1168

**🎯 Indicatori tecnici:**
- `calculate_technical_indicators()` → Riga 2364
- Lista completa 17 indicatori → Righe 2385-2576
- `get_all_signals_summary()` → Riga 2611

**🎯 Scheduler automatico:**
- `schedule_telegram_reports()` → Riga 5310
- Trigger 12:30 → Riga 5377
- Report settimanale → Riga 5320

---

## 📋 CHECKLIST MODIFICHE RAPIDE

### Per modificare funzionalità:
- **✅ Abilitare/Disabilitare invii** → Riga 74 `FEATURES_ENABLED`
- **✅ Aggiungere feed RSS** → Riga 200 `RSS_FEEDS`
- **✅ Modificare orari scheduler** → Righe 5320, 5377, 5362
- **✅ Aggiungere indicatori** → Riga 2364 + nuova funzione
- **✅ Modificare modelli ML** → Riga 1938 `models`

### Per debugging:
- **🔍 Errori invio Telegram** → Cerca "❌ [Telegram]"
- **🔍 Errori ML** → Cerca "❌ [ML]" o "❌ [UNIFIED]"
- **🔍 Errori scheduler** → Cerca "❌ [SCHEDULER]"

---

*📝 Questa mappa ti permetterà di navigare velocemente nel codice senza perdere tempo a cercare funzioni specifiche!*
