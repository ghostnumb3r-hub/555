#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test specifico per Daily Lunch Report del sistema 555lite
"""

import sys
import os
import datetime
import pytz

# Aggiungi la directory corrente al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import delle funzioni necessarie
from threading import Thread
import requests
import time
import feedparser

# === CONFIGURAZIONE TELEGRAM ===
TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
TELEGRAM_CHAT_ID = "@abkllr"

# === RSS FEEDS (Stesso del sistema principale) ===
RSS_FEEDS = {
    "Finanza": [
        "https://feeds.reuters.com/reuters/businessNews",
        "https://www.investing.com/rss/news_285.rss",
        "https://www.marketwatch.com/rss/topstories"
    ],
    "Criptovalute": [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
        "https://cryptoslate.com/feed/"
    ],
    "Geopolitica": [
        "https://feeds.reuters.com/Reuters/worldNews",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "http://feeds.bbci.co.uk/news/world/rss.xml"
    ]
}

def invia_messaggio_telegram_test(msg):
    """Versione di test per invio messaggio telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    print(f"📤 [TEST-TELEGRAM] Invio messaggio ({len(msg)} caratteri)")
    
    try:
        # Pulizia messaggio
        clean_msg = msg.replace('```', '`').replace('**', '*')
        
        # Gestione messaggi lunghi
        if len(clean_msg) > 2400:
            return send_long_message_test(clean_msg, url)
        else:
            return send_single_message_test(clean_msg, url)
            
    except Exception as e:
        print(f"❌ [TEST-TELEGRAM] Errore: {e}")
        return False

def send_single_message_test(clean_msg, url):
    """Invio singolo messaggio per test"""
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
                print(f"✅ [TEST-TELEGRAM] Inviato con {strategy['name']}")
                return True
        except Exception as e:
            print(f"⚠️ [TEST-TELEGRAM] Tentativo {strategy['name']} fallito: {e}")
            continue
    
    return False

def send_long_message_test(clean_msg, url):
    """Gestione messaggi lunghi per test"""
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
    
    # Invio sequenziale
    all_success = True
    for i, part in enumerate(parts):
        success = send_single_message_test(part, url)
        if not success:
            all_success = False
        
        if i < len(parts) - 1:
            time.sleep(1.5)
    
    return all_success

def get_notizie_critiche_test():
    """Recupero notizie critiche per test"""
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
        for url in feed_urls[:1]:  # Solo 1 feed per categoria per velocità test
            try:
                print(f"📡 [TEST-RSS] Controllo feed {categoria}: {url[:50]}...")
                parsed = feedparser.parse(url)
                if parsed.bozo or not parsed.entries:
                    continue
                
                for entry in parsed.entries[:3]:  # Max 3 per feed nel test
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
                        
                        if len(notizie_critiche) >= 3:  # Limitiamo a 3 per test
                            break
                
                if len(notizie_critiche) >= 3:
                    break
            except Exception as e:
                print(f"⚠️ [TEST-RSS] Errore feed {categoria}: {e}")
                continue
        
        if len(notizie_critiche) >= 3:
            break
    
    print(f"📰 [TEST-RSS] Trovate {len(notizie_critiche)} notizie critiche")
    return notizie_critiche[:3]  # Top 3 per test

def generate_daily_lunch_report_test():
    """NUOVO - Report di pranzo completo con analisi mercati (TEST - 14:10)"""
    print("🍽️ [TEST-LUNCH] Generazione daily lunch report...")
    
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
        notizie_critiche = get_notizie_critiche_test()
        if notizie_critiche:
            sezioni.append("🔥 *TOP NEWS MORNING → LUNCH*")
            sezioni.append("")
            
            for i, notizia in enumerate(notizie_critiche, 1):
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
        else:
            # Fallback notizie simulate se RSS non disponibili
            sezioni.append("🔥 *TOP NEWS MORNING → LUNCH*")
            sezioni.append("")
            sezioni.append("🚨 **1.** *Fed maintains hawkish stance on inflation targets*")
            sezioni.append("📂 Finanza • 📰 Reuters")
            sezioni.append("🔗 https://reuters.com/fed-hawkish-stance...")
            sezioni.append("")
            sezioni.append("📈 **2.** *Bitcoin consolidates above $42k support level*")
            sezioni.append("📂 Criptovalute • 📰 CoinDesk")
            sezioni.append("🔗 https://coindesk.com/bitcoin-42k-support...")
            sezioni.append("")
    except Exception as e:
        print(f"⚠️ [TEST-LUNCH] Errore nel recupero notizie: {e}")
        # Fallback a notizie simulate
        sezioni.append("🔥 *TOP NEWS MORNING → LUNCH*")
        sezioni.append("")
        sezioni.append("📈 **1.** *Markets show resilience amid global uncertainty*")
        sezioni.append("📂 Finanza • 📰 Market Analysis")
        sezioni.append("")
    
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
    success = invia_messaggio_telegram_test(msg)
    
    return f"Daily lunch report: {'✅' if success else '❌'}"

if __name__ == "__main__":
    print("🍽️ [TEST] Avvio test Daily Lunch Report...")
    print("=" * 50)
    
    # Test della funzione
    result = generate_daily_lunch_report_test()
    print(f"📊 [TEST] Risultato: {result}")
    
    print("=" * 50)
    print("🍽️ [TEST] Test Daily Lunch Report completato!")
