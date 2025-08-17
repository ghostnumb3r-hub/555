#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test specifico per Evening Report del sistema 555lite
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

# === CONFIGURAZIONE TELEGRAM ===
TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
TELEGRAM_CHAT_ID = "@abkllr"

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

def generate_evening_report_test():
    """NUOVO - Evening Report serale (20:10) - Versione TEST"""
    print("🌆 [TEST-EVENING] Generazione evening report...")
    
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
    
    # Breaking news simulate
    sezioni.append("📰 *BREAKING NEWS SERALI*")
    sezioni.append("")
    sezioni.append("🔴 **1.** *Fed Chair Powell: Interest rates may remain elevated longer...*")
    sezioni.append("📂 Finanza • 📰 Reuters")
    sezioni.append("🔗 https://reuters.com/markets/fed-powell-rates...")
    sezioni.append("")
    sezioni.append("🔴 **2.** *Bitcoin breaks $43,000 resistance on institutional buying...*")
    sezioni.append("📂 Criptovalute • 📰 CoinDesk")
    sezioni.append("🔗 https://coindesk.com/bitcoin-breaks-43k...")
    sezioni.append("")
    
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
    success = invia_messaggio_telegram_test(msg)
    
    return f"Evening report: {'✅' if success else '❌'}"

if __name__ == "__main__":
    print("🌆 [TEST] Avvio test Evening Report...")
    print("=" * 50)
    
    # Test della funzione
    result = generate_evening_report_test()
    print(f"📊 [TEST] Risultato: {result}")
    
    print("=" * 50)
    print("🌆 [TEST] Test Evening Report completato!")
