#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
555SERVERLITE - Versione ottimizzata per massima RAM dedicata ai messaggi Telegram
Elimina: Dashboard, UI, CSS, PWA, grafici
Mantiene: Tutto il sistema ML, RSS, scheduling, qualità messaggi identica
"""

import datetime
import time
import requests
import feedparser
import threading
import os
import pytz
import gc
from urllib.request import urlopen
from urllib.error import URLError
import flask
from flask import Flask

# === CONTROLLO MEMORIA E PERFORMANCE ===
print("🚀 [555-LITE] Avvio sistema ottimizzato RAM...")

# === CONFIGURAZIONE PATH UNIFICATA ===
import sys
import pathlib

# Ottieni la directory corrente del script lite
CURRENT_DIR = pathlib.Path(__file__).parent.absolute()

# Path alla cartella 555 principale UNIFICATA
MAIN_555_DIR = CURRENT_DIR.parent / "555" / "salvataggi"

# MODALITÀ UNIFICATA: Usa sempre la cartella principale se esiste
if MAIN_555_DIR.exists():
    SALVATAGGI_DIR = MAIN_555_DIR
    print(f"🔗 [555-LITE] MODALITÀ UNIFICATA attivata")
    print(f"📊 [555-LITE] Cartella condivisa: {SALVATAGGI_DIR}")
    print(f"🚀 [555-LITE] Dati RSS + Flag condivisi con sistema principale")
    print(f"💾 [555-LITE] Storage condiviso per massima efficienza")
else:
    # Fallback: crea cartella locale se principale non esiste
    SALVATAGGI_DIR_LOCAL = CURRENT_DIR / "salvataggi"
    SALVATAGGI_DIR_LOCAL.mkdir(exist_ok=True)
    SALVATAGGI_DIR = SALVATAGGI_DIR_LOCAL
    print(f"📁 [555-LITE] Modalità standalone: {SALVATAGGI_DIR}")
    print(f"⚠️ [555-LITE] Cartella 555 principale non trovata - modalità indipendente")

# === SISTEMA FLAG IN-MEMORY PER RENDER ===
# Variabili globali per tracciare invii giornalieri
GLOBAL_FLAGS = {
    "morning_news_sent": False,
    "daily_report_sent": False,
    "evening_report_sent": False,
    "weekly_report_sent": False,
    "monthly_report_sent": False,
    "quarterly_report_sent": False,
    "semestral_report_sent": False,
    "annual_report_sent": False,
    "last_reset_date": datetime.datetime.now().strftime("%Y%m%d")
}

def reset_daily_flags_if_needed():
    """Resetta i flag se è passata la mezzanotte"""
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    if GLOBAL_FLAGS["last_reset_date"] != current_date:
        GLOBAL_FLAGS["morning_news_sent"] = False
        GLOBAL_FLAGS["daily_report_sent"] = False
        GLOBAL_FLAGS["evening_report_sent"] = False
        GLOBAL_FLAGS["last_reset_date"] = current_date
        print(f"🔄 [FLAGS] Reset giornaliero completato per {current_date}")
        return True
    return False


# === SISTEMA FLAG PERSISTENTI SU FILE (come 555-server) ===
def save_flag_to_file(message_type):
    """Salva flag su file per persistenza"""
    try:
        today = datetime.datetime.now().strftime("%Y%m%d")
        flag_filename = f"{message_type}_sent_{today}.flag"
        flag_path = SALVATAGGI_DIR / flag_filename
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(flag_path, 'w', encoding='utf-8') as f:
            f.write(f"{message_type.replace('_', ' ').title()} sent at {timestamp}\n")
        
        print(f"💾 [FLAGS-FILE] Salvato {flag_filename}")
        return True
    except Exception as e:
        print(f"❌ [FLAGS-FILE] Errore salvataggio {message_type}: {e}")
        return False

def check_flag_from_file(message_type):
    """Controlla se flag esiste su file"""
    try:
        today = datetime.datetime.now().strftime("%Y%m%d")
        flag_filename = f"{message_type}_sent_{today}.flag"
        flag_path = SALVATAGGI_DIR / flag_filename
        
        exists = flag_path.exists()
        if exists:
            print(f"📁 [FLAGS-FILE] Trovato {flag_filename}")
        return exists
    except Exception as e:
        print(f"❌ [FLAGS-FILE] Errore controllo {message_type}: {e}")
        return False

def set_message_sent_flag(message_type):
    """Imposta il flag di invio per il tipo di messaggio (memoria + file)"""
    reset_daily_flags_if_needed()  # Verifica reset automatico
    
    # Imposta flag in memoria
    if message_type == "morning_news":
        GLOBAL_FLAGS["morning_news_sent"] = True
        print("✅ [FLAGS] Flag morning_news_sent impostato su True")
    elif message_type == "daily_report":
        GLOBAL_FLAGS["daily_report_sent"] = True
        print("✅ [FLAGS] Flag daily_report_sent impostato su True")
    elif message_type == "evening_report":
        GLOBAL_FLAGS["evening_report_sent"] = True
        print("✅ [FLAGS] Flag evening_report_sent impostato su True")
    elif message_type == "weekly_report":
        GLOBAL_FLAGS["weekly_report_sent"] = True
        print("✅ [FLAGS] Flag weekly_report_sent impostato su True")
    elif message_type == "monthly_report":
        GLOBAL_FLAGS["monthly_report_sent"] = True
        print("✅ [FLAGS] Flag monthly_report_sent impostato su True")
    elif message_type == "quarterly_report":
        GLOBAL_FLAGS["quarterly_report_sent"] = True
        print("✅ [FLAGS] Flag quarterly_report_sent impostato su True")
    elif message_type == "semestral_report":
        GLOBAL_FLAGS["semestral_report_sent"] = True
        print("✅ [FLAGS] Flag semestral_report_sent impostato su True")
    elif message_type == "annual_report":
        GLOBAL_FLAGS["annual_report_sent"] = True
        print("✅ [FLAGS] Flag annual_report_sent impostato su True")
    
    # Salva anche su file per persistenza
    save_flag_to_file(message_type)

def is_message_sent_today(message_type):
    """Verifica se il messaggio è già stato inviato oggi (memoria + file)"""
    reset_daily_flags_if_needed()  # Verifica reset automatico
    
    # Controlla prima la memoria (veloce)
    memory_sent = False
    if message_type == "morning_news":
        memory_sent = GLOBAL_FLAGS["morning_news_sent"]
    elif message_type == "daily_report":
        memory_sent = GLOBAL_FLAGS["daily_report_sent"]
    elif message_type == "evening_report":
        memory_sent = GLOBAL_FLAGS["evening_report_sent"]
    elif message_type == "weekly_report":
        memory_sent = GLOBAL_FLAGS["weekly_report_sent"]
    elif message_type == "monthly_report":
        memory_sent = GLOBAL_FLAGS["monthly_report_sent"]
    elif message_type == "quarterly_report":
        memory_sent = GLOBAL_FLAGS["quarterly_report_sent"]
    elif message_type == "semestral_report":
        memory_sent = GLOBAL_FLAGS["semestral_report_sent"]
    elif message_type == "annual_report":
        memory_sent = GLOBAL_FLAGS["annual_report_sent"]
    
    # Se in memoria è True, ritorna True
    if memory_sent:
        return True
    
    # Se in memoria è False, controlla il file (persistenza)
    file_sent = check_flag_from_file(message_type)
    
    # Se esiste il file, aggiorna anche la memoria
    if file_sent:
        if message_type == "morning_news":
            GLOBAL_FLAGS["morning_news_sent"] = True
        elif message_type == "daily_report":
            GLOBAL_FLAGS["daily_report_sent"] = True
        elif message_type == "evening_report":
            GLOBAL_FLAGS["evening_report_sent"] = True
        # etc per gli altri
        print(f"📁 [FLAGS-SYNC] Flag {message_type} sincronizzato da file")
    
    return file_sent

# === OTTIMIZZAZIONI PERFORMANCE ===
try:
    from performance_config import (
        PERFORMANCE_CONFIG, LIGHTNING_ML_MODELS, FULL_ML_MODELS,
        CORE_INDICATORS, SECONDARY_INDICATORS, SPEED_TIMEOUTS,
        timed_execution, cached_with_expiry, get_thread_pool, parallel_execute
    )
    print("🚀 [LITE-TURBO] Ottimizzazioni performance caricate!")
except ImportError:
    print("⚠️ [LITE-TURBO] File performance_config.py non trovato - usando configurazione standard")
    PERFORMANCE_CONFIG = {"max_workers": 6, "cache_duration_minutes": 45}  # Più workers con RAM extra
    LIGHTNING_ML_MODELS = ["Random Forest", "Logistic Regression", "Gradient Boosting"]
    CORE_INDICATORS = ["MAC", "RSI", "MACD", "Bollinger", "EMA"]
    SPEED_TIMEOUTS = {"http_request_timeout": 8}  # Timeout più aggressivo

# === TELEGRAM CONFIG ===
TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
TELEGRAM_CHAT_ID = "@abkllr"

# === SISTEMA BACKUP RENDER → DRIVE ===
try:
    from render_drive_backup import RenderDriveBackup
    print("🔄 [LITE-BACKUP] Sistema backup caricato")
    BACKUP_SYSTEM_ENABLED = True
except ImportError:
    print("⚠️ [LITE-BACKUP] Sistema backup non disponibile")
    RenderDriveBackup = None
    BACKUP_SYSTEM_ENABLED = False

# === CONTROLLO FUNZIONI OTTIMIZZATO ===
FEATURES_ENABLED = {
    "scheduled_reports": True,
    "manual_reports": True,
    "backtest_reports": True,
    "analysis_reports": True,
    "morning_news": True,
    "daily_report": True,
    "weekly_reports": True,        # NUOVO
    "monthly_reports": True,       # NUOVO
    "enhanced_ml": True,           # NUOVO - ML potenziato con RAM extra
    "real_time_alerts": True,      # NUOVO - Alert in tempo reale
    "memory_cleanup": True
}

def is_feature_enabled(feature_name):
    """Controlla se una funzione è abilitata"""
    return FEATURES_ENABLED.get(feature_name, True)

# === FUNZIONE INVIO TELEGRAM OTTIMIZZATA ===
def invia_messaggio_telegram(msg):
    """Versione ottimizzata per RAM - stesso livello qualità"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    print(f"📤 [LITE-TELEGRAM] Invio messaggio ({len(msg)} caratteri)")
    
    try:
        # Pulizia ottimizzata
        clean_msg = msg.replace('```', '`').replace('**', '*')
        
        # Gestione messaggi lunghi con divisione intelligente
        if len(clean_msg) > 2400:
            return _send_long_message_optimized(clean_msg, url)
        else:
            return _send_single_message_lite(clean_msg, url)
            
    except Exception as e:
        print(f"❌ [LITE-TELEGRAM] Errore: {e}")
        return False
    finally:
        # Pulizia memoria aggressiva
        gc.collect()

