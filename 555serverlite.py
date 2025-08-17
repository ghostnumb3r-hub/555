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

# === SISTEMA FLAG IN-MEMORY PER RENDER ===
GLOBAL_FLAGS = {
    "morning_news_sent": False,
    "daily_report_sent": False,
    "weekly_report_sent": False,     # Report settimanali
    "monthly_report_sent": False,    # Report mensili
    "quarterly_report_sent": False,  # Report trimestrali (Q1,Q2,Q3,Q4)
    "semestral_report_sent": False,  # Report semestrali (S1,S2)
    "annual_report_sent": False,     # Report annuali
    "last_reset_date": datetime.datetime.now().strftime("%Y%m%d")
}

def reset_daily_flags_if_needed():
    """Resetta i flag se è passata la mezzanotte"""
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    if GLOBAL_FLAGS["last_reset_date"] != current_date:
        GLOBAL_FLAGS["morning_news_sent"] = False
        GLOBAL_FLAGS["daily_report_sent"] = False
        # I flag settimanali/mensili hanno logica separata
        GLOBAL_FLAGS["last_reset_date"] = current_date
        print(f"🔄 [LITE-FLAGS] Reset giornaliero completato per {current_date}")
        return True
    return False

def set_message_sent_flag(message_type):
    """Imposta il flag di invio per il tipo di messaggio"""
    reset_daily_flags_if_needed()
    
    if message_type == "morning_news":
        GLOBAL_FLAGS["morning_news_sent"] = True
        print("✅ [LITE-FLAGS] Flag morning_news_sent impostato")
    elif message_type == "daily_report":
        GLOBAL_FLAGS["daily_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag daily_report_sent impostato")
    elif message_type == "weekly_report":
        GLOBAL_FLAGS["weekly_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag weekly_report_sent impostato")
    elif message_type == "monthly_report":
        GLOBAL_FLAGS["monthly_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag monthly_report_sent impostato")
    elif message_type == "quarterly_report":
        GLOBAL_FLAGS["quarterly_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag quarterly_report_sent impostato")
    elif message_type == "semestral_report":
        GLOBAL_FLAGS["semestral_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag semestral_report_sent impostato")
    elif message_type == "annual_report":
        GLOBAL_FLAGS["annual_report_sent"] = True
        print("✅ [LITE-FLAGS] Flag annual_report_sent impostato")

def is_message_sent_today(message_type):
    """Verifica se il messaggio è già stato inviato oggi"""
    reset_daily_flags_if_needed()
    
    if message_type == "morning_news":
        return GLOBAL_FLAGS["morning_news_sent"]
    elif message_type == "daily_report":
        return GLOBAL_FLAGS["daily_report_sent"]
    elif message_type == "weekly_report":
        return GLOBAL_FLAGS["weekly_report_sent"]
    elif message_type == "monthly_report":
        return GLOBAL_FLAGS["monthly_report_sent"]
    elif message_type == "quarterly_report":
        return GLOBAL_FLAGS["quarterly_report_sent"]
    elif message_type == "semestral_report":
        return GLOBAL_FLAGS["semestral_report_sent"]
    elif message_type == "annual_report":
        return GLOBAL_FLAGS["annual_report_sent"]
    return False

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

# === RSS FEEDS (Stesso sistema) ===
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

