#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST PREVIEW - Anteprima messaggi Telegram per 555 Lite
Invia esempi dei messaggi per verificare il layout
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
    
    print(f"📤 [TEST] Invio messaggio ({len(msg)} caratteri)")
    
    try:
        clean_msg = msg.replace('```', '`').replace('**', '*')
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": clean_msg,
            "parse_mode": "Markdown"
        }
        
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print("✅ [TEST] Messaggio inviato con successo")
            return True
        else:
            print(f"❌ [TEST] Errore invio: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ [TEST] Errore: {e}")
        return False

def test_morning_news_categoria():
    """Test messaggio categoria (Messaggio 1-4)"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    msg = f"""💰 *MORNING NEWS - FINANZA*
📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 1/6
─────────────────────────────────────

🔥 **1.** *Fed signals hawkish stance on interest rates amid inflation...*
📰 Reuters
🔗 https://www.reuters.com/markets/us/fed-policy...

⚡ **2.** *Bank earnings exceed expectations, JPMorgan leads rally*
📰 Bloomberg
🔗 https://www.bloomberg.com/news/articles/bank-earnings...

📊 **3.** *European Central Bank maintains dovish tone despite pressure*
📰 Financial Times
🔗 https://www.ft.com/content/ecb-policy-decision...

🔥 **4.** *Treasury yields surge as investors price in rate hikes*
📰 MarketWatch
🔗 https://www.marketwatch.com/story/treasury-yields...

⚡ **5.** *Dollar strengthens against major currencies on Fed outlook*
📰 Wall Street Journal
🔗 https://www.wsj.com/articles/dollar-gains-fed...

📊 **6.** *Corporate bond spreads tighten amid strong earnings season*
📰 Investing.com
🔗 https://www.investing.com/news/corporate-bonds...

🔥 **7.** *Inflation data shows persistent price pressures in services*
📰 Trading Economics
🔗 https://tradingeconomics.com/inflation-report...

─────────────────────────────────────
🤖 555 Lite • Finanza (7 notizie)"""
    
    return invia_messaggio_telegram(msg)

def test_daily_lunch_report():
    """Test Daily Lunch Report (12:30)"""
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

def test_ml_analysis():
    """Test messaggio ML Analysis (Messaggio 5)"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    msg = f"""🧠 *MORNING NEWS - ANALISI ML*
📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 5/6
─────────────────────────────────────

📰 *RASSEGNA STAMPA ML*
🔴 *Sentiment*: NEGATIVE
🔥 *Impatto Mercati*: HIGH

💡 *RACCOMANDAZIONI OPERATIVE:*
• 📉 **Finanza**: Fed hawkish stance. Strategy: Short duration bonds, defensive stocks
• 📊 **Criptovalute**: Regulation uncertainty. Strategy: Reduce crypto exposure, hedge positions
• 📈 **Geopolitica**: Energy supply risk. Strategy: Long energy stocks, oil ETFs

🚨 *TOP 5 NOTIZIE CRITICHE (24H)*

🔴 **1.** *Fed signals more aggressive rate hikes to combat inflation surge...*
📂 Finanza • 📰 Reuters
🔗 https://www.reuters.com/markets/us/fed-aggressive-rates...

🔴 **2.** *Bitcoin regulation proposal sparks crypto market selloff concerns*
📂 Criptovalute • 📰 CoinDesk
🔗 https://www.coindesk.com/policy/2024/regulation-proposal...

🔴 **3.** *Geopolitical tensions escalate, oil supply disruption feared*
📂 Geopolitica • 📰 Bloomberg
🔗 https://www.bloomberg.com/news/articles/oil-supply-risk...

🔴 **4.** *Banking sector stress tests reveal vulnerabilities in regional banks*
📂 Finanza • 📰 Wall Street Journal
🔗 https://www.wsj.com/articles/banking-stress-tests...

🔴 **5.** *Emerging markets face capital flight as US yields surge higher*
📂 Mercati Emergenti • 📰 Financial Times
🔗 https://www.ft.com/content/emerging-markets-outflow...

─────────────────────────────────────
🤖 555 Lite • Analisi ML & Alert Critici"""
    
    return invia_messaggio_telegram(msg)

def test_final_outlook():
    """Test messaggio finale con ML Outlook (Messaggio 6)"""
    italy_tz = pytz.timezone('Europe/Rome')
    now = datetime.datetime.now(italy_tz)
    
    msg = f"""📅 *MORNING NEWS - CALENDARIO & ML OUTLOOK*
📅 {now.strftime('%d/%m/%Y %H:%M')} • Messaggio 6/6
─────────────────────────────────────

🧠 *RACCOMANDAZIONI ML CALENDARIO*

💡 *TOP 5 STRATEGIE OGGI:*
1. 📉 **Finanza**: Fed hawkish stance. Strategy: Short duration bonds, defensive stocks
2. 📊 **Criptovalute**: Range trading 40-43k, wait breakout direction
3. 📈 **Geopolitica**: Energy supply risk. Strategy: Long energy stocks, oil ETFs
4. 📊 **Mercati Emergenti**: EM currency pressure. Strategy: USD strength plays
5. 📉 **Risk Management**: VIX above 20, reduce overall market exposure

🚨 *ALERT CRITICI GIORNATA:*

⚠️ **1.** *Fed Chair Powell speech at 16:00 ET - High volatility expected*
📂 Finanza • Impact: HIGH
🔗 https://www.federalreserve.gov/newsevents/speech/powell...

⚠️ **2.** *Bitcoin regulation hearing in Congress - Crypto impact*
📂 Criptovalute • Impact: MEDIUM
🔗 https://www.congress.gov/committee-meetings/crypto-hearing...

⚠️ **3.** *OPEC emergency meeting on production cuts - Oil volatility*
📂 Geopolitica • Impact: HIGH
🔗 https://www.opec.org/opec_web/en/press_room/emergency...

🔮 *OUTLOOK MERCATI OGGI*
• 🇺🇸 Wall Street: Apertura 15:30 CET - Watch tech earnings
• 🇪🇺 Europa: Chiusura 17:30 CET - Banks & Energy focus
• ₿ Crypto: 24/7 - BTC key levels 42k-45k
• 🌍 Forex: London-NY overlap 14:00-17:00 CET

✅ *RASSEGNA STAMPA COMPLETATA*
📊 25 notizie analizzate
🌍 4 categorie coperte
🧠 5 raccomandazioni ML

🔮 *PROSSIMI AGGIORNAMENTI:*
• 🍽️ Daily Report: 12:30
• 📊 Weekly Report: Domenica 20:00
• 📅 Monthly Report: Fine mese 21:00

─────────────────────────────────────
🤖 555 Lite • Morning Briefing + ML Outlook"""
    
    return invia_messaggio_telegram(msg)

if __name__ == "__main__":
    print("🎯 [TEST] Avvio test anteprima messaggi Telegram...")
    print("📱 [TEST] I messaggi verranno inviati al canale @abkllr")
    print()
    
    # Test dei vari messaggi con pause
    import time
    
    print("1️⃣ Test Messaggio Categoria (Finanza)...")
    test_morning_news_categoria()
    time.sleep(3)
    
    print("\n2️⃣ Test Daily Lunch Report...")
    test_daily_lunch_report()
    time.sleep(3)
    
    print("\n3️⃣ Test ML Analysis...")
    test_ml_analysis()
    time.sleep(3)
    
    print("\n4️⃣ Test Final ML Outlook...")
    test_final_outlook()
    
    print("\n✅ [TEST] Test completato! Controlla il canale Telegram per vedere i risultati.")