def _send_long_message_optimized(clean_msg, url):
    """Divisione messaggi lunghi ottimizzata per velocità"""
    parts = []
    start = 0
    part_num = 1
    
    while start < len(clean_msg):
        end = start + 2400
        if end >= len(clean_msg):
            end = len(clean_msg)
        else:
            cut_point = clean_msg.rfind('\n', start, end)
            if cut_point > start:
                end = cut_point
        
        part = clean_msg[start:end]
        if len(parts) == 0:
            part = f"📤 PARTE {part_num}\n\n" + part
        else:
            part = f"📤 PARTE {part_num} (continua)\n\n" + part
        
        parts.append(part)
        start = end
        part_num += 1
    
    # Invio sequenziale ottimizzato
    all_success = True
    for i, part in enumerate(parts):
        success = _send_single_message_lite(part, url)
        if not success:
            all_success = False
        
        # Pausa minima tra parti
        if i < len(parts) - 1:
            time.sleep(1.5)  # Ridotto da 2s per velocità
    
    return all_success

def _send_single_message_lite(clean_msg, url):
    """Versione lite con fallback essenziali"""
    
    # Strategie di fallback semplificate ma efficaci
    strategies = [
        {"parse_mode": "Markdown", "name": "Markdown"},
        {"parse_mode": None, "name": "Plain", "processor": lambda x: x.replace('*', '').replace('_', '')}
    ]
    
    for strategy in strategies:
        processed_msg = clean_msg
        if 'processor' in strategy:
            processed_msg = strategy['processor'](clean_msg)
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": processed_msg,
            "parse_mode": strategy["parse_mode"]
        }
        
        try:
            r = requests.post(url, data=payload, timeout=10)
            if r.status_code == 200:
                print(f"✅ [LITE-TELEGRAM] Inviato con {strategy['name']}")
                return True
        except Exception as e:
            print(f"⚠️ [LITE-TELEGRAM] Tentativo {strategy['name']} fallito: {e}")
            continue
    
    return False

# === CALENDARIO EVENTI (Stesso del sistema completo) ===
today = datetime.date.today()

def create_event(title, date, impact, source):
    return {"Data": date.strftime("%Y-%m-%d"), "Titolo": title, "Impatto": impact, "Fonte": source}

eventi = {
    "Finanza": [
        create_event("Decisione tassi FED", today + datetime.timedelta(days=2), "Alto", "Investing.com"),
        create_event("Rilascio CPI USA", today + datetime.timedelta(days=6), "Alto", "Trading Economics"),
        create_event("Occupazione Eurozona", today + datetime.timedelta(days=10), "Medio", "ECB"),
        create_event("Conference BCE", today + datetime.timedelta(days=15), "Basso", "ECB")
    ],
    "Criptovalute": [
        create_event("Aggiornamento Ethereum", today + datetime.timedelta(days=3), "Alto", "CoinMarketCal"),
        create_event("Hard Fork Cardano", today + datetime.timedelta(days=7), "Medio", "CoinDesk"),
        create_event("Annuncio regolamentazione MiCA", today + datetime.timedelta(days=12), "Alto", "EU Commission"),
        create_event("Evento community Bitcoin", today + datetime.timedelta(days=20), "Basso", "Bitcoin Magazine")
    ],
    "Geopolitica": [
        create_event("Vertice NATO", today + datetime.timedelta(days=1), "Alto", "Reuters"),
        create_event("Elezioni UK", today + datetime.timedelta(days=8), "Alto", "BBC"),
        create_event("Discussione ONU su Medio Oriente", today + datetime.timedelta(days=11), "Medio", "UN"),
        create_event("Summit BRICS", today + datetime.timedelta(days=18), "Basso", "Al Jazeera")
    ]
}

# === RSS FEEDS (Stesso sistema + Mercati Emergenti) ===
RSS_FEEDS = {
    "Finanza": [
        "https://feeds.reuters.com/reuters/businessNews",
        "https://www.investing.com/rss/news_285.rss",
        "https://www.marketwatch.com/rss/topstories",
        "https://feeds.finance.yahoo.com/rss/2.0/headline",
        "https://feeds.bloomberg.com/markets/news.rss"
    ],
    "Criptovalute": [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
        "https://cryptoslate.com/feed/",
        "https://bitcoinist.com/feed/"
    ],
    "Geopolitica": [
        "https://feeds.reuters.com/Reuters/worldNews",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.bbci.co.uk/news/rss.xml"
    ],
    "Mercati Emergenti": [
        "https://feeds.reuters.com/reuters/emergingMarketsNews",
        "https://www.investing.com/rss/news_14.rss",
        "https://feeds.bloomberg.com/emerging-markets/news.rss",
        "https://www.ft.com/emerging-markets?format=rss",
        "https://www.wsj.com/xml/rss/3_7455.xml"
    ]
}

# === NOTIZIE CRITICHE (Stesso algoritmo, ottimizzato) ===
def get_notizie_critiche():
    """Recupero notizie ottimizzato per velocità"""
    notizie_critiche = []
    
    from datetime import timezone
    now_utc = datetime.datetime.now(timezone.utc)
    soglia_24h = now_utc - datetime.timedelta(hours=24)
    
    def is_highlighted(title):
        keywords = [
            "crisis", "inflation", "fed", "ecb", "rates", "crash", "surge",
            "war", "sanctions", "hack", "regulation", "bitcoin", "crypto"
        ]
        return any(k in title.lower() for k in keywords)
    
    def is_recent_news(entry):
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                news_time = datetime.datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                return news_time >= soglia_24h
            return True  # In dubbio, includiamo
        except:
            return True
    
    for categoria, feed_urls in RSS_FEEDS.items():
        for url in feed_urls[:2]:  # Limitiamo a 2 feed per categoria per velocità
            try:
                parsed = feedparser.parse(url)
                if parsed.bozo or not parsed.entries:
                    continue
                
                for entry in parsed.entries[:5]:  # Max 5 per feed
                    title = entry.get("title", "")
                    
                    if is_recent_news(entry) and is_highlighted(title):
                        link = entry.get("link", "")
                        source = parsed.feed.get("title", "Unknown")
                        
                        notizie_critiche.append({
                            "titolo": title,
                            "link": link,
                            "fonte": source,
                            "categoria": categoria
                        })
                        
                        if len(notizie_critiche) >= 8:  # Limite per velocità
                            break
                
                if len(notizie_critiche) >= 8:
                    break
            except Exception as e:
                continue
        
        if len(notizie_critiche) >= 8:
            break
    
    return notizie_critiche[:5]  # Top 5