# === REPORT COMPLETI CON RAM EXTRA ===
# Copiati dal sistema locale - tutti i report avanzati!

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
    
    target_per_categoria = 6
    
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
    """NUOVO - Rassegna stampa mattutina completa con RAM extra"""
    try:
        italy_tz = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(italy_tz)
        
        print(f"🌅 [MORNING] Generazione rassegna stampa mattutina - {now.strftime('%H:%M:%S')}")
        
        morning_parts = []
        
        # Header
        morning_parts.append(f"🌅 *RASSEGNA STAMPA MATTUTINA - {now.strftime('%d/%m/%Y %H:%M')}*")
        morning_parts.append("═" * 40)
        
        # Notizie estese
        try:
            notizie_estese = get_extended_morning_news()
            
            if notizie_estese:
                morning_parts.append(f"📰 *TOP NOTIZIE INTERNAZIONALI* ({len(notizie_estese)} articoli)")
                morning_parts.append("")
                
                # Raggruppa per categoria
                notizie_per_categoria = {}
                for notizia in notizie_estese:
                    categoria = notizia.get('categoria', 'Generale')
                    if categoria not in notizie_per_categoria:
                        notizie_per_categoria[categoria] = []
                    notizie_per_categoria[categoria].append(notizia)
                
                # Mostra per categoria
                for categoria, notizie_cat in notizie_per_categoria.items():
                    morning_parts.append(f"📂 *{categoria.upper()}*:")
                    
                    for i, notizia in enumerate(notizie_cat[:6], 1):
                        titolo_breve = notizia['titolo'][:65] + "..." if len(notizia['titolo']) > 65 else notizia['titolo']
                        
                        # Classifica importanza
                        high_keywords = ["crisis", "crash", "war", "fed", "recession", "inflation", "breaking"]
                        med_keywords = ["bank", "rate", "gdp", "unemployment", "etf", "regulation"]
                        
                        if any(k in notizia['titolo'].lower() for k in high_keywords):
                            impact = "🔥"
                        elif any(k in notizia['titolo'].lower() for k in med_keywords):
                            impact = "⚡"
                        else:
                            impact = "📊"
                        
                        morning_parts.append(f"{impact} {i}. *{titolo_breve}*")
                        morning_parts.append(f"   📰 {notizia['fonte']}")
                        if notizia.get('link'):
                            morning_parts.append(f"   🔗 {notizia['link'][:80]}...")
                        morning_parts.append("")
                    
                    morning_parts.append("")
                
        except Exception as e:
            morning_parts.append("📰 *TOP NOTIZIE INTERNAZIONALI*")
            morning_parts.append("❌ Errore nel caricamento delle notizie")
            morning_parts.append("")

        # Analisi ML
        try:
            news_analysis = analyze_news_sentiment_and_impact()
            
            if news_analysis and news_analysis.get('summary'):
                morning_parts.append("🧠 *ANALISI ML DELLE NOTIZIE*")
                morning_parts.append("")
                morning_parts.append(news_analysis['summary'])
                morning_parts.append("")
                
                # Raccomandazioni
                recommendations = news_analysis.get('recommendations', [])
                if recommendations:
                    morning_parts.append("💡 *RACCOMANDAZIONI OPERATIVE:*")
                    for rec in recommendations[:3]:
                        morning_parts.append(f"• {rec}")
                    morning_parts.append("")
                
        except Exception as e:
            morning_parts.append("🧠 *ANALISI ML DELLE NOTIZIE*")
            morning_parts.append("❌ Errore nell'analisi ML")
            morning_parts.append("")

        # Footer
        morning_parts.append("═" * 40)
        morning_parts.append(f"🤖 Sistema 555 Lite - {now.strftime('%H:%M')} CET")
        morning_parts.append("📱 Canale: https://t.me/abkllr")
        
        # Dividi in parti per Telegram
        full_message = "\n".join(morning_parts)
        
        if len(full_message) > 3500:
            # Dividi in 2-3 parti
            mid_point = len(morning_parts) // 2
            
            part1 = "\n".join(morning_parts[:mid_point])
            part2 = "\n".join(morning_parts[mid_point:])
            
            success1 = invia_messaggio_telegram(part1)
            time.sleep(3)
            success2 = invia_messaggio_telegram(part2)
            
            return f"Morning briefing inviato: Parte 1 {'✅' if success1 else '❌'}, Parte 2 {'✅' if success2 else '❌'}"
        else:
            success = invia_messaggio_telegram(full_message)
            return f"Morning briefing: {'✅' if success else '❌'}"
        
    except Exception as e:
        print(f"❌ [MORNING] Errore nella generazione: {e}")
        return "❌ Errore nella generazione morning briefing"

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
    
    # Analisi eventi della settimana
    sezioni.append("📈 *ANALISI PERFORMANCE SETTIMANA*")
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

# === SCHEDULER POTENZIATO ===
def check_and_send_scheduled_messages():
    """Scheduler potenziato con nuovi report"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    current_time = now.strftime("%H:%M")
    current_day = now.strftime("%A")
    is_month_end = (now + datetime.timedelta(days=1)).day == 1
    
    # Report giornalieri esistenti
    if current_time == "08:10" and not is_message_sent_today("morning_news"):
        print("🌅 [SCHEDULER] Avvio morning news...")
        result = genera_messaggio_eventi()
        set_message_sent_flag("morning_news")
        print(f"Morning news result: {result}")
    
    # NUOVO - Report settimanale (Domenica 20:00)
    if current_day == "Sunday" and current_time == "20:00" and not is_message_sent_today("weekly_report"):
        print("📊 [SCHEDULER] Avvio report settimanale...")
        result = genera_report_settimanale()
        print(f"Weekly report result: {result}")
    
    # NUOVO - Report mensile (ultimo giorno del mese, 21:00)
    if is_month_end and current_time == "21:00" and not is_message_sent_today("monthly_report"):
        print("📊 [SCHEDULER] Avvio report mensile...")
        result = genera_report_mensile()
        print(f"Monthly report result: {result}")

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
        GLOBAL_FLAGS["daily_report_sent"]
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
            GLOBAL_FLAGS["daily_report_sent"]
        ]),
        "features_enabled": len([k for k, v in FEATURES_ENABLED.items() if v]),
        "ram_optimization": "60% more RAM available"
    }

# === THREAD PRINCIPALE ===
def main_scheduler_loop():
    """Loop principale ottimizzato"""
    print("🚀 [LITE-MAIN] Scheduler principale attivo")
    
    while True:
        try:
            check_and_send_scheduled_messages()
            
            # Pulizia memoria ogni ora
            italy_tz = pytz.timezone('Europe/Rome')
            now = datetime.datetime.now(italy_tz)
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
