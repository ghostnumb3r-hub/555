# 📡 ARCHITETTURA MESSAGING SISTEMA 555

**Aggiornato:** 15 Agosto 2025  
**Status:** Deploy Render Attivo

---

## 🏗️ **STRUTTURA ATTUALE**

### 🌐 **555-server.py (Render Deploy)**
**Responsabilità:** Messaggi automatici programmati

#### 📅 **Scheduler Attivo:**
- 🌅 **09:00** - Rassegna stampa mattutina completa
  - Top notizie internazionali (20-30 articoli)
  - Analisi ML sentiment notizie
  - Indicatori tecnici principali
  - Consenso modelli ML
- 📊 **13:00** - Report giornaliero unificato (4 messaggi separati)
  - MSG 1: Indicatori + ML + Confronto
  - MSG 2: Notizie critiche (24h)
  - MSG 3: Analisi ML notizie dettagliata
  - MSG 4: Calendario + Analisi ML calendario

#### 🔧 **Funzionalità Attive:**
- ✅ Keep-alive intelligente (07:45-22:00)
- ✅ API sync endpoints `/api/files-info`, `/api/download`, `/api/upload`
- ✅ Progressive Web App (PWA)
- ✅ Adaptive message splitter
- ✅ Elaborazione sequenziale RAM-friendly
- ✅ Cache persistente con scadenza

#### ❌ **Funzionalità RIMOSSE:**
- ❌ Pulsanti invio manuale Telegram
- ❌ Callbacks `send-backtest-button`
- ❌ Callbacks `send-unified-report-button`
- ❌ Callbacks `send-morning-briefing-button`

---

### 💻 **Sistema Locale (555.py/555bt.py)**
**Responsabilità:** Analisi avanzate e file generation

#### 📊 **Operazioni Locali:**
- 🗓️ **Lunedì** - Report settimanale avanzato
- 📈 **Backtest analysis** (555bt.py) - Generazione analysis_text.txt
- 💾 **File CSV** - Segnali tecnici, previsioni ML
- 📝 **Portfolio analysis** - Analisi portafoglio dettagliata
- 🔄 **Sync con server** - Upload file via API

#### 🔗 **Comunicazione con Server:**
- Upload `analysis_text.txt` → Server per inclusione in report
- Upload CSV files → Server per dashboard
- Download configurazioni → Server per sync settings

---

## ⚠️ **DATI OBSOLETI DA RIMUOVERE**

### 🗑️ **Nel Codice:**
- [ ] Tutti i riferimenti alle **18:00** (non più utilizzati)
- [ ] Tutti i riferimenti alle **08:00** (cambiato in 09:00)
- [ ] Variabile `fixed_time = "18:00:00"` (linea 5989)
- [ ] Commenti obsoleti su orari non più validi
- [ ] Callback functions per pulsanti manuali (già rimossi)
- [ ] Logica di invio duplicata tra sistemi

### 📝 **Nella Documentazione:**
- [ ] Aggiornare tutti i README con orari corretti
- [ ] Rimuovere riferimenti a funzionalità manuali
- [ ] Aggiornare diagrammi architettura

---

## 📋 **ORARI DEFINITIVI**

### ✅ **CONFERMATI:**
- 🌅 **09:00** - Rassegna stampa (555-server.py)
- 📊 **13:00** - Report giornaliero (555-server.py)
- 🗓️ **Lunedì** - Report settimanale (sistema locale)

### ❌ **NON ESISTONO PIÙ:**
- ~~18:00 - Report serale~~ (RIMOSSO)
- ~~08:00 - Briefing mattutino~~ (SPOSTATO a 09:00)
- ~~12:55 - Pre-report~~ (INTEGRATO in 13:00)

---

## 🔄 **FLUSSO MESSAGGI TIPO**

### 📅 **Giorno Tipo (es. Martedì):**
```
09:00 → Server invia Rassegna Stampa
13:00 → Server invia Report Giornaliero (4 MSG)
```

### 📅 **Lunedì:**
```
09:00 → Server invia Rassegna Stampa
13:00 → Server invia Report Giornaliero (4 MSG)
13:05 → Locale genera Report Settimanale (se abilitato)
```

---

## 🛠️ **PROSSIMI PASSI**

1. ✅ **Deploy Render** completato
2. 🔄 **Monitor deployment** (primo giorno)
3. 🧹 **Pulizia codice obsoleto**
4. 📝 **Update documentazione**
5. 🔧 **Ottimizzazioni RAM** (se necessarie)

---

## 📞 **CONTATTI TELEGRAM**

- **Channel:** @abkllr
- **Chat ID:** @abkllr  
- **Token:** Configurato in environment

---

**Note:** Questo documento deve essere aggiornato ad ogni modifica dell'architettura.
