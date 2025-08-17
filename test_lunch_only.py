#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST LUNCH ONLY - Test specifico del Daily Lunch Report
"""

import datetime
import requests
import pytz

# === TELEGRAM CONFIG ===
TELEGRAM_TOKEN = "8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs"
TELEGRAM_CHAT_ID = "@abkllr"

def invia_messaggio_telegram(msg):
    """Invio messaggio Telegram semplificato per test"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    print(f"📤 [TEST-LUNCH] Invio messaggio ({len(msg)} caratteri)")
    
    try:
        clean_msg = msg.replace('```', '`').replace('**', '*')
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": clean_msg,
            "parse_mode": "Markdown"
        }
        
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print("✅ [TEST-LUNCH] Messaggio inviato con successo")
            return True
        else:
            print(f"❌ [TEST-LUNCH] Errore invio: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ [TEST-LUNCH] Errore: {e}")
        return False

def test_solo_lunch_report():
    """Test SOLO Daily Lunch Report"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    msg = f"""🍽️ *DAILY LUNCH REPORT*
📅 {now.strftime('%d/%m/%Y %H:%M')} • Aggiornamento Mezzogiorno
─────────────────────────────────────

📊 *MARKET PULSE LIVE*

🇺🇸 **Mercati USA:**
• Pre-market: Consolidamento, futures misti
• Apertura: 15:30 CET - Watch earnings

🇪🇺 **Europa (Chiusura):**
• FTSE MIB: +0.5% • DAX: +0.3% • CAC: -0.1%
• Banche: +0.8% • Tech: -0.2% • Energy: +1.1%

₿ **Crypto Markets:**
• BTC: $42,850 (+0.8%) - Range 42k-44k
• ETH: $2,680 (+1.2%) - Alt coins mixed

💱 **Forex & Commodities:**
• EUR/USD: 1.0895 (+0.1%) - Stabile
• Gold: $2,045 (-0.3%) - Oro sotto pressione
• Oil WTI: $74.20 (+1.2%) - Energy rally

🔥 *TOP NEWS MORNING → LUNCH*

🚨 **1.** *Fed Chair Powell speech moves markets, rates outlook...*
📂 Finanza • 📰 Reuters
🔗 https://www.reuters.com/markets/us/powell-speech...

📈 **2.** *Bitcoin ETF approval timeline updated by SEC officials*
📂 Criptovalute • 📰 CoinDesk
🔗 https://www.coindesk.com/policy/2024/btc-etf...

🚨 **3.** *European gas prices surge on supply concerns from Russia*
📂 Geopolitica • 📰 Bloomberg
🔗 https://www.bloomberg.com/news/articles/gas-prices...

🔮 *OUTLOOK POMERIGGIO* (13:00-18:00)

⏰ **Eventi Programmati:**
• 14:30 ET: Retail Sales USA (previsione -0.2%)
• 15:30 ET: Apertura Wall Street
• 16:00 ET: Fed Chair Powell speech
• 17:30 CET: Chiusura mercati europei

📊 **Focus Settoriali:**
• Tech: Earnings season, watch guidance
• Banks: Interest rate sensitivity
• Energy: Oil momentum continuation

⚡ *LIVELLI CHIAVE POMERIGGIO*

📈 **Equity Markets:**
• S&P 500: 4850 resistance | 4800 support
• NASDAQ: QQQ 410 pivot | Watch 405 breakdown
• Russell 2000: Small caps 1950 resistance

₿ **Crypto Levels:**
• BTC: 44k resistance critica | 41k strong support
• ETH: 2700 breakout level | 2600 key support

💱 **Forex Watch:**
• EUR/USD: 1.095 resistance | 1.085 support
• GBP/USD: 1.275 key level da monitorare

💡 *STRATEGIE OPERATIVE IMMEDIATE*

🎯 **Trading Setup:**
• Intraday: Range trading fino breakout
• Powell speech: preparare volatility hedges
• Tech earnings: selective long su dip

🛡️ **Risk Management:**
• VIX watch: se >20 ridurre esposizione
• Cash position: mantenere 15-20%
• Stop loss: tight su posizioni swing

─────────────────────────────────────
🤖 Sistema 555 Lite - {now.strftime('%H:%M')} CET
📊 Prossimo update: Weekly report (domenica 20:00)"""
    
    return invia_messaggio_telegram(msg)

if __name__ == "__main__":
    print("🍽️ [TEST-LUNCH] Test specifico Daily Lunch Report...")
    print("📱 [TEST-LUNCH] Invio al canale @abkllr")
    print()
    
    success = test_solo_lunch_report()
    
    if success:
        print("\n✅ [TEST-LUNCH] Daily Lunch Report inviato! Controlla il canale per vedere il layout.")
    else:
        print("\n❌ [TEST-LUNCH] Invio fallito.")
