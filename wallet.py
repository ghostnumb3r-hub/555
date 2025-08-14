import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
from wallet_analyzer import WalletAnalyzer
from recommendation_tracker import RecommendationTracker

app = dash.Dash(__name__)
server = app.server
app.title = "💼 Wallet Dashboard"

# Inizializza l'analizzatore del portafoglio e il tracker raccomandazioni
wallet_analyzer = WalletAnalyzer()
recommendation_tracker = RecommendationTracker()

# Configurazione per dati reali
import pandas_datareader.data as web

start = datetime.datetime.today() - datetime.timedelta(days=1800)
end = datetime.datetime.today()

symbols = {
    "Dollar Index": "DTWEXBGS",
    "S&P 500": "SP500",
    "Gold ($/oz)": "IR14270"
}

def get_fred_data():
    data = {}
    for name, code in symbols.items():
        try:
            df = web.DataReader(code, 'fred', start, end).dropna()
            df.columns = ['Value']
            data[name] = df
        except:
            continue
    return data

def get_btc_data():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=1800"
        r = requests.get(url)
        js = r.json()
        prices = js["Data"]["Data"]
        df = pd.DataFrame(prices)
        df['Date'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('Date', inplace=True)
        df = df[['close']].rename(columns={'close': 'Value'})
        return df.dropna()
    except:
        return pd.DataFrame()

def get_performance(df, days):
    result = {}
    try:
        ref_date = df.index[-1] - pd.Timedelta(days=days)
        closest = df.index[df.index.get_indexer([ref_date], method="nearest")[0]]
    except:
        return result
    for col in df.columns:
        try:
            now = df[col].iloc[-1]
            past = df[col].loc[closest]
            delta = ((now - past) / past) * 100
            direction = "📈 Su" if delta > 0.5 else "📉 Giù" if delta < -0.5 else "⏸️ Stabile"
            result[col] = {"change": round(delta, 2), "direction": direction}
        except:
            result[col] = {"change": None, "direction": "ND"}
    return result

# Carica dati reali
print("📈 Caricamento dati di mercato...")
data = get_fred_data()
btc_df = get_btc_data()
if not btc_df.empty:
    data["Bitcoin"] = btc_df

# Crea DataFrame unificato
if data:
    df_all = pd.concat([df["Value"] for df in data.values()], axis=1)
    df_all.columns = list(data.keys())
    df_all.dropna(inplace=True)
    df_norm = df_all / df_all.iloc[0] * 100 if not df_all.empty else pd.DataFrame()
    
    # Calcola performance reali
    perf_1w = get_performance(df_all, 7)
    perf_1m = get_performance(df_all, 30)
    perf_6m = get_performance(df_all, 180)
    perf_1y = get_performance(df_all, 365)
    print(f"✅ Caricati dati per {len(df_all.columns)} asset: {list(df_all.columns)}")
else:
    # Fallback ai dati mock in caso di problemi
    df_norm = pd.DataFrame()
    perf_1w = {"Bitcoin": {"change": 5.23, "direction": "📈 Su"}, "Gold ($/oz)": {"change": -1.45, "direction": "📉 Giù"}}
    perf_1m = {"Bitcoin": {"change": 12.67, "direction": "📈 Su"}, "Gold ($/oz)": {"change": 2.34, "direction": "📈 Su"}}
    perf_6m = {"Bitcoin": {"change": 45.12, "direction": "📈 Su"}, "Gold ($/oz)": {"change": 8.90, "direction": "📈 Su"}}
    perf_1y = {"Bitcoin": {"change": 89.45, "direction": "📈 Su"}, "Gold ($/oz)": {"change": 15.23, "direction": "📈 Su"}}
    df_all = pd.DataFrame({'Bitcoin': [1, 2], 'Gold ($/oz)': [1, 2]})  # Mock data per tabella
    print("⚠️ Usando dati mock - problemi di connessione ai mercati")

def get_4_assets_recommendations():
    """Genera raccomandazioni intelligenti per i 4 asset principali basate su esposizione portafoglio REALE"""
    assets_data = []
    
    # DISTRIBUZIONE REALE DEL PORTAFOGLIO (aggiornata da wallet_data.csv)
    # Totale portafoglio: €57,893.48
    portfolio_exposure = {
        "Bitcoin": 88.3,         # ESTREMAMENTE sovraesposto - RISCHIO ALTISSIMO
        "Cash/Liquidità": 8.6,   # Discreto, ma potrebbe servire di più in caso di correzioni
        "Gold": 2.4,           # Sottopeso critico - manca diversificazione
        "ETF S&P500": 0.7      # Sottopeso estremo - quasi assente
    }
    
    # Target allocation ideali RIVISTI (strategia cash tattica)
    main_assets = [
        {"asset": "Bitcoin", "symbol": "🟠", "risk": "ALTISSIMO", "category": "Crypto", "target_min": 30, "target_max": 55},
        {"asset": "Cash/Liquidità", "symbol": "💵", "risk": "BASSO", "category": "Liquidi", "target_min": 20, "target_max": 25},  # Range ideale per strategia tattica
        {"asset": "Gold", "symbol": "🥇", "risk": "MEDIO", "category": "Safe Haven", "target_min": 8, "target_max": 20},
        {"asset": "ETF S&P500", "symbol": "📈", "risk": "MEDIO-ALTO", "category": "Equity", "target_min": 15, "target_max": 35}
    ]
    
    # Simulazione performance e ML (seed fisso per consistenza)
    import random
    random.seed(42)
    
    for asset_info in main_assets:
        asset_name = asset_info['asset']
        current_exposure = portfolio_exposure[asset_name]
        target_min = asset_info['target_min']
        target_max = asset_info['target_max']
        
        # Simula performance e ML
        perf_1w = round(random.uniform(-12, 18), 2)
        prob_ml = random.randint(35, 80)
        
        # LOGICA NUOVA per distribuzione reale wallet
        
        # Per Bitcoin (88.3% - ESTREMAMENTE sovraesposto)
        if asset_name == "Bitcoin":
            if current_exposure > 55:  # Estremamente sovraesposto
                signal = "SELL"
                action = "RIDUCI ESPOSIZIONE"
                reason = f"Molto sovraesposto ({current_exposure}%) - Rischio elevato di concentrazione"
            elif current_exposure > target_max:
                signal = "SELL"
                action = "VENDI GRADUALMENTE"
                reason = f"Sovraesposto ({current_exposure}%) - Suggerito ribilanciamento"
            else:
                signal = "HOLD"
                action = "MANTIENI"
                reason = f"Esposizione accettabile ({current_exposure}%)"
        
        # Per Gold (2.4% - Sottopeso)
        elif asset_name == "Gold":
            if current_exposure < target_min:
                signal = "BUY"
                action = "AUMENTA POSIZIONE"
                if current_exposure < 5:
                    reason = f"Sottopeso ({current_exposure}%) - Utile diversificazione in incertezza"
                else:
                    reason = f"Sottopeso ({current_exposure}%) - Considera aumentare per safe haven"
            else:
                signal = "HOLD"
                action = "MANTIENI"
                reason = f"Esposizione adeguata ({current_exposure}%)"
        
        # Per ETF S&P500 (0.7% - Quasi assente)
        elif asset_name == "ETF S&P500":
            if current_exposure < target_min:
                signal = "BUY"
                action = "AUMENTA POSIZIONE"
                if current_exposure < 5:
                    reason = f"Molto sottopeso ({current_exposure}%) - Ribilanciamento consigliato"
                else:
                    reason = f"Sottopeso ({current_exposure}%) - Utile diversificazione azionaria"
            else:
                signal = "HOLD"
                action = "MANTIENI"
                reason = f"Esposizione adeguata ({current_exposure}%)"
        
        # Per Cash/Liquidità (8.6% - Strategia tattica avanzata)
        elif asset_name == "Cash/Liquidità":
            # STRATEGIA CASH AVANZATA: 20-25% ideale, crash/opportunità logic
            
            # Simula contesto di mercato (basato su ML probability come proxy sentiment)
            market_context = "NEUTRO"
            if prob_ml > 70:
                market_context = "BULL_MARKET"  # Mercato forte - meno cash
            elif prob_ml < 35:
                market_context = "CRASH_OPPORTUNITY"  # Crash/correzione - usa cash per comprare
            elif prob_ml < 45:
                market_context = "INCERTEZZA"  # Mercati incerti - aumenta cash
                
            # Determina target cash dinamico in base al contesto
            if market_context == "INCERTEZZA":
                target_cash_min, target_cash_max = 25, 30  # Più cash in incertezza
            elif market_context == "CRASH_OPPORTUNITY":
                target_cash_min, target_cash_max = 10, 15  # Meno cash, si investe
            elif market_context == "BULL_MARKET":
                target_cash_min, target_cash_max = 15, 22  # Cash moderato
            else:  # NEUTRO
                target_cash_min, target_cash_max = 20, 25  # Range ideale standard
            
            # Logica decisionale cash
            if current_exposure < 10:  # Cash molto basso - critico
                signal = "BUY"
                action = "INCREMENTA LIQUIDITÀ"
                reason = f"Liquidità critica ({current_exposure}%) - Rischio di vendita forzata in perdita"
                
            elif current_exposure > 30:  # Cash molto alto
                signal = "SELL"
                action = "INVESTI ECCESSO CASH"
                reason = f"Cash eccessivo ({current_exposure}%) - Perdita opportunità, drag sulla performance"
                
            elif current_exposure < target_cash_min:  # Sotto target dinamico
                if market_context == "INCERTEZZA":
                    signal = "BUY"
                    action = "AUMENTA CASH - DIFESA"
                    reason = f"Cash sotto target ({current_exposure}% vs {target_cash_min}%) - Preparazione per incertezza/crash"
                elif market_context == "BULL_MARKET":
                    signal = "BUY"
                    action = "RIEQUILIBRA CASH"
                    reason = f"Cash sotto target ({current_exposure}% vs {target_cash_min}%) - Mantieni liquidità minima"
                else:
                    signal = "BUY"
                    action = "INCREMENTA GRADUALMENTE"
                    reason = f"Cash sotto target ({current_exposure}% vs {target_cash_min}%) - Riequilibrio prudente"
                    
            elif current_exposure > target_cash_max:  # Sopra target dinamico
                if market_context == "CRASH_OPPORTUNITY":
                    signal = "SELL"
                    action = "INVESTI IN CRASH"
                    reason = f"Cash sopra target ({current_exposure}% vs {target_cash_max}%) - Opportunità di acquisto a sconto"
                elif market_context == "BULL_MARKET":
                    signal = "SELL"
                    action = "RIDUCI CASH - INVESTI"
                    reason = f"Cash sopra target ({current_exposure}% vs {target_cash_max}%) - Mercato forte, partecipa alla crescita"
                else:
                    signal = "HOLD"
                    action = "MANTIENI - MONITORA"
                    reason = f"Cash sopra target ({current_exposure}% vs {target_cash_max}%) - Attendi chiarezza di mercato"
                    
            else:  # Nel target dinamico ideale
                if market_context == "CRASH_OPPORTUNITY" and current_exposure > 20:
                    signal = "SELL"
                    action = "USA CASH PER CRASH"
                    reason = f"Cash nel target ({current_exposure}%) - Usa parte per acquisti in correzione (cash to work)"
                else:
                    signal = "HOLD"
                    action = "MANTIENI - OTTIMALE"
                    reason = f"Cash ottimale ({current_exposure}%) - Strategia tattica ben posizionata per contesto {market_context.lower()}"
        
        # Fallback per altri asset
        else:
            if current_exposure > target_max:
                signal = "SELL"
                action = "RIDUCI ESPOSIZIONE"
                reason = f"Sovraesposto ({current_exposure}%) - Ribilanciamento necessario"
            elif current_exposure < target_min:
                signal = "BUY"
                action = "AUMENTA POSIZIONE"
                reason = f"Sottopeso ({current_exposure}%) - Opportunità diversificazione"
            else:
                signal = "HOLD"
                action = "MANTIENI"
                reason = f"Esposizione bilanciata ({current_exposure}%)"
        
        # Override basato su segnali ML se molto forti
        if prob_ml >= 75 and signal == "SELL" and asset_info['risk'] != 'ALTISSIMO':
            signal = "HOLD"
            action = "MANTIENI - ML POSITIVO"
            reason += f" [ML molto positivo: {prob_ml}%]"
        elif prob_ml <= 25 and signal == "BUY":
            signal = "HOLD"
            action = "MANTIENI - ML NEGATIVO"
            reason += f" [ML molto negativo: {prob_ml}%]"
        # Calcola target ideale dinamico (per cash usa il target dinamico)
        if asset_name == "Cash/Liquidità":
            # Usa i target dinamici calcolati sopra
            market_context = "NEUTRO"
            if prob_ml > 70:
                market_context = "BULL_MARKET"
            elif prob_ml < 35:
                market_context = "CRASH_OPPORTUNITY"
            elif prob_ml < 45:
                market_context = "INCERTEZZA"
                
            if market_context == "INCERTEZZA":
                target_ideal = "25-30%"  # Più cash in incertezza
            elif market_context == "CRASH_OPPORTUNITY":
                target_ideal = "10-15%"  # Meno cash, si investe
            elif market_context == "BULL_MARKET":
                target_ideal = "15-22%"  # Cash moderato
            else:  # NEUTRO
                target_ideal = "20-25%"  # Range ideale standard
        else:
            # Per altri asset usa il target fisso
            target_ideal = f"{target_min}-{target_max}%"
            
        assets_data.append({
            "Asset": f"{asset_info['symbol']} {asset_info['asset']}",
            "Categoria": asset_info['category'],
            "Rischio": asset_info['risk'],
            "Esposizione Attuale": f"{current_exposure}%",
            "Ribilanciamento Ideale": target_ideal,
            "Performance 1W": f"{perf_1w:+.2f}%",
            "ML Probability": f"{prob_ml}%",
            "Segnale": signal,
            "Azione": action,
            "Motivazione": reason
        })
    
    return assets_data


# === Wallet ===
def load_and_save_wallet_data():
    """Carica i dati del portafoglio da Google Sheets e li salva per 555bt"""
    csv_url = "https://docs.google.com/spreadsheets/d/1gFLCD6pggapfhgxTJYcgCkttSWCeSHe92P7cvKUPA8A/export?format=csv&gid=0"
    
    try:
        print("💼 Caricamento dati portafoglio da Google Sheets...")
        wallet_df = pd.read_csv(csv_url)
        wallet_df.columns = ['Categoria', 'Asset', 'Ticker', 'Prezzo', 'Quantità', 'Totale']
        
        for col in ['Prezzo', 'Quantità', 'Totale']:
            wallet_df[col] = wallet_df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        
        wallet_df = wallet_df[wallet_df['Totale'] > 0]
        wallet_df['Categoria'] = wallet_df['Categoria'].fillna('Altro')
        
        # Crea la cartella salvataggi se non esiste
        os.makedirs('salvataggi', exist_ok=True)
        
        # Salva i dati per 555bt con timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wallet_df['Timestamp'] = timestamp
        
        # File per 555bt
        wallet_path = os.path.join('salvataggi', 'wallet_data.csv')
        wallet_df.to_csv(wallet_path, index=False, encoding='utf-8-sig')
        
        # Salva anche una versione con analisi estesa
        wallet_analysis = analyze_wallet_composition(wallet_df)
        analysis_path = os.path.join('salvataggi', 'wallet_analysis.csv')
        wallet_analysis.to_csv(analysis_path, index=False, encoding='utf-8-sig')
        
        print(f"✅ Dati portafoglio salvati per 555bt:")
        print(f"   📊 Composizione: {wallet_path}")
        print(f"   📈 Analisi: {analysis_path}")
        print(f"   💰 Valore totale: €{wallet_df['Totale'].sum():,.2f}")
        print(f"   📋 Asset: {len(wallet_df)} posizioni")
        
        return wallet_df
        
    except Exception as e:
        print(f"❌ Errore caricamento portafoglio: {e}")
        return pd.DataFrame(columns=['Categoria', 'Asset', 'Ticker', 'Prezzo', 'Quantità', 'Totale', 'Timestamp'])

def analyze_wallet_composition(wallet_df):
    """Analizza la composizione del portafoglio per 555bt"""
    if wallet_df.empty:
        return pd.DataFrame()
    
    total_value = wallet_df['Totale'].sum()
    analysis_data = []
    
    # Analisi per categoria
    category_analysis = wallet_df.groupby('Categoria').agg({
        'Totale': ['sum', 'count'],
        'Asset': 'count'
    }).round(2)
    
    category_analysis.columns = ['Valore_Totale', 'Posizioni', 'Numero_Asset']
    category_analysis['Percentuale'] = (category_analysis['Valore_Totale'] / total_value * 100).round(2)
    category_analysis.reset_index(inplace=True)
    
    # Aggiungi metriche di rischio per categoria
    for _, row in category_analysis.iterrows():
        categoria = row['Categoria']
        valore = row['Valore_Totale']
        percentuale = row['Percentuale']
        
        # Determina livello di rischio per categoria
        if categoria in ['Criptovalute', 'Crypto']:
            risk_level = 'ALTO'
            volatility_score = 8.5
        elif categoria in ['Azioni', 'Equity', 'Stocks']:
            risk_level = 'MEDIO-ALTO'
            volatility_score = 6.5
        elif categoria in ['Obbligazioni', 'Bonds', 'Fixed Income']:
            risk_level = 'BASSO-MEDIO'
            volatility_score = 3.5
        elif categoria in ['Cash', 'Liquidità', 'Money Market']:
            risk_level = 'BASSO'
            volatility_score = 1.0
        else:
            risk_level = 'MEDIO'
            volatility_score = 5.0
        
        analysis_data.append({
            'Categoria': categoria,
            'Valore_Euro': valore,
            'Percentuale_Portafoglio': percentuale,
            'Numero_Posizioni': row['Posizioni'],
            'Risk_Level': risk_level,
            'Volatility_Score': volatility_score,
            'Raccomandazione': get_category_recommendation(percentuale, risk_level),
            'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(analysis_data)

def get_category_recommendation(percentage, risk_level):
    """Genera raccomandazioni basate su percentuale e rischio"""
    if risk_level == 'ALTO' and percentage > 20:
        return 'RIDURRE - Eccessiva esposizione ad alto rischio'
    elif risk_level == 'ALTO' and percentage < 5:
        return 'MANTENERE - Esposizione conservativa'
    elif risk_level == 'MEDIO-ALTO' and percentage > 60:
        return 'RIBILANCIARE - Troppa concentrazione'
    elif risk_level == 'BASSO' and percentage > 30:
        return 'DIVERSIFICARE - Troppo conservativo'
    elif 5 <= percentage <= 20 and risk_level in ['ALTO', 'MEDIO-ALTO']:
        return 'OTTIMALE - Buon bilanciamento'
    else:
        return 'MONITORARE - Valutare ribilanciamento'

# === FUNZIONI PER LEGGERE ANALISI 555BT ===
def load_555bt_analysis():
    """Carica i risultati dell'analisi ML e indicatori da 555bt"""
    analysis_results = {
        'ml_predictions': [],
        'technical_signals': [],
        'portfolio_recommendations': [],
        'last_update': None,
        'available': False
    }
    
    # File che 555bt genera
    ml_file = os.path.join('salvataggi', 'previsioni_ml.csv')
    signals_file = os.path.join('salvataggi', 'segnali_tecnici.csv')
    portfolio_file = os.path.join('salvataggi', 'portfolio_analysis.txt')
    
    try:
        # Carica previsioni ML con enhancement
        if os.path.exists(ml_file):
            ml_df = pd.read_csv(ml_file)
            if not ml_df.empty:
                # Aggiungi segnali e raccomandazioni basati su probabilità
                ml_enhanced = enhance_ml_predictions(ml_df)
                analysis_results['ml_predictions'] = ml_enhanced
                analysis_results['available'] = True
                print(f"✅ [WALLET] Caricati {len(ml_enhanced)} segnali ML da 555bt (enhanced)")
        
        # Carica segnali tecnici
        if os.path.exists(signals_file):
            signals_df = pd.read_csv(signals_file)
            if not signals_df.empty:
                analysis_results['technical_signals'] = signals_df.to_dict('records')
                print(f"✅ [WALLET] Caricati {len(signals_df)} segnali tecnici da 555bt")
        
        # Aggiungi Gold alle previsioni ML se mancante, usando i segnali tecnici
        if analysis_results['ml_predictions'] and analysis_results['technical_signals']:
            analysis_results['ml_predictions'] = add_missing_gold_prediction(
                analysis_results['ml_predictions'], 
                analysis_results['technical_signals']
            )
        
        # Genera raccomandazioni per tutti gli asset
        analysis_results['portfolio_recommendations'] = generate_all_assets_recommendations(analysis_results)
        analysis_results['last_update'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        print(f"✅ [WALLET] Generate raccomandazioni per tutti gli asset")
        
        return analysis_results
        
    except Exception as e:
        print(f"❌ [WALLET] Errore caricamento analisi 555bt: {e}")
        return analysis_results

def enhance_ml_predictions(ml_df):
    """Aggiunge segnali e raccomandazioni alle previsioni ML"""
    enhanced_predictions = []
    
    for _, row in ml_df.iterrows():
        prediction = row.to_dict()
        probabilita = float(row.get('Probabilità', 0))
        
        # Calcola segnale basato su probabilità
        if probabilita >= 65:
            segnale = "BUY"
            segnale_emoji = "🟢"
            raccomandazione = "ACQUISTO - Segnale forte"
        elif probabilita >= 55:
            segnale = "BUY"
            segnale_emoji = "🟢"
            raccomandazione = "ACQUISTO - Segnale moderato"
        elif probabilita <= 35:
            segnale = "SELL"
            segnale_emoji = "🔴"
            raccomandazione = "VENDITA - Segnale forte"
        elif probabilita <= 45:
            segnale = "SELL"
            segnale_emoji = "🔴"
            raccomandazione = "VENDITA - Segnale moderato"
        else:
            segnale = "HOLD"
            segnale_emoji = "🟡"
            raccomandazione = "MANTIENI - Segnale neutro"
        
        # Aggiungi nuove colonne
        prediction['Segnale'] = segnale
        prediction['Segnale_Emoji'] = segnale_emoji
        prediction['Raccomandazione'] = raccomandazione
        prediction['Prob_Formatted'] = f"{probabilita:.1f}%"
        
        enhanced_predictions.append(prediction)
    
    return enhanced_predictions

def add_missing_gold_prediction(enhanced_predictions, technical_signals):
    """Aggiunge Gold alle previsioni ML se mancante, usando segnali tecnici"""
    # Controlla se Gold è già presente
    existing_assets = [pred['Asset'] for pred in enhanced_predictions]
    gold_variants = ['Gold', 'Gold ($/oz)', 'Gold (PAXG)']
    
    has_gold = any(any(variant in asset for variant in gold_variants) for asset in existing_assets)
    
    if not has_gold and technical_signals:
        # Cerca Gold nei segnali tecnici
        gold_tech_signal = None
        for signal in technical_signals:
            asset = signal.get('Asset', '')
            if 'Gold' in asset or 'PAXG' in asset:
                gold_tech_signal = signal
                break
        
        if gold_tech_signal:
            # Conta segnali BUY/SELL/HOLD dai tecnici
            buy_count = 0
            sell_count = 0
            hold_count = 0
            
            for key, value in gold_tech_signal.items():
                if key not in ['Asset', 'Data', 'Timeframe']:
                    if value == 'Buy':
                        buy_count += 1
                    elif value == 'Sell':
                        sell_count += 1
                    elif value == 'Hold':
                        hold_count += 1
            
            # Calcola probabilità simulata basata sui segnali tecnici
            total_signals = buy_count + sell_count + hold_count
            if total_signals > 0:
                buy_ratio = buy_count / total_signals
                sell_ratio = sell_count / total_signals
                
                # Simula probabilità: più BUY = probabilità più alta
                if buy_ratio >= 0.6:
                    probabilita_sim = 65 + (buy_ratio * 20)  # 65-85%
                elif sell_ratio >= 0.6:
                    probabilita_sim = 35 - (sell_ratio * 20)  # 15-35%
                else:
                    probabilita_sim = 50  # Neutro
                
                # Determina segnale
                if probabilita_sim >= 65:
                    segnale = "BUY"
                    segnale_emoji = "🟢"
                    raccomandazione = "ACQUISTO - Basato su indicatori tecnici"
                elif probabilita_sim <= 35:
                    segnale = "SELL"
                    segnale_emoji = "🔴"
                    raccomandazione = "VENDITA - Basato su indicatori tecnici"
                else:
                    segnale = "HOLD"
                    segnale_emoji = "🟡"
                    raccomandazione = "MANTIENI - Segnali tecnici misti"
                
                # Crea predizione simulata per Gold
                gold_prediction = {
                    'Modello': 'Indicatori Tecnici',
                    'Asset': 'Gold (PAXG)',
                    'Probabilità': probabilita_sim,
                    'Accuratezza': 'N/A - Tecnici',
                    'Orizzonte': '1 settimana',
                    'Data': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Segnale': segnale,
                    'Segnale_Emoji': segnale_emoji,
                    'Raccomandazione': raccomandazione,
                    'Prob_Formatted': f"{probabilita_sim:.1f}%"
                }
                
                enhanced_predictions.append(gold_prediction)
                print(f"✅ [WALLET] Aggiunto Gold alle previsioni ML (basato su {buy_count} BUY, {sell_count} SELL tecnici)")
    
    return enhanced_predictions

def generate_all_assets_recommendations(analysis_results):
    """Genera raccomandazioni per tutti gli asset (Bitcoin, Gold, ETF, Cash)"""
    recommendations = []
    
    # Asset del portafoglio
    portfolio_assets = {
        'Bitcoin': {'categoria': 'CRYPTO', 'rischio': 'ALTO'},
        'Gold': {'categoria': 'COMMODITIES', 'rischio': 'MEDIO'},
        'ETF': {'categoria': 'EQUITY', 'rischio': 'MEDIO'},
        'Cash': {'categoria': 'LIQUIDITA', 'rischio': 'BASSO'}
    }
    
    # Ottieni segnali ML per asset
    ml_signals = {}
    if analysis_results['ml_predictions']:
        for pred in analysis_results['ml_predictions']:
            asset = pred.get('Asset', '')
            if 'Bitcoin' in asset:
                ml_signals['Bitcoin'] = pred
            elif 'Gold' in asset:
                ml_signals['Gold'] = pred
            elif 'S&P 500' in asset:
                ml_signals['ETF'] = pred
    
    # Ottieni segnali tecnici per asset
    tech_signals = {}
    if analysis_results['technical_signals']:
        for signal in analysis_results['technical_signals']:
            asset = signal.get('Asset', '')
            if 'Bitcoin' in asset:
                tech_signals['Bitcoin'] = signal
            elif 'Gold' in asset or 'PAXG' in asset:
                tech_signals['Gold'] = signal
            elif 'S&P 500' in asset:
                tech_signals['ETF'] = signal
    
    # Genera raccomandazioni per ogni asset
    for asset, info in portfolio_assets.items():
        ml_signal = ml_signals.get(asset, {})
        tech_signal = tech_signals.get(asset, {})
        
        # Determina azione consigliata
        ml_segnale = ml_signal.get('Segnale', 'HOLD')
        ml_prob = ml_signal.get('Probabilità', 50)
        
        # Conta segnali tecnici BUY/SELL
        buy_signals = 0
        sell_signals = 0
        if tech_signal:
            for key, value in tech_signal.items():
                if key not in ['Asset', 'Data', 'Timeframe']:
                    if value == 'Buy':
                        buy_signals += 1
                    elif value == 'Sell':
                        sell_signals += 1
        
        # Logica di raccomandazione combinata
        if ml_segnale == 'BUY' and buy_signals > sell_signals:
            action = "FORTE ACQUISTO"
            priority = "ALTA"
            reason = f"ML: {ml_segnale} ({ml_prob:.1f}%) + Tecnici: {buy_signals} BUY vs {sell_signals} SELL"
        elif ml_segnale == 'SELL' and sell_signals > buy_signals:
            action = "FORTE VENDITA"
            priority = "ALTA"
            reason = f"ML: {ml_segnale} ({ml_prob:.1f}%) + Tecnici: {sell_signals} SELL vs {buy_signals} BUY"
        elif ml_segnale == 'BUY':
            action = "ACQUISTO MODERATO"
            priority = "MEDIA"
            reason = f"ML: {ml_segnale} ({ml_prob:.1f}%)"
        elif ml_segnale == 'SELL':
            action = "VENDITA MODERATA"
            priority = "MEDIA"
            reason = f"ML: {ml_segnale} ({ml_prob:.1f}%)"
        else:
            action = "MANTIENI"
            priority = "BASSA"
            reason = f"Segnali contrastanti - ML: {ml_prob:.1f}%"
        
        # Suggerimento specifico
        if info['rischio'] == 'ALTO' and action in ['FORTE ACQUISTO', 'ACQUISTO MODERATO']:
            suggestion = "⚠️ Asset ad alto rischio - Considera position sizing ridotto"
        elif info['rischio'] == 'BASSO' and action in ['FORTE VENDITA', 'VENDITA MODERATA']:
            suggestion = "💰 Mantieni liquidità per opportunità future"
        else:
            suggestion = f"📊 Monitora evoluzione segnali per {info['categoria']}"
        
        recommendations.append({
            'asset': asset,
            'action': action,
            'priority': priority,
            'reason': reason,
            'suggestion': suggestion,
            'ml_signal': ml_segnale,
            'tech_buy': buy_signals,
            'tech_sell': sell_signals,
            'risk_level': info['rischio']
        })
    
    return recommendations

def extract_recommendations_from_text(portfolio_content):
    """Estrae raccomandazioni dal testo dell'analisi portafoglio"""
    recommendations = []
    try:
        lines = portfolio_content.split('\n')
        in_recommendations = False
        current_rec = {}
        
        for line in lines:
            line = line.strip()
            if 'RACCOMANDAZIONI OPERATIVE' in line:
                in_recommendations = True
                continue
            elif in_recommendations:
                if line.startswith('•') and '**' in line:
                    # Nueva raccomandazione
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    # Estrai asset e azione
                    parts = line.split('**')
                    if len(parts) >= 3:
                        asset = parts[1]
                        action = parts[2].replace(':', '').strip()
                        current_rec = {
                            'asset': asset,
                            'action': action,
                            'details': []
                        }
                elif line.startswith('📋') or line.startswith('💡'):
                    # Dettagli della raccomandazione
                    if current_rec:
                        current_rec['details'].append(line)
                elif line.startswith('🔴') or line.startswith('🟡'):
                    # Nuova sezione di priorità
                    if current_rec:
                        recommendations.append(current_rec)
                        current_rec = {}
        
        # Aggiungi l'ultima raccomandazione
        if current_rec:
            recommendations.append(current_rec)
        
        return recommendations
    except Exception as e:
        print(f"❌ [WALLET] Errore estrazione raccomandazioni: {e}")
        return []

# Carica e salva i dati del portafoglio
wallet_df = load_and_save_wallet_data()

# === Layout ===
app.layout = html.Div([
    html.H1("💼 Wallet Dashboard", style={"textAlign": "center", "marginBottom": "30px", "color": "#2c3e50"}),
    
    # === SEZIONE ANDAMENTI ===
    html.Div([
        html.H2("📈 Andamenti Asset", style={"color": "#2c3e50", "marginBottom": "20px"}),
        
        # Grafico andamenti normalizzati
        html.Div([
            dcc.Graph(
                figure=px.line(df_norm, title="📊 Andamenti Normalizzati (Base 100)", labels={"value": "Base 100"})
                if not df_norm.empty else px.line(title="📊 Nessun dato disponibile")
            )
        ], style={"marginBottom": "30px"}),
        
        # Tabella performance
        html.H4("📊 Performance % & Direzione", style={"color": "#2c3e50"}),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Asset", style={"backgroundColor": "#3498db", "color": "white", "padding": "10px"}),
                html.Th("1 Settimana", style={"backgroundColor": "#3498db", "color": "white", "padding": "10px"}),
                html.Th("1 Mese", style={"backgroundColor": "#3498db", "color": "white", "padding": "10px"}),
                html.Th("6 Mesi", style={"backgroundColor": "#3498db", "color": "white", "padding": "10px"}),
                html.Th("1 Anno", style={"backgroundColor": "#3498db", "color": "white", "padding": "10px"})
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(asset, style={"padding": "8px", "fontWeight": "bold"}),
                    html.Td(f"{perf_1w[asset]['change']}% {perf_1w[asset]['direction']}", 
                           style={"padding": "8px", "color": "#27ae60" if perf_1w[asset]['change'] and perf_1w[asset]['change'] > 0 else "#e74c3c" if perf_1w[asset]['change'] and perf_1w[asset]['change'] < 0 else "#7f8c8d"}),
                    html.Td(f"{perf_1m[asset]['change']}% {perf_1m[asset]['direction']}", 
                           style={"padding": "8px", "color": "#27ae60" if perf_1m[asset]['change'] and perf_1m[asset]['change'] > 0 else "#e74c3c" if perf_1m[asset]['change'] and perf_1m[asset]['change'] < 0 else "#7f8c8d"}),
                    html.Td(f"{perf_6m[asset]['change']}% {perf_6m[asset]['direction']}", 
                           style={"padding": "8px", "color": "#27ae60" if perf_6m[asset]['change'] and perf_6m[asset]['change'] > 0 else "#e74c3c" if perf_6m[asset]['change'] and perf_6m[asset]['change'] < 0 else "#7f8c8d"}),
                    html.Td(f"{perf_1y[asset]['change']}% {perf_1y[asset]['direction']}", 
                           style={"padding": "8px", "color": "#27ae60" if perf_1y[asset]['change'] and perf_1y[asset]['change'] > 0 else "#e74c3c" if perf_1y[asset]['change'] and perf_1y[asset]['change'] < 0 else "#7f8c8d"})
                ]) for asset in df_all.columns
            ])
        ], style={"width": "100%", "border": "1px solid #ddd", "borderRadius": "5px", "marginBottom": "40px"})
    ], style={"padding": "20px", "backgroundColor": "#f8f9fa", "borderRadius": "10px", "marginBottom": "30px"}),

    # === SEZIONE PORTAFOGLIO ===
    html.Hr(style={"margin": "40px 0", "border": "2px solid #3498db"}),
    
    html.Div([
        html.Div([
            html.H2("💼 EurExelWallet", style={"color": "#2c3e50", "marginBottom": "20px", "display": "inline-block"}),
            html.Button("🔄 Aggiorna Dati", id="refresh-wallet-button", n_clicks=0,
                       style={"padding": "8px 15px", "backgroundColor": "#e67e22", "color": "white", 
                             "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginLeft": "20px",
                             "fontSize": "14px", "fontWeight": "bold"}),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
        
        html.Div(id="wallet-refresh-status", style={"marginBottom": "10px"}),
        
        html.Button("👁️ Mostra/Nascondi Portafoglio", id="toggle-wallet", n_clicks=0,
                   style={"padding": "10px 20px", "backgroundColor": "#3498db", "color": "white", 
                         "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginBottom": "20px"}),
        
        html.Div([
            html.P("📊 I dati del portafoglio vengono automaticamente salvati in 'salvataggi/wallet_data.csv' per l'analisi con 555bt.py",
                   style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginBottom": "15px"})
        ]),
        
        html.Div(id="wallet-section", style={"display": "block"})
    ], style={"padding": "20px", "backgroundColor": "#f8f9fa", "borderRadius": "10px"}),
    
    # === NUOVA SEZIONE CONSIGLI 555BT ===
    html.Hr(style={"margin": "40px 0", "border": "2px solid #9b59b6"}),
    
    html.Div([
        html.Div([
            html.H2("🤖 Consigli ML & Indicatori da 555BT", style={"color": "#2c3e50", "marginBottom": "20px", "display": "inline-block"}),
            html.Button("🔄 Carica Analisi 555BT", id="load-555bt-button", n_clicks=0,
                       style={"padding": "8px 15px", "backgroundColor": "#9b59b6", "color": "white", 
                             "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginLeft": "20px",
                             "fontSize": "14px", "fontWeight": "bold"}),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
        
        html.Div(id="555bt-load-status", style={"marginBottom": "10px"}),
        
        html.Button("👁️ Mostra/Nascondi Analisi 555BT", id="toggle-555bt", n_clicks=0,
                   style={"padding": "10px 20px", "backgroundColor": "#9b59b6", "color": "white", 
                         "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginBottom": "20px"}),
        
        html.Div([
            html.P("🤖 Questa sezione mostra i risultati dell'analisi ML di 555bt.py applicata al tuo portafoglio. Esegui prima 555bt.py per popolare i dati.",
                   style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginBottom": "15px"})
        ]),
        
        html.Div(id="555bt-analysis-section", style={"display": "block"})
    ], style={"padding": "20px", "backgroundColor": "#f4f1f8", "borderRadius": "10px"}),
    
    # === SEZIONE ACCURACY TRACKING ===
    html.Hr(style={"margin": "40px 0", "border": "2px solid #16a085"}),
    
    html.Div([
        html.Div([
            html.H2("🎯 Accuracy Tracking Raccomandazioni", style={"color": "#2c3e50", "marginBottom": "20px", "display": "inline-block"}),
            html.Button("📊 Genera Report Weekly", id="generate-accuracy-button", n_clicks=0,
                       style={"padding": "8px 15px", "backgroundColor": "#16a085", "color": "white", 
                             "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginLeft": "20px",
                             "fontSize": "14px", "fontWeight": "bold"}),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
        
        html.Div(id="accuracy-status", style={"marginBottom": "10px"}),
        
        html.Button("👁️ Mostra/Nascondi Tracking", id="toggle-accuracy", n_clicks=0,
                   style={"padding": "10px 20px", "backgroundColor": "#16a085", "color": "white", 
                         "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginBottom": "20px"}),
        
        html.Div([
            html.P("🎯 Questa sezione mostra l'accuratezza delle raccomandazioni nel tempo. I report vengono generati automaticamente dopo aver accumulato almeno 7 giorni di dati.",
                   style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginBottom": "15px"})
        ]),
        
        html.Div(id="accuracy-section", style={"display": "block"})
    ], style={"padding": "20px", "backgroundColor": "#e8f8f5", "borderRadius": "10px", "marginBottom": "30px"}),
    
    # === SEZIONE 4 ASSET PRINCIPALI ===
    html.Hr(style={"margin": "40px 0", "border": "2px solid #e67e22"}),
    
    html.Div([
        html.H2("🎯 Raccomandazioni 4 Asset Principali", style={"color": "#2c3e50", "marginBottom": "20px", "textAlign": "center"}),
        
        html.P("Riepilogo semplificato delle raccomandazioni per i 4 asset core del portafoglio",
               style={"textAlign": "center", "color": "#7f8c8d", "fontSize": "14px", "marginBottom": "30px"}),
        
        # Tabella 4 asset
        dash_table.DataTable(
            data=get_4_assets_recommendations(),
            columns=[
                {"name": "Asset", "id": "Asset"},
                {"name": "Categoria", "id": "Categoria"},
                {"name": "Rischio", "id": "Rischio"},
                {"name": "Attuale", "id": "Esposizione Attuale"},
                {"name": "Target", "id": "Ribilanciamento Ideale"},
                {"name": "Perf 1W", "id": "Performance 1W"},
                {"name": "Segnale", "id": "Segnale"},
                {"name": "Azione", "id": "Azione"},
                {"name": "Motivazione", "id": "Motivazione"}
            ],
            style_cell={
                'textAlign': 'left',
                'padding': '15px',
                'fontFamily': 'Arial',
                'fontSize': '13px',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_header={
                'backgroundColor': '#e67e22',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Segnale} = BUY'},
                    'backgroundColor': '#d5f4e6',
                    'color': '#27ae60',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Segnale} = SELL'},
                    'backgroundColor': '#fadbd8',
                    'color': '#e74c3c',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Segnale} = HOLD'},
                    'backgroundColor': '#fdeaa7',
                    'color': '#f39c12',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Rischio} = ALTO'},
                    'backgroundColor': '#ffebee'
                },
                {
                    'if': {'filter_query': '{Rischio} = MEDIO'},
                    'backgroundColor': '#fff3e0'
                },
                {
                    'if': {'filter_query': '{Rischio} = BASSO'},
                    'backgroundColor': '#e8f5e8'
                }
            ],
            sort_action="native",
            page_size=4,
            style_table={'margin': '0 auto', 'width': '95%'}
        ),
        
        # Info addizionale
        html.Div([
            html.H4("📊 Info Raccomandazioni", style={"color": "#2c3e50", "marginTop": "30px", "marginBottom": "15px"}),
            html.Ul([
                html.Li("🔴 SELL: Segnali negativi prevalenti - considera vendita"),
                html.Li("🟡 HOLD: Segnali misti o neutrali - mantieni posizione"), 
                html.Li("🟢 BUY: Segnali positivi prevalenti - considera acquisto"),
            ], style={"fontSize": "14px", "color": "#34495e"}),
            
            html.P([
                html.Strong("Nota: "),
                "Queste sono raccomandazioni simulate. Per analisi reali esegui 555bt.py per ottenere segnali ML aggiornati."
            ], style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginTop": "20px", "textAlign": "center"})
        ])
    ], style={"padding": "20px", "backgroundColor": "#fdf6e3", "borderRadius": "10px", "marginBottom": "30px"})
])

# === CALLBACK TOGGLE WALLET ===
@app.callback(
    Output("wallet-section", "style"),
    Input("toggle-wallet", "n_clicks"),
    State("wallet-section", "style")
)
def toggle_wallet(n, current_style):
    if not current_style: 
        current_style = {"display": "block"}
    return {"display": "none"} if current_style["display"] == "block" else {"display": "block"}

# === CALLBACK AGGIORNAMENTO DATI ===
@app.callback(
    Output('wallet-refresh-status', 'children'),
    Input('refresh-wallet-button', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_wallet_data(n_clicks):
    """Aggiorna i dati del portafoglio e li salva per 555bt + tracking raccomandazioni"""
    if n_clicks:
        global wallet_df
        wallet_df = load_and_save_wallet_data()
        
        # === SALVATAGGIO AUTOMATICO TRACKING RACCOMANDAZIONI ===
        try:
            # Ottieni raccomandazioni attuali
            current_recommendations = get_4_assets_recommendations()
            
            # Salva raccomandazioni storiche
            rec_count = recommendation_tracker.save_current_recommendations(
                current_recommendations, 
                wallet_df.to_dict('records') if not wallet_df.empty else [],
                {'perf_1w': perf_1w, 'perf_1m': perf_1m, 'perf_6m': perf_6m, 'perf_1y': perf_1y}
            )
            
            # Salva performance di mercato storiche
            perf_count = recommendation_tracker.save_market_performance(perf_1w)
            
            return html.Div([
                html.Span("✅ Dati aggiornati!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"📊 Salvate {rec_count} raccomandazioni + {perf_count} performance per tracking", 
                         style={'fontSize': '11px', 'color': '#7f8c8d'}),
                html.Span(f" - {datetime.datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
        except Exception as e:
            print(f"⚠️ Errore tracking: {e}")
            return html.Div([
                html.Span("✅ Dati aggiornati!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"⚠️ Tracking parziale - {str(e)[:50]}", style={'fontSize': '11px', 'color': '#e67e22'}),
                html.Span(f" - {datetime.datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
    return html.Div()

# === CALLBACK WALLET CONTENT ===
@app.callback(
    Output('wallet-section', 'children'),
    Input('toggle-wallet', 'n_clicks')
)
def update_wallet_content(n):
    if wallet_df.empty:
        return html.Div([
            html.Div("⚠️ Nessun dato nel portafoglio.", 
                    style={"textAlign": "center", "color": "#e74c3c", "fontSize": "18px", "padding": "20px"})
        ])
    
    total_value = wallet_df['Totale'].sum()
    
    # Grafico a torta per composizione portafoglio
    pie_fig = px.pie(wallet_df, names="Asset", values="Totale", 
                     title="🥧 Composizione Portafoglio per Asset")
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Grafico a barre per valore per categoria
    bar_fig = px.bar(wallet_df, x="Asset", y="Totale", color="Categoria", 
                     text_auto=True, title="📊 Valore per Asset e Categoria")
    bar_fig.update_layout(xaxis_tickangle=-45)
    
    # Formattazione valore totale (formato europeo)
    label = f"💰 Valore totale: € {total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Tabella dettagliata portafoglio
    table_data = wallet_df.to_dict('records')
    
    return html.Div([
        # Valore totale
        html.Div([
            html.H3(label, style={"color": "#27ae60", "textAlign": "center", "marginBottom": "20px"})
        ]),
        
        # Grafici side by side
        html.Div([
            html.Div([
                dcc.Graph(figure=pie_fig)
            ], style={"width": "48%", "display": "inline-block"}),
            
            html.Div([
                dcc.Graph(figure=bar_fig)
            ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%"})
        ]),
        
        # Tabella dettagliata
        html.H4("📋 Dettaglio Portafoglio", style={"color": "#2c3e50", "marginTop": "30px"}),
        dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Categoria", "id": "Categoria"},
                {"name": "Asset", "id": "Asset"},
                {"name": "Ticker", "id": "Ticker"},
                {"name": "Prezzo (€)", "id": "Prezzo", "type": "numeric", "format": {"specifier": ",.2f"}},
                {"name": "Quantità", "id": "Quantità", "type": "numeric", "format": {"specifier": ",.4f"}},
                {"name": "Totale (€)", "id": "Totale", "type": "numeric", "format": {"specifier": ",.2f"}}
            ],
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontFamily': 'Arial',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_header={
                'backgroundColor': '#3498db',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data_conditional=[
                {
                    'if': {'column_id': 'Totale'},
                    'backgroundColor': '#e8f5e8',
                    'fontWeight': 'bold'
                }
            ],
            sort_action="native",
            filter_action="native",
            page_size=10
        )
    ])

# === CALLBACK TOGGLE 555BT SECTION ===
@app.callback(
    Output("555bt-analysis-section", "style"),
    Input("toggle-555bt", "n_clicks"),
    State("555bt-analysis-section", "style")
)
def toggle_555bt_section(n, current_style):
    if not current_style: 
        current_style = {"display": "block"}
    return {"display": "none"} if current_style["display"] == "block" else {"display": "block"}

# === CALLBACK CARICAMENTO 555BT ===
@app.callback(
    Output('555bt-load-status', 'children'),
    Input('load-555bt-button', 'n_clicks'),
    prevent_initial_call=True
)
def load_555bt_analysis_callback(n_clicks):
    """Carica i risultati dall'analisi 555bt"""
    if n_clicks:
        analysis = load_555bt_analysis()
        
        if analysis['available']:
            ml_count = len(analysis['ml_predictions'])
            tech_count = len(analysis['technical_signals'])
            rec_count = len(analysis['portfolio_recommendations'])
            
            return html.Div([
                html.Span("✅ Analisi 555BT caricata!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"📊 ML: {ml_count} | 📈 Tecnici: {tech_count} | 🎯 Raccomandazioni: {rec_count}", 
                         style={'fontSize': '12px', 'color': '#7f8c8d'}),
                html.Span(f" - {datetime.datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
        else:
            return html.Div([
                html.Span("⚠️ Nessun dato 555BT trovato", style={'color': '#e67e22', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span("Esegui prima 555bt.py per generare le analisi", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
    return html.Div()

# === CALLBACK CONTENUTO 555BT ===
@app.callback(
    Output('555bt-analysis-section', 'children'),
    Input('load-555bt-button', 'n_clicks'),
    Input('toggle-555bt', 'n_clicks')
)
def update_555bt_content(load_clicks, toggle_clicks):
    """Aggiorna il contenuto della sezione 555BT"""
    analysis = load_555bt_analysis()
    
    if not analysis['available']:
        return html.Div([
            html.Div([
                html.H4("🚫 Nessuna Analisi Disponibile", style={"color": "#e74c3c", "textAlign": "center"}),
                html.P("Per visualizzare i consigli ML e gli indicatori:", style={"textAlign": "center", "margin": "20px 0"}),
                html.Ol([
                    html.Li("1. Assicurati che i dati del portafoglio siano aggiornati (pulsante 'Aggiorna Dati' sopra)"),
                    html.Li("2. Esegui 555bt.py nella directory principale"),
                    html.Li("3. Torna qui e clicca 'Carica Analisi 555BT'"),
                ], style={"textAlign": "left", "margin": "20px auto", "maxWidth": "500px"}),
                html.P("📁 I file cercati:", style={"fontWeight": "bold", "marginTop": "30px"}),
                html.Ul([
                    html.Li("salvataggi/previsioni_ml.csv"),
                    html.Li("salvataggi/segnali_tecnici.csv"),
                    html.Li("salvataggi/portfolio_analysis.txt")
                ], style={"textAlign": "left", "margin": "10px auto", "maxWidth": "300px"})
            ], style={"padding": "40px", "backgroundColor": "#fdf2f2", "borderRadius": "10px", "margin": "20px"})
        ])
    
    # Contenuto quando i dati sono disponibili
    content_sections = []
    
    # === SEZIONE PREVISIONI ML ===
    if analysis['ml_predictions']:
        ml_data = analysis['ml_predictions']
        
        content_sections.append(
            html.Div([
                html.H4("🤖 Previsioni Machine Learning", style={"color": "#2c3e50", "marginBottom": "15px"}),
                dash_table.DataTable(
                    data=ml_data,
                    columns=[
                        {"name": "Modello", "id": "Modello"},
                        {"name": "Asset", "id": "Asset"},
                        {"name": "🎯 Segnale", "id": "Segnale"},
                        {"name": "📊 Probabilità", "id": "Prob_Formatted"},
                        {"name": "🎯 Accuratezza", "id": "Accuratezza"},
                        {"name": "💡 Raccomandazione", "id": "Raccomandazione"}
                    ],
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'fontFamily': 'Arial',
                        'fontSize': '12px'
                    },
                    style_header={
                        'backgroundColor': '#9b59b6',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Segnale} = BUY'},
                            'backgroundColor': '#d5f4e6',
                            'color': '#27ae60'
                        },
                        {
                            'if': {'filter_query': '{Segnale} = SELL'},
                            'backgroundColor': '#fadbd8',
                            'color': '#e74c3c'
                        },
                        {
                            'if': {'filter_query': '{Segnale} = HOLD'},
                            'backgroundColor': '#fdeaa7',
                            'color': '#f39c12'
                        }
                    ],
                    page_size=10
                )
            ], style={"marginBottom": "30px"})
        )
    
    # === SEZIONE SEGNALI TECNICI ===
    if analysis['technical_signals']:
        tech_data = analysis['technical_signals']
        
        content_sections.append(
            html.Div([
                html.H4("📈 Indicatori Tecnici", style={"color": "#2c3e50", "marginBottom": "15px"}),
                dash_table.DataTable(
                    data=tech_data,
                    columns=[
                        {"name": col, "id": col} for col in tech_data[0].keys()
                    ],
                    style_cell={
                        'textAlign': 'left',
                        'padding': '8px',
                        'fontFamily': 'Arial',
                        'fontSize': '11px'
                    },
                    style_header={
                        'backgroundColor': '#3498db',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    page_size=8
                )
            ], style={"marginBottom": "30px"})
        )
    
    # === SEZIONE RACCOMANDAZIONI PORTAFOGLIO ===
    if analysis['portfolio_recommendations']:
        rec_data = analysis['portfolio_recommendations']
        
        # Ordinare per priorità
        high_priority = [r for r in rec_data if r.get('priority') == 'ALTA']
        medium_priority = [r for r in rec_data if r.get('priority') == 'MEDIA']
        low_priority = [r for r in rec_data if r.get('priority') == 'BASSA']
        
        rec_cards = []
        
        # Sezione ALTA priorità
        if high_priority:
            rec_cards.append(
                html.H5("🔴 PRIORITÀ ALTA", style={"color": "#e74c3c", "marginTop": "20px", "marginBottom": "15px"})
            )
            for rec in high_priority:
                priority_color = "#e74c3c"
                bg_color = "#fdf2f2"
                
                rec_cards.append(
                    html.Div([
                        html.Div([
                            html.H5(f"🎯 {rec.get('asset', 'N/A')}", 
                                   style={"color": "#2c3e50", "marginBottom": "5px", "display": "inline-block"}),
                            html.Span(f"🔥 {rec.get('priority', 'N/A')}", 
                                    style={"backgroundColor": priority_color, "color": "white", "padding": "2px 8px", 
                                           "borderRadius": "12px", "fontSize": "10px", "marginLeft": "10px"})
                        ], style={"marginBottom": "10px"}),
                        
                        html.P([
                            html.Strong("Azione: "),
                            html.Span(rec.get('action', 'N/A'), style={"color": priority_color, "fontWeight": "bold"})
                        ], style={"marginBottom": "8px"}),
                        
                        html.P([
                            html.Strong("📋 Motivo: "),
                            rec.get('reason', 'N/A')
                        ], style={"fontSize": "12px", "marginBottom": "8px"}),
                        
                        html.P([
                            html.Strong("💡 Consiglio: "),
                            rec.get('suggestion', 'N/A')
                        ], style={"fontSize": "12px", "color": "#7f8c8d"}),
                        
                        # Info aggiuntive
                        html.Div([
                            html.Span(f"ML: {rec.get('ml_signal', 'N/A')}", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px", "marginRight": "5px"}),
                            html.Span(f"Tecnici: {rec.get('tech_buy', 0)} BUY / {rec.get('tech_sell', 0)} SELL", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px", "marginRight": "5px"}),
                            html.Span(f"Rischio: {rec.get('risk_level', 'N/A')}", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px"})
                        ], style={"marginTop": "10px"})
                    ], style={
                        "border": f"2px solid {priority_color}", 
                        "borderRadius": "12px", 
                        "padding": "15px", 
                        "margin": "10px 0",
                        "backgroundColor": bg_color,
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                    })
                )
        
        # Sezione MEDIA priorità
        if medium_priority:
            rec_cards.append(
                html.H5("🟡 PRIORITÀ MEDIA", style={"color": "#f39c12", "marginTop": "20px", "marginBottom": "15px"})
            )
            for rec in medium_priority:
                priority_color = "#f39c12"
                bg_color = "#fef9e7"
                
                rec_cards.append(
                    html.Div([
                        html.Div([
                            html.H5(f"🎯 {rec.get('asset', 'N/A')}", 
                                   style={"color": "#2c3e50", "marginBottom": "5px", "display": "inline-block"}),
                            html.Span(f"🟡 {rec.get('priority', 'N/A')}", 
                                    style={"backgroundColor": priority_color, "color": "white", "padding": "2px 8px", 
                                           "borderRadius": "12px", "fontSize": "10px", "marginLeft": "10px"})
                        ], style={"marginBottom": "10px"}),
                        
                        html.P([
                            html.Strong("Azione: "),
                            html.Span(rec.get('action', 'N/A'), style={"color": priority_color, "fontWeight": "bold"})
                        ], style={"marginBottom": "8px"}),
                        
                        html.P([
                            html.Strong("📋 Motivo: "),
                            rec.get('reason', 'N/A')
                        ], style={"fontSize": "12px", "marginBottom": "8px"}),
                        
                        html.P([
                            html.Strong("💡 Consiglio: "),
                            rec.get('suggestion', 'N/A')
                        ], style={"fontSize": "12px", "color": "#7f8c8d"}),
                        
                        html.Div([
                            html.Span(f"ML: {rec.get('ml_signal', 'N/A')}", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px", "marginRight": "5px"}),
                            html.Span(f"Tecnici: {rec.get('tech_buy', 0)} BUY / {rec.get('tech_sell', 0)} SELL", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px", "marginRight": "5px"}),
                            html.Span(f"Rischio: {rec.get('risk_level', 'N/A')}", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px"})
                        ], style={"marginTop": "10px"})
                    ], style={
                        "border": f"1px solid {priority_color}", 
                        "borderRadius": "8px", 
                        "padding": "15px", 
                        "margin": "10px 0",
                        "backgroundColor": bg_color
                    })
                )
        
        # Sezione BASSA priorità
        if low_priority:
            rec_cards.append(
                html.H5("🟢 PRIORITÀ BASSA", style={"color": "#27ae60", "marginTop": "20px", "marginBottom": "15px"})
            )
            for rec in low_priority:
                priority_color = "#27ae60"
                bg_color = "#eafaf1"
                
                rec_cards.append(
                    html.Div([
                        html.Div([
                            html.H5(f"🎯 {rec.get('asset', 'N/A')}", 
                                   style={"color": "#2c3e50", "marginBottom": "5px", "display": "inline-block"}),
                            html.Span(f"🟢 {rec.get('priority', 'N/A')}", 
                                    style={"backgroundColor": priority_color, "color": "white", "padding": "2px 8px", 
                                           "borderRadius": "12px", "fontSize": "10px", "marginLeft": "10px"})
                        ], style={"marginBottom": "10px"}),
                        
                        html.P([
                            html.Strong("Azione: "),
                            html.Span(rec.get('action', 'N/A'), style={"color": priority_color, "fontWeight": "bold"})
                        ], style={"marginBottom": "8px"}),
                        
                        html.P([
                            html.Strong("📋 Motivo: "),
                            rec.get('reason', 'N/A')
                        ], style={"fontSize": "12px", "marginBottom": "8px"}),
                        
                        html.P([
                            html.Strong("💡 Consiglio: "),
                            rec.get('suggestion', 'N/A')
                        ], style={"fontSize": "12px", "color": "#7f8c8d"}),
                        
                        html.Div([
                            html.Span(f"ML: {rec.get('ml_signal', 'N/A')}", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px", "marginRight": "5px"}),
                            html.Span(f"Tecnici: {rec.get('tech_buy', 0)} BUY / {rec.get('tech_sell', 0)} SELL", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px", "marginRight": "5px"}),
                            html.Span(f"Rischio: {rec.get('risk_level', 'N/A')}", 
                                    style={"backgroundColor": "#ecf0f1", "padding": "2px 6px", "borderRadius": "8px", "fontSize": "10px"})
                        ], style={"marginTop": "10px"})
                    ], style={
                        "border": f"1px solid {priority_color}", 
                        "borderRadius": "8px", 
                        "padding": "15px", 
                        "margin": "10px 0",
                        "backgroundColor": bg_color
                    })
                )
        
        content_sections.append(
            html.Div([
                html.H4("💡 Raccomandazioni Portafoglio", style={"color": "#2c3e50", "marginBottom": "15px"}),
                html.Div(rec_cards)
            ], style={"marginBottom": "30px"})
        )
    
    # === TIMESTAMP E INFO ===
    if analysis['last_update']:
        content_sections.append(
            html.Div([
                html.P(f"📅 Ultimo aggiornamento: {analysis['last_update']}", 
                       style={"fontSize": "12px", "color": "#7f8c8d", "textAlign": "center", "marginTop": "30px"})
            ])
        )
    
    return html.Div(content_sections)

# === CALLBACK TOGGLE ACCURACY SECTION ===
@app.callback(
    Output("accuracy-section", "style"),
    Input("toggle-accuracy", "n_clicks"),
    State("accuracy-section", "style")
)
def toggle_accuracy_section(n, current_style):
    if not current_style: 
        current_style = {"display": "block"}
    return {"display": "none"} if current_style["display"] == "block" else {"display": "block"}

# === CALLBACK GENERA ACCURACY REPORT ===
@app.callback(
    Output('accuracy-status', 'children'),
    Input('generate-accuracy-button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_accuracy_report(n_clicks):
    """Genera un report di accuracy settimanale"""
    if n_clicks:
        try:
            # Genera report settimanale
            report = recommendation_tracker.calculate_accuracy_report(7)
            
            if report is None:
                return html.Div([
                    html.Span("⚠️ Nessun dato sufficiente", style={'color': '#e67e22', 'fontWeight': 'bold'}),
                    html.Br(),
                    html.Span("Serve almeno 1 settimana di dati storici per generare il report", style={'fontSize': '12px', 'color': '#7f8c8d'})
                ])
            
            # Calcola rating
            accuracy_pct = report['accuracy_percentuale']
            if accuracy_pct >= 70:
                rating_icon = "🎆"
                rating_color = "#27ae60"
                rating_text = "ECCELLENTE"
            elif accuracy_pct >= 60:
                rating_icon = "🚀"
                rating_color = "#f39c12"
                rating_text = "BUONA"
            elif accuracy_pct >= 50:
                rating_icon = "🔥"
                rating_color = "#e67e22"
                rating_text = "MEDIA"
            else:
                rating_icon = "⚡"
                rating_color = "#e74c3c"
                rating_text = "DA MIGLIORARE"
            
            return html.Div([
                html.Span("✅ Report accuracy generato!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"{rating_icon} {rating_text}: {accuracy_pct:.1f}% ({report['raccomandazioni_corrette']}/{report['totale_raccomandazioni']})", 
                         style={'fontSize': '12px', 'color': rating_color, 'fontWeight': 'bold'}),
                html.Span(f" - {datetime.datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
        except Exception as e:
            return html.Div([
                html.Span("❌ Errore generazione report", style={'color': '#e74c3c', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"Dettagli: {str(e)[:60]}", style={'fontSize': '11px', 'color': '#7f8c8d'})
            ])
    return html.Div()

# === CALLBACK CONTENUTO ACCURACY ===
@app.callback(
    Output('accuracy-section', 'children'),
    Input('generate-accuracy-button', 'n_clicks'),
    Input('toggle-accuracy', 'n_clicks')
)
def update_accuracy_content(generate_clicks, toggle_clicks):
    """Aggiorna il contenuto della sezione accuracy tracking"""
    
    # Ottieni summary più recente
    summary = recommendation_tracker.get_latest_accuracy_summary()
    
    if summary is None:
        return html.Div([
            html.Div([
                html.H4("🚀 Inizia il Tracking!", style={"color": "#2c3e50", "textAlign": "center"}),
                html.P("Il sistema di accuracy tracking ti permette di misurare l'efficacia delle raccomandazioni nel tempo.", 
                       style={"textAlign": "center", "margin": "20px 0"}),
                html.P("📋 Come funziona:", style={"fontWeight": "bold", "marginTop": "30px"}),
                html.Ol([
                    html.Li("Ogni volta che aggiorni i dati, vengono salvate le raccomandazioni attuali"),
                    html.Li("Dopo 7 giorni, il sistema confronta le previsioni con le performance reali"),
                    html.Li("Viene calcolata l'accuratezza: BUY corretti se asset sale, SELL corretti se scende, ecc."),
                    html.Li("I report mostrano la percentuale di successo delle raccomandazioni")
                ], style={"textAlign": "left", "margin": "10px 0", "lineHeight": "1.6"}),
                
                html.Div([
                    html.P("📊 Per iniziare:", style={"fontWeight": "bold", "marginTop": "30px", "marginBottom": "10px"}),
                    html.P("1. Clicca 'Aggiorna Dati' nella sezione Wallet per salvare le raccomandazioni attuali", 
                           style={"fontSize": "14px", "margin": "5px 0"}),
                    html.P("2. Ripeti l'operazione regolarmente per accumulare dati storici", 
                           style={"fontSize": "14px", "margin": "5px 0"}),
                    html.P("3. Dopo 7+ giorni, clicca 'Genera Report Weekly' per vedere l'accuracy", 
                           style={"fontSize": "14px", "margin": "5px 0"})
                ], style={"backgroundColor": "#f0f8ff", "padding": "15px", "borderRadius": "8px", "border": "1px solid #16a085"})
            ], style={"padding": "30px", "backgroundColor": "#fafafa", "borderRadius": "10px", "margin": "20px"})
        ])
    
    # Mostra l'ultimo report disponibile
    accuracy_pct = summary['accuracy_pct']
    
    # Determina rating e colore
    if accuracy_pct >= 70:
        rating_icon = "🎆"
        rating_color = "#27ae60"
        rating_text = "ECCELLENTE"
        rating_bg = "#eafaf1"
        performance_comment = "Le raccomandazioni sono molto affidabili! 🚀"
    elif accuracy_pct >= 60:
        rating_icon = "🚀"
        rating_color = "#f39c12"
        rating_text = "BUONA"
        rating_bg = "#fef9e7"
        performance_comment = "Buone performance, con margine di miglioramento. 💪"
    elif accuracy_pct >= 50:
        rating_icon = "🔥"
        rating_color = "#e67e22"
        rating_text = "MEDIA"
        rating_bg = "#fdf2e9"
        performance_comment = "Performance nella media, consider aggiustamenti. 🎯"
    else:
        rating_icon = "⚡"
        rating_color = "#e74c3c"
        rating_text = "DA MIGLIORARE"
        rating_bg = "#fdf2f2"
        performance_comment = "Il sistema ha bisogno di calibrazione. 🔧"
    
    return html.Div([
        # Card accuracy principale
        html.Div([
            html.H4(f"{rating_icon} Accuracy Report - {rating_text}", 
                   style={"color": rating_color, "textAlign": "center", "marginBottom": "20px"}),
            
            # Statistiche principali
            html.Div([
                html.Div([
                    html.H2(f"{accuracy_pct:.1f}%", style={"color": rating_color, "margin": "0", "fontSize": "48px", "fontWeight": "bold"}),
                    html.P("Accuracy", style={"color": "#7f8c8d", "margin": "0", "fontSize": "14px"})
                ], style={"textAlign": "center", "width": "30%", "display": "inline-block", "verticalAlign": "top"}),
                
                html.Div([
                    html.H3(f"{summary['corrette']}", style={"color": "#27ae60", "margin": "0", "fontSize": "36px"}),
                    html.P("Corrette", style={"color": "#7f8c8d", "margin": "0", "fontSize": "14px"})
                ], style={"textAlign": "center", "width": "30%", "display": "inline-block", "verticalAlign": "top", "marginLeft": "5%"}),
                
                html.Div([
                    html.H3(f"{summary['totale_raccomandazioni']}", style={"color": "#3498db", "margin": "0", "fontSize": "36px"}),
                    html.P("Totale", style={"color": "#7f8c8d", "margin": "0", "fontSize": "14px"})
                ], style={"textAlign": "center", "width": "30%", "display": "inline-block", "verticalAlign": "top", "marginLeft": "5%"})
            ], style={"marginBottom": "25px"}),
            
            # Commento performance
            html.P(performance_comment, 
                   style={"textAlign": "center", "fontSize": "16px", "color": "#2c3e50", "marginBottom": "20px"}),
            
            # Dettagli tecnici
            html.Div([
                html.P(f"📅 Periodo analizzato: {summary['giorni_analizzati']} giorni (dal {summary['date']})", 
                       style={"fontSize": "12px", "color": "#7f8c8d", "margin": "5px 0"}),
                html.P(f"📊 Reports generati: {summary['total_reports']}", 
                       style={"fontSize": "12px", "color": "#7f8c8d", "margin": "5px 0"})
            ], style={"textAlign": "center"})
            
        ], style={
            "backgroundColor": rating_bg,
            "padding": "30px",
            "borderRadius": "15px",
            "border": f"2px solid {rating_color}",
            "margin": "20px 0",
            "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
        }),
        
        # Info metodologia
        html.Div([
            html.H5("🎯 Metodologia di Valutazione", style={"color": "#2c3e50", "marginBottom": "15px"}),
            html.Ul([
                html.Li("🟢 BUY corretto: Asset ha performance positiva dopo 1 settimana"),
                html.Li("🔴 SELL corretto: Asset ha performance negativa dopo 1 settimana"),
                html.Li("🟡 HOLD corretto: Asset ha performance stabile (±2%) dopo 1 settimana")
            ], style={"fontSize": "13px", "lineHeight": "1.6"}),
            
            html.P([
                html.Strong("Nota: "),
                "Il sistema migliora con più dati. Raccomandazioni più frequenti = accuracy più affidabile."
            ], style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginTop": "15px"})
        ], style={
            "backgroundColor": "#f8f9fa",
            "padding": "20px",
            "borderRadius": "10px",
            "border": "1px solid #dee2e6",
            "marginTop": "20px"
        })
    ])

if __name__ == "__main__":
    print("💼 Avvio Wallet Dashboard...")
    print("🌍 Accesso: http://localhost:8051")
    app.run(debug=True, port=8051)