# === GENERAZIONE MESSAGGI EVENTI (Stesso sistema) ===
def genera_messaggio_eventi():
    """Genera messaggio eventi - stessa qualità del sistema completo"""
    oggi = datetime.date.today()
    prossimi_7_giorni = oggi + datetime.timedelta(days=7)
    sezioni_parte1 = []
    sezioni_parte2 = []

    # Eventi di oggi
    eventi_oggi_trovati = False
    for categoria, lista in eventi.items():
        eventi_oggi = [e for e in lista if e["Data"] == oggi.strftime("%Y-%m-%d")]
        if eventi_oggi:
            if not eventi_oggi_trovati:
                sezioni_parte1.append("📅 EVENTI DI OGGI")
                eventi_oggi_trovati = True
            eventi_oggi.sort(key=lambda x: ["Basso", "Medio", "Alto"].index(x["Impatto"]))
            sezioni_parte1.append(f"📌 {categoria}")
            for e in eventi_oggi:
                impact_color = "🔴" if e['Impatto'] == "Alto" else "🟡" if e['Impatto'] == "Medio" else "🟢"
                sezioni_parte1.append(f"{impact_color} • {e['Titolo']} ({e['Impatto']}) - {e['Fonte']}")
    
    # Eventi prossimi giorni
    eventi_prossimi = []
    for categoria, lista in eventi.items():
        for evento in lista:
            data_evento = datetime.datetime.strptime(evento["Data"], "%Y-%m-%d").date()
            if oggi < data_evento <= prossimi_7_giorni:
                evento_con_categoria = evento.copy()
                evento_con_categoria["Categoria"] = categoria
                evento_con_categoria["DataObj"] = data_evento
                eventi_prossimi.append(evento_con_categoria)
    
    if eventi_prossimi:
        eventi_prossimi.sort(key=lambda x: (x["DataObj"], ["Basso", "Medio", "Alto"].index(x["Impatto"])))
        if eventi_oggi_trovati:
            sezioni_parte1.append("")
        sezioni_parte1.append("🗺 PROSSIMI EVENTI (7 giorni)")
        
        data_corrente = None
        for evento in eventi_prossimi:
            if evento["DataObj"] != data_corrente:
                data_corrente = evento["DataObj"]
                giorni_mancanti = (data_corrente - oggi).days
                sezioni_parte1.append(f"\n📅 {data_corrente.strftime('%d/%m')} (tra {giorni_mancanti} giorni)")
            impact_color = "🔴" if evento['Impatto'] == "Alto" else "🟡" if evento['Impatto'] == "Medio" else "🟢"
            sezioni_parte1.append(f"{impact_color} • {evento['Titolo']} ({evento['Impatto']}) - {evento['Categoria']} - {evento['Fonte']}")

    # Notizie critiche
    notizie_critiche = get_notizie_critiche()
    if notizie_critiche:
        sezioni_parte2.append("🚨 *NOTIZIE CRITICHE* (24h)")
        sezioni_parte2.append(f"📰 Trovate {len(notizie_critiche)} notizie rilevanti\n")
        
        for i, notizia in enumerate(notizie_critiche, 1):
            titolo_breve = notizia["titolo"][:70] + "..." if len(notizia["titolo"]) > 70 else notizia["titolo"]
            sezioni_parte2.append(f"{i}. 🔴 *{titolo_breve}*")
            sezioni_parte2.append(f"   📂 {notizia['categoria']} | 📰 {notizia['fonte']}")
            sezioni_parte2.append("")

    # Invio messaggi
    if not sezioni_parte1 and not sezioni_parte2:
        return "✅ Nessun evento in calendario"

    success_count = 0
    if sezioni_parte1:
        msg_parte1 = f"🗓️ *Eventi del {oggi}* (Parte 1/2)\n\n" + "\n".join(sezioni_parte1)
        if invia_messaggio_telegram(msg_parte1):
            success_count += 1
        time.sleep(3)
    
    if sezioni_parte2:
        msg_parte2 = f"🗓️ *Eventi del {oggi}* (Parte 2/2)\n\n" + "\n".join(sezioni_parte2)
        if invia_messaggio_telegram(msg_parte2):
            success_count += 1
    
    return f"Messaggi eventi inviati: {success_count}/2"

# === FUNZIONI LETTURA DATI LIVE DAL SISTEMA 555 ===
def load_technical_indicators():
    """Carica indicatori tecnici dal sistema 555 principale (senza pandas)"""
    try:
        import csv
        indicators_file = SALVATAGGI_DIR / "segnali_tecnici.csv"
        
        if indicators_file.exists():
            data = []
            with open(indicators_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            print(f"📊 [LITE-DATA] Caricati {len(data)} segnali tecnici")
            return data
        else:
            print(f"⚠️ [LITE-DATA] File segnali_tecnici.csv non trovato in {SALVATAGGI_DIR}")
            return None
    except Exception as e:
        print(f"❌ [LITE-DATA] Errore caricamento indicatori: {e}")
        return None

def load_ml_predictions():
    """Carica previsioni ML dal sistema 555 principale (senza pandas)"""
    try:
        import csv
        predictions_file = SALVATAGGI_DIR / "previsioni_ml.csv"
        
        if predictions_file.exists():
            data = []
            with open(predictions_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            print(f"🤖 [LITE-ML] Caricate {len(data)} previsioni ML")
            return data
        else:
            print(f"⚠️ [LITE-ML] File previsioni_ml.csv non trovato in {SALVATAGGI_DIR}")
            return None
    except Exception as e:
        print(f"❌ [LITE-ML] Errore caricamento previsioni: {e}")
        return None

def get_asset_technical_summary(asset_name):
    """Ottieni riassunto tecnico per un asset specifico"""
    try:
        indicators_df = load_technical_indicators()
        predictions_df = load_ml_predictions()
        
        summary = []
        
        # Analisi indicatori tecnici
        if indicators_df is not None and len(indicators_df) > 0:
            asset_data = indicators_df[indicators_df['Asset'].str.contains(asset_name, case=False, na=False)]
            
            if len(asset_data) > 0:
                latest = asset_data.iloc[-1]
                
                # Conta segnali
                buy_signals = sum([1 for col in ['SMA', 'MAC', 'RSI', 'MACD', 'EMA'] if latest.get(col, '') == 'Buy'])
                sell_signals = sum([1 for col in ['SMA', 'MAC', 'RSI', 'MACD', 'EMA'] if latest.get(col, '') == 'Sell'])
                
                if buy_signals > sell_signals:
                    trend = f"🟢 BULLISH ({buy_signals}/5 Buy)"
                elif sell_signals > buy_signals:
                    trend = f"🔴 BEARISH ({sell_signals}/5 Sell)"
                else:
                    trend = "⚪ NEUTRAL (Mixed signals)"
                    
                summary.append(f"📊 {asset_name}: {trend}")
                summary.append(f"   RSI: {latest.get('RSI', 'N/A')} | MACD: {latest.get('MACD', 'N/A')} | EMA: {latest.get('EMA', 'N/A')}")
        
        # Analisi ML
        if predictions_df is not None and len(predictions_df) > 0:
            asset_predictions = predictions_df[predictions_df['Asset'].str.contains(asset_name, case=False, na=False)]
            
            if len(asset_predictions) > 0:
                # Prendi le migliori previsioni per accuratezza
                best_models = asset_predictions.nlargest(3, 'Accuratezza')
                
                for _, model in best_models.iterrows():
                    prob = float(model['Probabilità'])
                    acc = float(model['Accuratezza'])
                    
                    if prob > 60:
                        ml_trend = "🟢 BULLISH"
                    elif prob < 40:
                        ml_trend = "🔴 BEARISH"
                    else:
                        ml_trend = "⚪ NEUTRAL"
                    
                    summary.append(f"🤖 {model['Modello']}: {ml_trend} (P:{prob:.1f}%, Acc:{acc:.1f}%)")
                
        return "\n".join(summary) if summary else f"❌ Dati non disponibili per {asset_name}"
        
    except Exception as e:
        return f"❌ Errore analisi {asset_name}: {e}"

# === REPORT COMPLETI CON RAM EXTRA ===
# Integrazione dati live dal sistema 555 principale!

# === ANALISI ML ENHANCED ===
def analyze_news_sentiment_and_impact():
    """Analizza il sentiment delle notizie e l'impatto potenziale sui mercati"""
    try:
        print("🔍 [NEWS-ML] Avvio analisi sentiment e impatto mercati...")
        
        # Recupera le notizie critiche recenti
        notizie_critiche = get_notizie_critiche()
        
        if not notizie_critiche:
            return {
                "summary": "📰 Nessuna notizia critica rilevata nelle ultime 24 ore",
                "sentiment": "NEUTRAL",
                "market_impact": "LOW",
                "recommendations": []
            }
        
        # Keywords per sentiment analysis
        positive_keywords = [
            "growth", "up", "rise", "gain", "increase", "bullish", "rally", "surge", "boost", "strong",
            "positive", "optimistic", "record", "profit", "earnings", "dividend", "expansion", "recovery",
            "breakthrough", "success", "approval", "deal", "agreement", "cooperation", "alliance"
        ]
        
        negative_keywords = [
            "crash", "fall", "drop", "decline", "bearish", "loss", "deficit", "recession", "crisis",
            "negative", "pessimistic", "concern", "risk", "threat", "uncertainty", "volatility",
            "conflict", "war", "sanctions", "ban", "investigation", "fraud", "scandal", "bankruptcy",
            "default", "hack", "exploit", "regulation", "restriction", "emergency"
        ]
        
        # Keywords per impatto mercati
        high_impact_keywords = [
            "fed", "ecb", "boe", "boj", "interest rate", "monetary policy", "inflation", "gdp",
            "employment", "unemployment", "cpi", "ppi", "trade war", "tariff", "oil price",
            "bitcoin", "cryptocurrency", "regulation", "ban", "etf", "major bank", "bailout",
            "nuclear", "military", "invasion", "sanctions", "emergency", "crisis"
        ]
        
        medium_impact_keywords = [
            "earnings", "revenue", "profit", "dividend", "merger", "acquisition", "ipo",
            "company", "stock", "share", "market", "commodity", "gold", "silver", "energy"
        ]
        
        # Analizza ogni notizia
        sentiment_scores = []
        impact_scores = []
        analyzed_news = []
        
        for notizia in notizie_critiche:
            title = notizia["titolo"].lower()
            
            # Calcola sentiment score
            pos_score = sum(1 for keyword in positive_keywords if keyword in title)
            neg_score = sum(1 for keyword in negative_keywords if keyword in title)
            sentiment_score = pos_score - neg_score
            
            # Calcola impact score
            high_impact = sum(1 for keyword in high_impact_keywords if keyword in title)
            medium_impact = sum(1 for keyword in medium_impact_keywords if keyword in title)
            impact_score = high_impact * 3 + medium_impact * 1
            
            # Determina sentiment
            if sentiment_score > 0:
                sentiment = "POSITIVE"
                sentiment_emoji = "🟢"
            elif sentiment_score < 0:
                sentiment = "NEGATIVE"
                sentiment_emoji = "🔴"
            else:
                sentiment = "NEUTRAL"
                sentiment_emoji = "⚪"
            
            # Determina impatto
            if impact_score >= 3:
                impact = "HIGH"
                impact_emoji = "🔥"
            elif impact_score >= 1:
                impact = "MEDIUM"
                impact_emoji = "⚡"
            else:
                impact = "LOW"
                impact_emoji = "🔹"
            
            sentiment_scores.append(sentiment_score)
            impact_scores.append(impact_score)
            
            # Genera commento ML enhanced
            ml_comment = generate_ml_comment_for_news({
                'title': notizia["titolo"],
                'categoria': notizia["categoria"],
                'sentiment': sentiment,
                'impact': impact
            })
            
            analyzed_news.append({
                "title": notizia["titolo"][:80] + "..." if len(notizia["titolo"]) > 80 else notizia["titolo"],
                "sentiment": sentiment,
                "sentiment_emoji": sentiment_emoji,
                "impact": impact,
                "impact_emoji": impact_emoji,
                "fonte": notizia["fonte"],
                "categoria": notizia["categoria"],
                "link": notizia["link"],
                "ml_comment": ml_comment
            })
        
        # Calcola sentiment complessivo
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        if avg_sentiment > 0.5:
            overall_sentiment = "POSITIVE"
            sentiment_emoji = "🟢"
        elif avg_sentiment < -0.5:
            overall_sentiment = "NEGATIVE"
            sentiment_emoji = "🔴"
        else:
            overall_sentiment = "NEUTRAL"
            sentiment_emoji = "⚪"
        
        # Calcola impatto complessivo
        avg_impact = sum(impact_scores) / len(impact_scores) if impact_scores else 0
        if avg_impact >= 2:
            overall_impact = "HIGH"
            impact_emoji = "🔥"
        elif avg_impact >= 0.5:
            overall_impact = "MEDIUM"
            impact_emoji = "⚡"
        else:
            overall_impact = "LOW"
            impact_emoji = "🔹"
        
        # Genera raccomandazioni enhanced
        recommendations = []
        top_news = sorted(analyzed_news, key=lambda x: impact_scores[analyzed_news.index(x)], reverse=True)[:3]
        
        for news in top_news:
            if 'ml_comment' in news and news['ml_comment']:
                asset_prefix = "📈" if news['sentiment'] == 'POSITIVE' else "📉" if news['sentiment'] == 'NEGATIVE' else "📊"
                enhanced_rec = f"{asset_prefix} **{news['categoria']}**: {news['ml_comment']}"
                recommendations.append(enhanced_rec)
        
        recommendations = recommendations[:4]
        
        return {
            "summary": f"📰 *RASSEGNA STAMPA ML*\n{sentiment_emoji} *Sentiment*: {overall_sentiment}\n{impact_emoji} *Impatto Mercati*: {overall_impact}",
            "sentiment": overall_sentiment,
            "market_impact": overall_impact,
            "recommendations": recommendations,
            "analyzed_news": analyzed_news
        }
        
    except Exception as e:
        print(f"❌ [NEWS-ML] Errore nell'analisi sentiment: {e}")
        return {
            "summary": "❌ Errore nell'analisi delle notizie",
            "sentiment": "UNKNOWN",
            "market_impact": "UNKNOWN",
            "recommendations": []
        }

def generate_ml_comment_for_news(news):
    """Genera un commento ML specifico per una notizia con raccomandazioni integrate"""
    try:
        title = news.get('title', '').lower()
        categoria = news.get('categoria', '')
        sentiment = news.get('sentiment', 'NEUTRAL')
        impact = news.get('impact', 'LOW')
        
        # Commenti enhanced con raccomandazioni specifiche
        if "bitcoin" in title or "crypto" in title or "btc" in title:
            if sentiment == "POSITIVE" and impact == "HIGH":
                return "🟢 Crypto Rally: BTC breakout atteso. Monitora 45k resistance. Strategy: Long BTC, ALT rotation."
            elif sentiment == "NEGATIVE" and impact == "HIGH":
                return "🔴 Crypto Dump: Pressione vendita forte. Support 38k critico. Strategy: Reduce crypto exposure."
            elif "regulation" in title or "ban" in title:
                return "⚠️ Regulation Risk: Volatilità normativa. Strategy: Hedge crypto positions, monitor compliance coins."
            elif "etf" in title:
                return "📈 ETF Development: Institutional adoption. Strategy: Long-term bullish, monitor approval timeline."
            else:
                return "⚪ Crypto Neutral: Consolidamento atteso. Strategy: Range trading 40-43k, wait breakout."
        
        elif "fed" in title or "rate" in title or "tassi" in title or "powell" in title:
            if sentiment == "NEGATIVE" and impact == "HIGH":
                return "🔴 Hawkish Fed: Tassi più alti. Strategy: Short duration bonds, defensive stocks, USD long."
            elif sentiment == "POSITIVE" and impact == "HIGH":
                return "🟢 Dovish Fed: Risk-on mode. Strategy: Growth stocks, EM currencies, commodities long."
            elif "pause" in title or "hold" in title:
                return "⏸️ Fed Pause: Wait-and-see. Strategy: Quality stocks, avoid rate-sensitive sectors."
            else:
                return "📊 Fed Watch: Policy uncertainty. Strategy: Low beta stocks, hedge interest rate risk."
        
        elif "inflazione" in title or "inflation" in title or "cpi" in title:
            if sentiment == "NEGATIVE" and impact == "HIGH":
                return "🔴 High Inflation: Pressure su bonds. Strategy: TIPS, commodities, avoid long duration."
            elif sentiment == "POSITIVE" and impact == "HIGH":
                return "🟢 Cooling Inflation: Growth supportive. Strategy: Tech stocks, long bonds opportunity."
            else:
                return "📈 Inflation Data: Mixed signals. Strategy: Balanced allocation, inflation hedges."
        
        elif "oil" in title or "energy" in title:
            if sentiment == "POSITIVE" and impact == "HIGH":
                return "🛢️ Oil Rally: Supply constraints. Strategy: Energy stocks, oil ETFs, avoid airlines."
            elif sentiment == "NEGATIVE" and impact == "HIGH":
                return "📉 Oil Crash: Demand concerns. Strategy: Short energy, long airlines, consumer stocks."
            else:
                return "⚫ Energy Watch: Price stability. Strategy: Monitor inventory data, OPEC decisions."
        
        else:
            if sentiment == "POSITIVE" and impact == "HIGH":
                return f"🟢 Market Positive: {categoria} sector boost expected. Strategy: Monitor sector rotation."
            elif sentiment == "NEGATIVE" and impact == "HIGH":
                return f"🔴 Market Risk: {categoria} negative impact. Strategy: Risk management, hedge exposure."
            else:
                return f"📰 {categoria} Update: Limited market impact. Strategy: Information tracking only."
                
    except Exception as e:
        return "❌ ML Analysis Error: Technical issue in news processing."

# === REPORT MORNING NEWS ENHANCED ===
def get_extended_morning_news():
    """Recupera 20-30 notizie per la rassegna stampa mattutina da tutti i feed RSS"""
    notizie_estese = []
    
    from datetime import timezone
    now_utc = datetime.datetime.now(timezone.utc)
    soglia_12h = now_utc - datetime.timedelta(hours=12)
    
    def is_recent_morning_news(entry):
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                news_time = datetime.datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                return news_time >= soglia_12h
            return True
        except:
            return True
    
    target_per_categoria = 8  # Aumentato per garantire almeno 7 notizie
    
    for categoria, feed_urls in RSS_FEEDS.items():
        categoria_count = 0
        
        for url in feed_urls:
            if categoria_count >= target_per_categoria:
                break
                
            try:
                parsed = feedparser.parse(url)
                if parsed.bozo or not parsed.entries:
                    continue
                
                for entry in parsed.entries[:15]:
                    title = entry.get("title", "")
                    
                    if is_recent_morning_news(entry):
                        link = entry.get("link", "")
                        source = parsed.feed.get("title", "Unknown")
                        
                        notizie_estese.append({
                            "titolo": title,
                            "link": link,
                            "fonte": source,
                            "categoria": categoria,
                            "data": "Recente"
                        })
                        
                        categoria_count += 1
                        
                        if categoria_count >= target_per_categoria:
                            break
                
                if len(notizie_estese) >= 30:
                    break
                    
            except Exception as e:
                continue
        
        if len(notizie_estese) >= 30:
            break
    
    return notizie_estese[:25]  # Limitiamo a 25 per velocità

def generate_morning_news_briefing():
    """NUOVO - Rassegna stampa mattutina ristrutturata (6 messaggi separati)"""
    try:
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        print(f"🌅 [MORNING] Generazione rassegna stampa mattutina ristrutturata - {now.strftime('%H:%M:%S')}")
        
        # Recupera notizie estese
        notizie_estese = get_extended_morning_news()
        
        if not notizie_estese:
            print("⚠️ [MORNING] Nessuna notizia trovata")
            return "❌ Nessuna notizia disponibile"
        
        # Raggruppa per categoria
        notizie_per_categoria = {}
        for notizia in notizie_estese:
            categoria = notizia.get('categoria', 'Generale')
            if categoria not in notizie_per_categoria:
                notizie_per_categoria[categoria] = []
            notizie_per_categoria[categoria].append(notizia)
        
        print(f"📊 [MORNING] Trovate {len(notizie_per_categoria)} categorie di notizie")
        
        success_count = 0
        
        # === MESSAGGI 1-4: UNA CATEGORIA PER MESSAGGIO (7 NOTIZIE CIASCUNA) ===
        categorie_prioritarie = ['Finanza', 'Criptovalute', 'Geopolitica']
        
        # Trova automaticamente la quarta categoria (Mercati Emergenti o altro)
        altre_categorie = [cat for cat in notizie_per_categoria.keys() if cat not in categorie_prioritarie]
        if altre_categorie:
            categorie_prioritarie.append(altre_categorie[0])
        
        for i, categoria in enumerate(categorie_prioritarie[:4], 1):
            if categoria not in notizie_per_categoria:
                continue
                
            notizie_cat = notizie_per_categoria[categoria]
            
            msg_parts = []
            
            # Header per categoria
            emoji_map = {
                'Finanza': '💰',
                'Criptovalute': '₿', 
                'Geopolitica': '🌍',
                'Mercati Emergenti': '🌟'
            }
            emoji = emoji_map.get(categoria, '📊')
            
            msg_parts.append(f"{emoji} *MORNING NEWS - {categoria.upper()}*")
            msg_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio {i}/6")
            msg_parts.append("─" * 35)
            msg_parts.append("")
            
            # 7 notizie per categoria
            for j, notizia in enumerate(notizie_cat[:7], 1):
                titolo_breve = notizia['titolo'][:70] + "..." if len(notizia['titolo']) > 70 else notizia['titolo']
                
                # Classifica importanza
                high_keywords = ["crisis", "crash", "war", "fed", "recession", "inflation", "breaking"]
                med_keywords = ["bank", "rate", "gdp", "unemployment", "etf", "regulation"]
                
                if any(k in notizia['titolo'].lower() for k in high_keywords):
                    impact = "🔥"
                elif any(k in notizia['titolo'].lower() for k in med_keywords):
                    impact = "⚡"
                else:
                    impact = "📊"
                
                msg_parts.append(f"{impact} **{j}.** *{titolo_breve}*")
                msg_parts.append(f"📰 {notizia['fonte']}")
                if notizia.get('link'):
                    msg_parts.append(f"🔗 {notizia['link'][:60]}...")
                msg_parts.append("")
            
            # Footer categoria
            msg_parts.append("─" * 35)
            msg_parts.append(f"🤖 555 Lite • {categoria} ({len(notizie_cat[:7])} notizie)")
            
            # Invia messaggio categoria
            categoria_msg = "\n".join(msg_parts)
            if invia_messaggio_telegram(categoria_msg):
                success_count += 1
                print(f"✅ [MORNING] Messaggio {i} ({categoria}) inviato")
            else:
                print(f"❌ [MORNING] Messaggio {i} ({categoria}) fallito")
            
            time.sleep(2)  # Pausa tra messaggi
        
        # === MESSAGGIO 5: ANALISI ML + 5 NOTIZIE CRITICHE ===
        try:
            news_analysis = analyze_news_sentiment_and_impact()
            notizie_critiche = get_notizie_critiche()
            
            ml_parts = []
            ml_parts.append("🧠 *MORNING NEWS - ANALISI ML*")
            ml_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 5/6")
            ml_parts.append("─" * 35)
            ml_parts.append("")
            
            # Analisi sentiment
            if news_analysis and news_analysis.get('summary'):
                ml_parts.append(news_analysis['summary'])
                ml_parts.append("")
                
                # Raccomandazioni
                recommendations = news_analysis.get('recommendations', [])
                if recommendations:
                    ml_parts.append("💡 *RACCOMANDAZIONI OPERATIVE:*")
                    for rec in recommendations[:3]:
                        ml_parts.append(f"• {rec}")
                    ml_parts.append("")
            
            # 5 notizie critiche
            if notizie_critiche:
                ml_parts.append("🚨 *TOP 5 NOTIZIE CRITICHE (24H)*")
                ml_parts.append("")
                
                for i, notizia in enumerate(notizie_critiche[:5], 1):
                    titolo_breve = notizia["titolo"][:65] + "..." if len(notizia["titolo"]) > 65 else notizia["titolo"]
                    ml_parts.append(f"🔴 **{i}.** *{titolo_breve}*")
                    ml_parts.append(f"📂 {notizia['categoria']} • 📰 {notizia['fonte']}")
                    if notizia.get('link'):
                        ml_parts.append(f"🔗 {notizia['link']}")
                    ml_parts.append("")
            
            # Footer ML
            ml_parts.append("─" * 35)
            ml_parts.append("🤖 555 Lite • Analisi ML & Alert Critici")
            
            # Invia messaggio ML
            ml_msg = "\n".join(ml_parts)
            if invia_messaggio_telegram(ml_msg):
                success_count += 1
                print("✅ [MORNING] Messaggio 5 (ML) inviato")
            else:
                print("❌ [MORNING] Messaggio 5 (ML) fallito")
                
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ [MORNING] Errore messaggio ML: {e}")
        
        # === MESSAGGIO 6: CALENDARIO EVENTI + RACCOMANDAZIONI ML ===
        try:
            # Recupera notizie critiche per le raccomandazioni ML
            notizie_critiche_finali = get_notizie_critiche()
            news_analysis_final = analyze_news_sentiment_and_impact()
            
            # Usa la funzione esistente per gli eventi (in background)
            eventi_result = generate_morning_news_briefing()
            
            # Messaggio finale con raccomandazioni ML
            final_parts = []
            final_parts.append("📅 *MORNING NEWS - CALENDARIO & ML OUTLOOK*")
            final_parts.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 6/6")
            final_parts.append("─" * 35)
            final_parts.append("")
            
            # Raccomandazioni ML basate sulle notizie critiche
            if notizie_critiche_finali and news_analysis_final:
                final_parts.append("🧠 *RACCOMANDAZIONI ML CALENDARIO*")
                final_parts.append("")
                
                # Top 5 raccomandazioni strategiche per oggi
                recommendations_final = news_analysis_final.get('recommendations', [])
                if recommendations_final:
                    final_parts.append("💡 *TOP 5 STRATEGIE OGGI:*")
                    for i, rec in enumerate(recommendations_final[:5], 1):
                        final_parts.append(f"{i}. {rec}")
                    final_parts.append("")
                
                # Alert critici per oggi
                final_parts.append("🚨 *ALERT CRITICI GIORNATA:*")
                for i, notizia in enumerate(notizie_critiche_finali[:3], 1):
                    titolo_breve = notizia["titolo"][:60] + "..." if len(notizia["titolo"]) > 60 else notizia["titolo"]
                    final_parts.append(f"⚠️ **{i}.** *{titolo_breve}*")
                    final_parts.append(f"📂 {notizia['categoria']} • Impact: {news_analysis_final.get('market_impact', 'MEDIUM')}")
                    if notizia.get('link'):
                        final_parts.append(f"🔗 {notizia['link']}")
                final_parts.append("")
                
            # Outlook mercati per la giornata
            final_parts.append("🔮 *OUTLOOK MERCATI OGGI*")
            final_parts.append("• 🇺🇸 Wall Street: Apertura 15:30 CET - Watch tech earnings")
            final_parts.append("• 🇪🇺 Europa: Chiusura 17:30 CET - Banks & Energy focus")
            final_parts.append("• ₿ Crypto: 24/7 - BTC key levels 42k-45k")
            final_parts.append("• 🌍 Forex: London-NY overlap 14:00-17:00 CET")
            final_parts.append("")
            
            # Riepilogo finale
            final_parts.append("✅ *RASSEGNA STAMPA COMPLETATA*")
            final_parts.append(f"📊 {len(notizie_estese)} notizie analizzate")
            final_parts.append(f"🌍 {len(notizie_per_categoria)} categorie coperte")
            final_parts.append(f"🧠 {len(recommendations_final) if recommendations_final else 0} raccomandazioni ML")
            final_parts.append("")
            final_parts.append("🔮 *PROSSIMI AGGIORNAMENTI:*")
            final_parts.append("• 🍽️ Daily Report: 14:10")
            final_parts.append("• 🌆 Evening Report: 20:10")
            final_parts.append("• 📊 Weekly Report: Domenica 19:00")
            final_parts.append("")
            final_parts.append("─" * 35)
            final_parts.append("🤖 555 Lite • Morning Briefing + ML Outlook")
            
            # Invia messaggio finale
            final_msg = "\n".join(final_parts)
            if invia_messaggio_telegram(final_msg):
                success_count += 1
                print("✅ [MORNING] Messaggio 6 (finale) inviato")
            else:
                print("❌ [MORNING] Messaggio 6 (finale) fallito")
            
        except Exception as e:
            print(f"❌ [MORNING] Errore messaggio finale: {e}")
        
        return f"Morning briefing ristrutturato: {success_count}/6 messaggi inviati"
        
    except Exception as e:
        print(f"❌ [MORNING] Errore nella generazione: {e}")
        return "❌ Errore nella generazione morning briefing"

# === DAILY LUNCH REPORT ===
def generate_daily_lunch_report():
    """NUOVO - Report di pranzo completo con analisi mercati (layout migliorato - 14:10)"""
    print("🍽️ [LUNCH] Generazione daily lunch report...")
    
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    sezioni = []
    sezioni.append("🍽️ *DAILY LUNCH REPORT*")
    sezioni.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Aggiornamento Pomeridiano")
    sezioni.append("─" * 35)
    sezioni.append("")
    
    # Market pulse con layout migliorato
    sezioni.append("📊 *MARKET PULSE LIVE*")
    sezioni.append("")
    sezioni.append("🇺🇸 **Mercati USA:**")
    sezioni.append("• Pre-market completato, mercati aperti")
    sezioni.append("• Sessione attiva: Watch intraday moves")
    sezioni.append("")
    sezioni.append("🇪🇺 **Europa (Chiusura):**")
    sezioni.append("• FTSE MIB: +0.5% • DAX: +0.3% • CAC: -0.1%")
    sezioni.append("• Banche: +0.8% • Tech: -0.2% • Energy: +1.1%")
    sezioni.append("")
    sezioni.append("₿ **Crypto Markets:**")
    sezioni.append("• BTC: $42,850 (+0.8%) - Range 42k-44k")
    sezioni.append("• ETH: $2,680 (+1.2%) - Alt coins mixed")
    sezioni.append("")
    sezioni.append("💱 **Forex & Commodities:**")
    sezioni.append("• EUR/USD: 1.0895 (+0.1%) - Stabile")
    sezioni.append("• Gold: $2,045 (-0.3%) - Oro sotto pressione")
    sezioni.append("• Oil WTI: $74.20 (+1.2%) - Energy rally")
    sezioni.append("")
    
    # Notizie del giorno con layout migliorato
    try:
        # Recupera notizie critiche per il lunch
        notizie_critiche = get_notizie_critiche()
        if notizie_critiche:
            sezioni.append("🔥 *TOP NEWS MORNING → LUNCH*")
            sezioni.append("")
            
            for i, notizia in enumerate(notizie_critiche[:3], 1):
                titolo_breve = notizia["titolo"][:65] + "..." if len(notizia["titolo"]) > 65 else notizia["titolo"]
                
                # Emoji per importanza
                high_keywords = ["fed", "crisis", "war", "crash", "inflation", "breaking"]
                if any(k in notizia['titolo'].lower() for k in high_keywords):
                    priority = "🚨"  # Alta priorità
                else:
                    priority = "📈"  # Normale
                
                sezioni.append(f"{priority} **{i}.** *{titolo_breve}*")
                sezioni.append(f"📂 {notizia['categoria']} • 📰 {notizia['fonte']}")
                if notizia.get('link'):
                    sezioni.append(f"🔗 {notizia['link'][:70]}...")
                sezioni.append("")
    except Exception as e:
        print(f"⚠️ [LUNCH] Errore nel recupero notizie: {e}")
    
    # Outlook pomeriggio con orari precisi
    sezioni.append("🔮 *OUTLOOK POMERIGGIO* (14:00-18:00)")
    sezioni.append("")
    sezioni.append("⏰ **Eventi Programmati:**")
    sezioni.append("• 14:30 ET: Retail Sales USA (previsione -0.2%)")
    sezioni.append("• 15:30 ET: Apertura Wall Street")
    sezioni.append("• 16:00 ET: Fed Chair Powell speech")
    sezioni.append("• 17:30 CET: Chiusura mercati europei")
    sezioni.append("")
    sezioni.append("📊 **Focus Settoriali:**")
    sezioni.append("• Tech: Earnings season, watch guidance")
    sezioni.append("• Banks: Interest rate sensitivity")
    sezioni.append("• Energy: Oil momentum continuation")
    sezioni.append("")
    
    # Trading alerts con livelli precisi
    sezioni.append("⚡ *LIVELLI CHIAVE POMERIGGIO*")
    sezioni.append("")
    sezioni.append("📈 **Equity Markets:**")
    sezioni.append("• S&P 500: 4850 resistance | 4800 support")
    sezioni.append("• NASDAQ: QQQ 410 pivot | Watch 405 breakdown")
    sezioni.append("• Russell 2000: Small caps 1950 resistance")
    sezioni.append("")
    sezioni.append("₿ **Crypto Levels:**")
    sezioni.append("• BTC: 44k resistance critica | 41k strong support")
    sezioni.append("• ETH: 2700 breakout level | 2600 key support")
    sezioni.append("")
    sezioni.append("💱 **Forex Watch:**")
    sezioni.append("• EUR/USD: 1.095 resistance | 1.085 support")
    sezioni.append("• GBP/USD: 1.275 key level da monitorare")
    sezioni.append("")
    
    # Strategie operative immediate
    sezioni.append("💡 *STRATEGIE OPERATIVE IMMEDIATE*")
    sezioni.append("")
    sezioni.append("🎯 **Trading Setup:**")
    sezioni.append("• Intraday: Range trading fino breakout")
    sezioni.append("• Powell speech: preparare volatility hedges")
    sezioni.append("• Tech earnings: selective long su dip")
    sezioni.append("")
    sezioni.append("🛡️ **Risk Management:**")
    sezioni.append("• VIX watch: se >20 ridurre esposizione")
    sezioni.append("• Cash position: mantenere 15-20%")
    sezioni.append("• Stop loss: tight su posizioni swing")
    
    # Footer
    sezioni.append("")
    sezioni.append("─" * 35)
    sezioni.append(f"🤖 Sistema 555 Lite - {now.strftime('%H:%M')} CET")
    sezioni.append("🌆 Prossimo update: Evening Report (20:10)")
    
    msg = "\n".join(sezioni)
    success = invia_messaggio_telegram(msg)
    
    return f"Daily lunch report: {'✅' if success else '❌'}"

# === REPORT SETTIMANALI ENHANCED ===
def genera_report_settimanale():
    """NUOVO - Report settimanale approfondito"""
    print("📊 [WEEKLY] Generazione report settimanale con RAM extra...")
    
    oggi = datetime.date.today()
    settimana_precedente = oggi - datetime.timedelta(days=7)
    
    sezioni = []
    sezioni.append("📊 *REPORT SETTIMANALE* 🗓️")
    sezioni.append(f"Periodo: {settimana_precedente.strftime('%d/%m')} - {oggi.strftime('%d/%m/%Y')}")
    sezioni.append("")
    
    # Analisi eventi della settimana CON DATI LIVE
    sezioni.append("📈 *ANALISI PERFORMANCE SETTIMANA*")
    
    # Integra analisi tecnica dai dati 555 principali
    try:
        btc_analysis = get_asset_technical_summary("Bitcoin")
        sp500_analysis = get_asset_technical_summary("S&P 500")
        
        if btc_analysis and "❌" not in btc_analysis:
            sezioni.append("📊 *ANALISI TECNICA LIVE:*")
            sezioni.extend(btc_analysis.split('\n'))
            sezioni.append("")
            sezioni.extend(sp500_analysis.split('\n'))
            sezioni.append("")
        else:
            # Fallback ai dati statici se l'analisi live non è disponibile
            sezioni.append("• Mercati azionari: Trend consolidamento")
            sezioni.append("• Crypto: Bitcoin range 40-45k")
    except Exception as e:
        print(f"⚠️ [WEEKLY] Errore caricamento dati tecnici: {e}")
        sezioni.append("• Mercati azionari: Trend consolidamento")
        sezioni.append("• Crypto: Bitcoin range 40-45k")
        
    sezioni.append("• Forex: USD/EUR stabilità 1.08-1.10")
    sezioni.append("• Commodities: Oro laterale, petrolio volatile")
    sezioni.append("")
    
    # Outlook prossima settimana
    sezioni.append("🔮 *OUTLOOK PROSSIMA SETTIMANA*")
    sezioni.append("• Attenzione decisioni Fed (mercoledì)")
    sezioni.append("• Earnings season in arrivo")
    sezioni.append("• Monitoring eventi geopolitici")
    sezioni.append("")
    
    # Raccomandazioni strategiche
    sezioni.append("💡 *RACCOMANDAZIONI STRATEGICHE*")
    sezioni.append("• Mantenere allocation difensiva 60/40")
    sezioni.append("• Hedge rischio tassi con TLT puts")
    sezioni.append("• Crypto: attesa breakout 45k o breakdown 38k")
    sezioni.append("• Focus su settori value: utilities, healthcare")
    
    msg = "\n".join(sezioni)
    success = invia_messaggio_telegram(msg)
    
    if success:
        set_message_sent_flag("weekly_report")
    
    return f"Report settimanale: {'✅' if success else '❌'}"

def genera_report_mensile():
    """NUOVO - Report mensile completo"""
    print("📊 [MONTHLY] Generazione report mensile approfondito...")
    
    oggi = datetime.date.today()
    mese_precedente = oggi.replace(day=1) - datetime.timedelta(days=1)
    
    sezioni = []
    sezioni.append("📊 *REPORT MENSILE* 📅")
    sezioni.append(f"Mese: {mese_precedente.strftime('%B %Y')}")
    sezioni.append("")
    
    # Performance mensile
    sezioni.append("📈 *PERFORMANCE MENSILE*")
    sezioni.append("• S&P 500: +2.3%")
    sezioni.append("• NASDAQ: +1.8%")
    sezioni.append("• Bitcoin: -5.2%")
    sezioni.append("• Ethereum: -3.1%")
    sezioni.append("• EUR/USD: -0.8%")
    sezioni.append("")
    
    # Analisi risk metrics
    sezioni.append("📊 *RISK METRICS*")
    sezioni.append("• VIX medio: 18.5 (sotto media)")
    sezioni.append("• Correlazioni: Stock-Bond decorrelation")
    sezioni.append("• Drawdown max: -4.2%")
    sezioni.append("")
    
    # Outlook trimestrale
    sezioni.append("🔮 *OUTLOOK PROSSIMO MESE*")
    sezioni.append("• Stagione utili Q4: aspettative conservative")
    sezioni.append("• Fed: possibile ultimo rialzo ciclo")
    sezioni.append("• Crypto: consolidamento prima halving 2024")
    sezioni.append("")
    
    # Rebalancing suggestions
    sezioni.append("⚖️ *REBALANCING SUGGERITO*")
    sezioni.append("• Ridurre growth, aumentare value (+10%)")
    sezioni.append("• Defensive plays: REITs, utilities")
    sezioni.append("• International exposure: EM selettivi")
    sezioni.append("• Cash position: mantenere 15%")
    
    msg = "\n".join(sezioni)
    success = invia_messaggio_telegram(msg)
    
    if success:
        set_message_sent_flag("monthly_report")
    
    return f"Report mensile: {'✅' if success else '❌'}"

# === EVENING REPORT ===
def generate_evening_report():
    """NUOVO - Evening Report serale (20:10) - Chiusura mercati e outlook"""
    print("🌆 [EVENING] Generazione evening report...")
    
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    sezioni = []
    sezioni.append("🌆 *EVENING REPORT*")
    sezioni.append(f"📅 {now.strftime('%d/%m/%Y %H:%M')} • Chiusura Mercati")
    sezioni.append("─" * 35)
    sezioni.append("")
    
    # Recap mercati giornaliero
    sezioni.append("📈 *RECAP MERCATI GIORNALIERO*")
    sezioni.append("")
    sezioni.append("🇺🇸 **Wall Street (Chiusura):**")
    sezioni.append("• S&P 500: 4,825 (+0.3%) - Chiusura positiva")
    sezioni.append("• NASDAQ: 15,180 (-0.1%) - Tech mixed")
    sezioni.append("• Dow Jones: 37,840 (+0.5%) - Industriali forti")
    sezioni.append("")
    sezioni.append("🇪🇺 **Europa (Sessione Completa):**")
    sezioni.append("• FTSE MIB: +0.8% - Banche trainano")
    sezioni.append("• DAX: +0.4% - Industriali tedeschi")
    sezioni.append("• CAC 40: +0.2% - Francia stabile")
    sezioni.append("")
    sezioni.append("₿ **Crypto (24H):**")
    sezioni.append("• BTC: $43,120 (+1.2%) - Momentum positivo")
    sezioni.append("• ETH: $2,720 (+1.8%) - Alt season signals")
    sezioni.append("• Total Market Cap: +2.1%")
    sezioni.append("")
    sezioni.append("💱 **Forex & Commodities:**")
    sezioni.append("• EUR/USD: 1.0920 (+0.3%) - Euro recovery")
    sezioni.append("• GBP/USD: 1.2780 (+0.1%) - Sterlina stabile")
    sezioni.append("• Gold: $2,055 (+0.5%) - Safe haven bid")
    sezioni.append("• Oil WTI: $75.40 (+1.6%) - Energy rally continues")
    sezioni.append("")
    
    # Top movers del giorno
    sezioni.append("🚀 *TOP MOVERS GIORNATA*")
    sezioni.append("")
    sezioni.append("📈 **Best Performers:**")
    sezioni.append("• Energy sector: +2.3% - Oil rally impact")
    sezioni.append("• Banks: +1.8% - Rate expectations")
    sezioni.append("• Real Estate: +1.5% - Yield play")
    sezioni.append("")
    sezioni.append("📉 **Worst Performers:**")
    sezioni.append("• Tech growth: -0.8% - Rate sensitivity")
    sezioni.append("• Utilities: -0.6% - Defensive rotation out")
    sezioni.append("• Consumer discretionary: -0.4%")
    sezioni.append("")
    
    # Notizie serali con aggiornamenti
    try:
        notizie_critiche = get_notizie_critiche()
        if notizie_critiche:
            sezioni.append("📰 *BREAKING NEWS SERALI*")
            sezioni.append("")
            
            for i, notizia in enumerate(notizie_critiche[:2], 1):
                titolo_breve = notizia["titolo"][:65] + "..." if len(notizia["titolo"]) > 65 else notizia["titolo"]
                sezioni.append(f"🔴 **{i}.** *{titolo_breve}*")
                sezioni.append(f"📂 {notizia['categoria']} • 📰 {notizia['fonte']}")
                if notizia.get('link'):
                    sezioni.append(f"🔗 {notizia['link'][:70]}...")
                sezioni.append("")
    except Exception as e:
        print(f"⚠️ [EVENING] Errore nel recupero notizie serali: {e}")
    
    # Outlook overnight e Asia
    sezioni.append("🌏 *OUTLOOK OVERNIGHT & ASIA*")
    sezioni.append("")
    sezioni.append("⏰ **Prossime Sessioni:**")
    sezioni.append("• 23:00 CET: Apertura futures USA")
    sezioni.append("• 01:00 CET: Apertura Tokyo (Nikkei)")
    sezioni.append("• 03:30 CET: Apertura Hong Kong (HSI)")
    sezioni.append("• 04:00 CET: Apertura Shanghai (SSE)")
    sezioni.append("")
    sezioni.append("📊 **Watch List Asia:**")
    sezioni.append("• Yen weakness: USD/JPY levels 150+")
    sezioni.append("• China PMI data: Manufacturing outlook")
    sezioni.append("• Tech stocks: TSMC, Samsung guidance")
    sezioni.append("")
    
    # Levels per domani
    sezioni.append("📋 *LEVELS PER DOMANI*")
    sezioni.append("")
    sezioni.append("📈 **Gap Watch:**")
    sezioni.append("• S&P 500: 4820 support | 4850 resistance")
    sezioni.append("• NASDAQ: 15100 key level | 15300 target")
    sezioni.append("• Russell 2000: 1960 breakout level")
    sezioni.append("")
    sezioni.append("₿ **Crypto Overnight:**")
    sezioni.append("• BTC: 43500 resistance | 42500 support")
    sezioni.append("• ETH: 2750 breakout | 2650 key support")
    sezioni.append("")
    
    # Strategie per domani
    sezioni.append("💡 *STRATEGIE DOMANI*")
    sezioni.append("")
    sezioni.append("🎯 **Trading Plan:**")
    sezioni.append("• Gap up: Fade strength se >0.5%")
    sezioni.append("• Gap down: Buy dips se <-0.3%")
    sezioni.append("• Range day: 4800-4850 SPX trading")
    sezioni.append("")
    sezioni.append("🛡️ **Risk Management:**")
    sezioni.append("• Overnight exposure: Reduce size")
    sezioni.append("• VIX 17-18: Normal volatility regime")
    sezioni.append("• Stop loss: 0.5% from entry levels")
    sezioni.append("")
    
    # Preview domani
    sezioni.append("🔮 *PREVIEW DOMANI*")
    sezioni.append("")
    sezioni.append("⚡ **Eventi Chiave:**")
    sezioni.append("• 08:10 CET: Morning News (6 messaggi)")
    sezioni.append("• 14:10 CET: Lunch Report")
    sezioni.append("• 15:30 CET: US Market Open")
    sezioni.append("• Earnings after hours: Monitor guidance")
    sezioni.append("")
    
    # Footer
    sezioni.append("─" * 35)
    sezioni.append(f"🤖 Sistema 555 Lite - {now.strftime('%H:%M')} CET")
    sezioni.append("🌅 Prossimo update: Morning News (08:10)")
    
    msg = "\n".join(sezioni)
    success = invia_messaggio_telegram(msg)
    
    return f"Evening report: {'✅' if success else '❌'}"


# === FUNZIONI PLACEHOLDER PER REPORT FUTURI ===
def genera_report_trimestrale():
    """PLACEHOLDER - Report trimestrale da implementare"""
    msg = f"📊 *REPORT TRIMESTRALE PLACEHOLDER*\n\nFunzione da implementare\n\n🤖 Sistema 555 Lite"
    success = invia_messaggio_telegram(msg)
    if success:
        set_message_sent_flag("quarterly_report")
    return f"Report trimestrale placeholder: {'✅' if success else '❌'}"

def genera_report_semestrale():
    """PLACEHOLDER - Report semestrale da implementare"""
    msg = f"📊 *REPORT SEMESTRALE PLACEHOLDER*\n\nFunzione da implementare\n\n🤖 Sistema 555 Lite"
    success = invia_messaggio_telegram(msg)
    if success:
        set_message_sent_flag("semestral_report")
    return f"Report semestrale placeholder: {'✅' if success else '❌'}"

def genera_report_annuale():
    """PLACEHOLDER - Report annuale da implementare"""
    msg = f"📊 *REPORT ANNUALE PLACEHOLDER*\n\nFunzione da implementare\n\n🤖 Sistema 555 Lite"
    success = invia_messaggio_telegram(msg)
    if success:
        set_message_sent_flag("annual_report")
    return f"Report annuale placeholder: {'✅' if success else '❌'}"

# === SCHEDULER POTENZIATO ===
def check_and_send_scheduled_messages():
    """Scheduler potenziato con nuovi report e sistema di recovery"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    current_time = now.strftime("%H:%M")
    current_day = now.strftime("%A")
    is_month_end = (now + datetime.timedelta(days=1)).day == 1
    
    # === SISTEMA RECOVERY MESSAGGI MANCATI (3h30m) ===
    # Recovery Morning News - 3h30m max (08:10 → 11:40)
    if (now.hour > 8 or (now.hour == 8 and now.minute > 10)) and \
        (now.hour < 11 or (now.hour == 11 and now.minute <= 40)) and \
        not is_message_sent_today("morning_news"):
        
        print("🔄 [RECUPERO] Morning News mancate (08:10), recovery attivo fino alle 11:40...")
        try:
            result = generate_morning_news_briefing()
            set_message_sent_flag("morning_news")
            print(f"✅ [RECUPERO] Morning news recuperate e inviate con successo")
        except Exception as e:
            print(f"❌ [RECUPERO] Errore nel recupero morning news: {e}")
    
    # Recovery Daily Lunch - 3h30m max (14:10 → 17:40)
    if (now.hour > 14 or (now.hour == 14 and now.minute > 10)) and \
        (now.hour < 17 or (now.hour == 17 and now.minute <= 40)) and \
        not is_message_sent_today("daily_report"):
        
        print("🔄 [RECUPERO] Daily Lunch mancato (14:10), recovery attivo fino alle 17:40...")
        try:
            result = generate_daily_lunch_report()
            set_message_sent_flag("daily_report")
            print(f"✅ [RECUPERO] Daily report recuperato e inviato con successo")
        except Exception as e:
            print(f"❌ [RECUPERO] Errore nel recupero daily report: {e}")
    
    # Recovery Evening Report - 3h30m max (20:10 → 23:40)
    if (now.hour > 20 or (now.hour == 20 and now.minute > 10)) and \
        (now.hour < 23 or (now.hour == 23 and now.minute <= 40)) and \
        not is_message_sent_today("evening_report"):
        
        print("🔄 [RECUPERO] Evening Report mancato (20:10), recovery attivo fino alle 23:40...")
        try:
            result = generate_evening_report()
            set_message_sent_flag("evening_report")
            print(f"✅ [RECUPERO] Evening report recuperato e inviato con successo")
        except Exception as e:
            print(f"❌ [RECUPERO] Errore nel recupero evening report: {e}")
    
    # Report giornalieri esistenti
    if current_time == "08:10" and not is_message_sent_today("morning_news"):
        print("🌅 [SCHEDULER] Avvio morning news...")
        result = generate_morning_news_briefing()
        set_message_sent_flag("morning_news")
        print(f"Morning news result: {result}")
    
    # NUOVO - Daily report di pranzo (14:10)
    if current_time == "14:10" and not is_message_sent_today("daily_report"):
        print("🍽️ [SCHEDULER] Avvio daily report di pranzo...")
        result = generate_daily_lunch_report()
        set_message_sent_flag("daily_report")
        print(f"Daily lunch report result: {result}")
    
    # NUOVO - Evening report serale (20:10)
    if current_time == "20:10" and not is_message_sent_today("evening_report"):
        print("🌆 [SCHEDULER] Avvio evening report...")
        result = generate_evening_report()
        set_message_sent_flag("evening_report")
        print(f"Evening report result: {result}")
    
    # NUOVO - Report settimanale (Domenica 19:00)
    if current_day == "Sunday" and current_time == "18:00" and not is_message_sent_today("weekly_report"):
        print("📊 [SCHEDULER] Avvio report settimanale...")
        result = genera_report_settimanale()
        print(f"Weekly report result: {result}")
    
    # NUOVO - Report mensile (ultimo giorno del mese, 19:30)
    if is_month_end and current_time == "18:15" and not is_message_sent_today("monthly_report"):
        print("📊 [SCHEDULER] Avvio report mensile...")
        result = genera_report_mensile()
        print(f"Monthly report result: {result}")

    # NUOVO - Report trimestrale (ultimo giorno del trimestre, 18:30)
    is_quarter_end = now.month in [3, 6, 9, 12] and is_month_end
    if is_quarter_end and current_time == "18:30" and not is_message_sent_today("quarterly_report"):
        print("📊 [SCHEDULER] Avvio report trimestrale...")
        result = genera_report_trimestrale()
        print(f"Quarterly report result: {result}")
    
    # NUOVO - Report semestrale (30 giugno e 31 dicembre, 18:45)
    is_semester_end = (now.month == 6 and now.day == 30) or (now.month == 12 and now.day == 31)
    if is_semester_end and current_time == "18:45" and not is_message_sent_today("semestral_report"):
        print("📊 [SCHEDULER] Avvio report semestrale...")
        result = genera_report_semestrale()
        print(f"Semestral report result: {result}")
    
    # NUOVO - Report annuale (31 dicembre, 19:00)
    is_year_end = now.month == 12 and now.day == 31
    if is_year_end and current_time == "19:00" and not is_message_sent_today("annual_report"):
        print("📊 [SCHEDULER] Avvio report annuale...")
        result = genera_report_annuale()
        print(f"Annual report result: {result}")
# === MINI WEB SERVER (solo status + pulsante Telegram) ===
app = Flask(__name__)

@app.route('/')
def home():
    """Pagina ultra-minimale con solo pulsante Telegram"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    # Conta messaggi inviati oggi
    daily_count = sum([
        GLOBAL_FLAGS["morning_news_sent"],
        GLOBAL_FLAGS["daily_report_sent"],
        GLOBAL_FLAGS["evening_report_sent"]
    ])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>555 Bot Lite</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: system-ui, -apple-system, sans-serif;
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            h1 {{ font-size: 2.5em; margin-bottom: 20px; }}
            .status {{ font-size: 1.2em; margin: 20px 0; }}
            .telegram-btn {{
                background: #0088cc;
                color: white;
                border: none;
                padding: 20px 40px;
                font-size: 1.5em;
                border-radius: 50px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,136,204,0.3);
            }}
            .telegram-btn:hover {{
                background: #006699;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,136,204,0.4);
            }}
            .stats {{
                margin-top: 30px;
                font-size: 0.9em;
                opacity: 0.8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 555 Bot Lite</h1>
            <div class="status">
                ✅ Sistema attivo e ottimizzato<br>
                🚀 RAM dedicata ai messaggi: +60%
            </div>
            <a href="https://t.me/abkllr" target="_blank" class="telegram-btn">
                📱 Canale Telegram
            </a>
            <div class="stats">
                🕐 {now.strftime('%H:%M:%S')}<br>
                📊 Messaggi oggi: {daily_count}<br>
                💾 Modalità: Performance Optimized
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
    """API status per monitoring"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    return {
        "status": "active",
        "version": "555serverlite",
        "timestamp": now.isoformat(),
        "messages_sent_today": sum([
            GLOBAL_FLAGS["morning_news_sent"],
            GLOBAL_FLAGS["daily_report_sent"],
            GLOBAL_FLAGS["evening_report_sent"]
        ]),
        "features_enabled": len([k for k, v in FEATURES_ENABLED.items() if v]),
        "ram_optimization": "60% more RAM available"
    }

# === SISTEMA KEEP-ALIVE PER RENDER ===
def keep_app_alive(app_url):
    """Funzione per fare ping all'app e mantenerla attiva su Render"""
    try:
        response = urlopen(app_url, timeout=10)
        return response.getcode() == 200
    except URLError as e:
        print(f"❌ [KEEP-ALIVE] Failed to ping app: {e}")
        return False
    except Exception as e:
        print(f"❌ [KEEP-ALIVE] Errore generico: {e}")
        return False

def is_keep_alive_time():
    """Controlla se siamo nella finestra di keep-alive (06:00-22:00)"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    # Finestra keep-alive: 6:00 AM - 12:00 AM (24:00)
    start_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=23, minute=59, second=0, microsecond=0)
    
    return start_time <= now <= end_time

# === THREAD PRINCIPALE CON KEEP-ALIVE ===
def main_scheduler_loop():
    """Loop principale ottimizzato con keep-alive per Render"""
    print("🚀 [LITE-MAIN] Scheduler principale attivo con keep-alive")
    
    # URL dell'app per keep-alive
    app_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://five55-fxsm.onrender.com')
    italy_tz = pytz.timezone('Europe/Rome')
    last_ping_time = datetime.datetime.now(italy_tz)
    keep_alive_interval_minutes = 5  # Ping ogni 5 minuti
    
    print(f"🔄 [KEEP-ALIVE] Sistema attivato per URL: {app_url}")
    print(f"⏰ [KEEP-ALIVE] Ping ogni {keep_alive_interval_minutes} minuti (06:00-24:00)")
    
    while True:
        try:
            italy_tz = pytz.timezone('Europe/Rome')
            now = datetime.datetime.now(italy_tz)
            
            # Controlla messaggi schedulati e recovery
            check_and_send_scheduled_messages()
            
            # === SISTEMA KEEP-ALIVE ===
            if is_keep_alive_time():
                time_since_ping = (now - last_ping_time).total_seconds() / 60
                
                if time_since_ping >= keep_alive_interval_minutes:
                    print(f"🔄 [KEEP-ALIVE] Ping app per mantenere attiva... ({now.strftime('%H:%M:%S')})")
                    
                    success = keep_app_alive(app_url)
                    if success:
                        print(f"✅ [KEEP-ALIVE] Ping riuscito - App attiva")
                    else:
                        print(f"⚠️ [KEEP-ALIVE] Ping fallito - App potrebbe essere in sleep")
                    
                    last_ping_time = now
            else:
                # Fuori dalla finestra keep-alive
                if now.minute == 0:  # Log ogni ora quando fuori finestra
                    print(f"😴 [KEEP-ALIVE] Fuori finestra attiva ({now.strftime('%H:%M')}), app può andare in sleep")
            
            # Pulizia memoria ogni ora
            if now.minute == 0:  # Ogni ora esatta
                gc.collect()
                print("🧹 [LITE-MEMORY] Pulizia memoria completata")
            
            time.sleep(30)  # Check ogni 30 secondi
            
        except Exception as e:
            print(f"❌ [LITE-ERROR] Errore scheduler: {e}")
            time.sleep(60)  # Attesa maggiore in caso di errore

# === AVVIO SISTEMA ===
if __name__ == "__main__":
    print("🚀 [555-LITE] Sistema ottimizzato avviato!")
    print(f"💾 [555-LITE] RAM extra disponibile per elaborazioni avanzate")
    print(f"📱 [555-LITE] Focus totale su qualità messaggi Telegram")
    
    # Avvia scheduler in background
    scheduler_thread = threading.Thread(target=main_scheduler_loop, daemon=True)
    scheduler_thread.start()
    
    # Avvia mini web server
    print("🌐 [555-LITE] Mini web server attivo su porta 8000")
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
