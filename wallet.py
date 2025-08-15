import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import datetime
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
import requests
import os

app = dash.Dash(__name__)
server = app.server
app.title = "💼 Wallet Dashboard"

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
            print(f"📊 Caricando {name}...")
            df = web.DataReader(code, 'fred', start, end).dropna()
            df.columns = ['Value']
            data[name] = df
            print(f"✅ {name} caricato")
        except Exception as e:
            print(f"❌ Errore caricando {name}: {e}")
            continue
    return data

def get_btc_data():
    try:
        print("📊 Caricando Bitcoin...")
        url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=1800"
        r = requests.get(url, timeout=10)  # Timeout di 10 secondi
        if r.status_code == 200:
            js = r.json()
            if 'Data' in js and 'Data' in js['Data']:
                prices = js["Data"]["Data"]
                df = pd.DataFrame(prices)
                if not df.empty:
                    df['Date'] = pd.to_datetime(df['time'], unit='s')
                    df.set_index('Date', inplace=True)
                    df = df[['close']].rename(columns={'close': 'Value'})
                    print("✅ Bitcoin caricato")
                    return df.dropna()
        print("❌ Errore caricando Bitcoin: risposta non valida")
        return pd.DataFrame()
    except requests.exceptions.Timeout:
        print("❌ Errore caricando Bitcoin: timeout connessione")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Errore caricando Bitcoin: {e}")
        return pd.DataFrame()

data = get_fred_data()
btc_df = get_btc_data()
if not btc_df.empty:
    data["Bitcoin"] = btc_df

df_all = pd.concat([df["Value"] for df in data.values()], axis=1)
df_all.columns = list(data.keys())
df_all.dropna(inplace=True)
df_norm = df_all / df_all.iloc[0] * 100 if not df_all.empty else pd.DataFrame()

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

perf_1w = get_performance(df_all, 7)
perf_1m = get_performance(df_all, 30)
perf_6m = get_performance(df_all, 180)
perf_1y = get_performance(df_all, 365)

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

# === FUNZIONI PER ANALISI PERFORMANCE SETTIMANALI ===
def load_weekly_performance_analysis():
    """Carica e analizza le performance settimanali dalle raccomandazioni storiche"""
    wallet_dir = 'salvataggiwallet'
    recommendations_file = os.path.join(wallet_dir, 'raccomandazioni_storiche.csv')
    performance_file = os.path.join(wallet_dir, 'performance_storiche.csv')
    
    analysis = {
        'available': False,
        'total_recommendations': 0,
        'accuracy_by_asset': {},
        'recent_performance': {},
        'trend_analysis': {},
        'summary_stats': {}
    }
    
    try:
        if not os.path.exists(recommendations_file) or not os.path.exists(performance_file):
            return analysis
        
        # Carica i dati
        recs_df = pd.read_csv(recommendations_file)
        perf_df = pd.read_csv(performance_file)
        
        if recs_df.empty or perf_df.empty:
            return analysis
        
        # Converti timestamp
        recs_df['timestamp'] = pd.to_datetime(recs_df['timestamp'])
        perf_df['timestamp'] = pd.to_datetime(perf_df['timestamp'])
        
        # Filtra ultimi 7 giorni
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)
        recent_recs = recs_df[recs_df['timestamp'] >= cutoff_date]
        recent_perf = perf_df[perf_df['timestamp'] >= cutoff_date]
        
        analysis['available'] = True
        analysis['total_recommendations'] = len(recent_recs)
        
        # Analisi per asset
        for asset in recent_recs['asset'].unique():
            asset_recs = recent_recs[recent_recs['asset'] == asset]
            asset_perf = recent_perf[recent_perf['asset'] == asset]
            
            if not asset_perf.empty:
                # Calcola accuracy semplificata
                buy_recs = len(asset_recs[asset_recs['segnale'] == 'BUY'])
                sell_recs = len(asset_recs[asset_recs['segnale'] == 'SELL'])
                
                # Performance media 1w
                avg_performance = asset_recs['performance_1w'].mean() if 'performance_1w' in asset_recs.columns else 0.0
                
                # Ultima raccomandazione
                last_rec = asset_recs.iloc[-1] if not asset_recs.empty else None
                
                analysis['accuracy_by_asset'][asset] = {
                    'buy_signals': buy_recs,
                    'sell_signals': sell_recs,
                    'total_signals': len(asset_recs),
                    'avg_performance_1w': round(avg_performance, 2),
                    'last_recommendation': last_rec['segnale'] if last_rec is not None else 'N/A',
                    'last_action': last_rec['azione'] if last_rec is not None else 'N/A',
                    'consistency_score': calculate_consistency_score(asset_recs)
                }
        
        # Summary stats
        analysis['summary_stats'] = {
            'total_days_analyzed': 7,
            'unique_assets': len(recent_recs['asset'].unique()),
            'avg_daily_recommendations': round(len(recent_recs) / 7, 1),
            'most_recommended_action': recent_recs['segnale'].mode().iloc[0] if not recent_recs.empty else 'N/A',
            'high_risk_recommendations': len(recent_recs[recent_recs['rischio'] == 'ALTISSIMO']),
            'last_update': recent_recs['timestamp'].max().strftime('%d/%m/%Y %H:%M') if not recent_recs.empty else 'N/A'
        }
        
        print(f"✅ [WALLET] Analisi performance settimanale caricata: {analysis['total_recommendations']} raccomandazioni")
        
    except Exception as e:
        print(f"❌ [WALLET] Errore caricamento performance settimanale: {e}")
        
    return analysis

def calculate_consistency_score(asset_recommendations):
    """Calcola un punteggio di consistenza per le raccomandazioni"""
    if len(asset_recommendations) < 2:
        return 0.5
    
    # Conta cambi di direzione BUY/SELL
    signals = asset_recommendations['segnale'].tolist()
    changes = sum(1 for i in range(1, len(signals)) if signals[i] != signals[i-1])
    
    # Più cambi = meno consistenza
    consistency = 1.0 - (changes / len(signals))
    return round(max(0.0, consistency), 2)

def load_weekly_summary_analysis():
    """Carica e genera il riepilogo dei consigli settimanali"""
    wallet_dir = 'salvataggiwallet'
    recommendations_file = os.path.join(wallet_dir, 'raccomandazioni_storiche.csv')
    
    summary = {
        'available': False,
        'trend_patterns': {},
        'asset_focus': {},
        'risk_distribution': {},
        'weekly_insights': [],
        'action_frequency': {}
    }
    
    try:
        if not os.path.exists(recommendations_file):
            return summary
            
        recs_df = pd.read_csv(recommendations_file)
        if recs_df.empty:
            return summary
            
        # Converti timestamp
        recs_df['timestamp'] = pd.to_datetime(recs_df['timestamp'])
        
        # Filtra ultimi 7 giorni
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)
        recent_recs = recs_df[recs_df['timestamp'] >= cutoff_date]
        
        if recent_recs.empty:
            return summary
            
        summary['available'] = True
        
        # Analisi frequenza azioni
        action_counts = recent_recs['segnale'].value_counts()
        summary['action_frequency'] = {
            'BUY': int(action_counts.get('BUY', 0)),
            'SELL': int(action_counts.get('SELL', 0)),
            'HOLD': int(action_counts.get('HOLD', 0))
        }
        
        # Distribuzione rischi
        risk_counts = recent_recs['rischio'].value_counts()
        summary['risk_distribution'] = dict(risk_counts.head())
        
        # Focus per asset (più raccomandazioni = più focus)
        asset_counts = recent_recs['asset'].value_counts()
        summary['asset_focus'] = dict(asset_counts.head(4))
        
        # Pattern temporali (raggruppamento per giorni)
        recent_recs['day'] = recent_recs['timestamp'].dt.strftime('%A')
        daily_counts = recent_recs['day'].value_counts()
        
        # Insights automatici
        insights = []
        
        # Insight 1: Asset più raccomandato
        if not asset_counts.empty:
            top_asset = asset_counts.index[0]
            top_count = asset_counts.iloc[0]
            insights.append(f"🎯 Focus principale: {top_asset} ({top_count} raccomandazioni)")
        
        # Insight 2: Bias direzionale
        total_actions = sum(summary['action_frequency'].values())
        if total_actions > 0:
            buy_pct = (summary['action_frequency']['BUY'] / total_actions) * 100
            sell_pct = (summary['action_frequency']['SELL'] / total_actions) * 100
            
            if buy_pct > 60:
                insights.append(f"📈 Bias rialzista: {buy_pct:.0f}% raccomandazioni BUY")
            elif sell_pct > 60:
                insights.append(f"📉 Bias ribassista: {sell_pct:.0f}% raccomandazioni SELL")
            else:
                insights.append("⚖️ Approccio bilanciato tra BUY e SELL")
        
        # Insight 3: Gestione del rischio
        high_risk_count = len(recent_recs[recent_recs['rischio'].isin(['ALTISSIMO', 'ALTO'])])
        if high_risk_count > len(recent_recs) * 0.7:
            insights.append(f"⚠️ Alert: {high_risk_count} raccomandazioni ad alto rischio")
        else:
            insights.append(f"✅ Gestione rischio: {high_risk_count} raccomandazioni alto rischio")
        
        # Insight 4: Consistenza temporale
        unique_dates = recent_recs['timestamp'].dt.date.nunique()
        avg_daily = len(recent_recs) / max(1, unique_dates)
        insights.append(f"📊 Media: {avg_daily:.1f} raccomandazioni/giorno su {unique_dates} giorni")
        
        summary['weekly_insights'] = insights
        
        print(f"✅ [WALLET] Riepilogo settimanale generato: {len(insights)} insights")
        
    except Exception as e:
        print(f"❌ [WALLET] Errore generazione riepilogo settimanale: {e}")
        
    return summary

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
    
    # === SEZIONE PERFORMANCE RACCOMANDAZIONI SETTIMANALI ===
    html.Hr(style={"margin": "40px 0", "border": "2px solid #e67e22"}),
    
    html.Div([
        html.Div([
            html.H2("📊 Performance Raccomandazioni Settimanali", style={"color": "#2c3e50", "marginBottom": "20px", "display": "inline-block"}),
            html.Button("🔄 Aggiorna Analisi", id="refresh-weekly-performance", n_clicks=0,
                       style={"padding": "8px 15px", "backgroundColor": "#e67e22", "color": "white", 
                             "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginLeft": "20px",
                             "fontSize": "14px", "fontWeight": "bold"}),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
        
        html.Div(id="weekly-performance-status", style={"marginBottom": "10px"}),
        
        html.Button("👁️ Mostra/Nascondi Performance Settimanali", id="toggle-weekly-performance", n_clicks=0,
                   style={"padding": "10px 20px", "backgroundColor": "#e67e22", "color": "white", 
                         "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginBottom": "20px"}),
        
        html.Div([
            html.P("📈 Questa sezione mostra l'accuracy e le performance delle raccomandazioni degli ultimi 7 giorni basate sui dati salvati.",
                   style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginBottom": "15px"})
        ]),
        
        html.Div(id="weekly-performance-section", style={"display": "block"})
    ], style={"padding": "20px", "backgroundColor": "#fef5e7", "borderRadius": "10px"}),

    # === SEZIONE RIEPILOGO CONSIGLI SETTIMANALI ===
    html.Hr(style={"margin": "40px 0", "border": "2px solid #27ae60"}),
    
    html.Div([
        html.Div([
            html.H2("📈 Riepilogo Consigli Settimanali", style={"color": "#2c3e50", "marginBottom": "20px", "display": "inline-block"}),
            html.Button("🔄 Aggiorna Riepilogo", id="refresh-weekly-summary", n_clicks=0,
                       style={"padding": "8px 15px", "backgroundColor": "#27ae60", "color": "white", 
                             "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginLeft": "20px",
                             "fontSize": "14px", "fontWeight": "bold"}),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
        
        html.Div(id="weekly-summary-status", style={"marginBottom": "10px"}),
        
        html.Button("👁️ Mostra/Nascondi Riepilogo Settimanale", id="toggle-weekly-summary", n_clicks=0,
                   style={"padding": "10px 20px", "backgroundColor": "#27ae60", "color": "white", 
                         "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginBottom": "20px"}),
        
        html.Div([
            html.P("📋 Questa sezione fornisce un riassunto dei pattern di raccomandazione e trend settimanali del portafoglio.",
                   style={"fontSize": "12px", "color": "#7f8c8d", "fontStyle": "italic", "marginBottom": "15px"})
        ]),
        
        html.Div(id="weekly-summary-section", style={"display": "block"})
    ], style={"padding": "20px", "backgroundColor": "#eafaf1", "borderRadius": "10px"}),
    
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
    ], style={"padding": "20px", "backgroundColor": "#f4f1f8", "borderRadius": "10px"})
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
    """Aggiorna i dati del portafoglio e li salva per 555bt"""
    if n_clicks:
        global wallet_df
        wallet_df = load_and_save_wallet_data()
        return html.Div([
            html.Span("✅ Dati aggiornati!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
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

# === CALLBACK TOGGLE WEEKLY PERFORMANCE SECTION ===
@app.callback(
    Output("weekly-performance-section", "style"),
    Input("toggle-weekly-performance", "n_clicks"),
    State("weekly-performance-section", "style")
)
def toggle_weekly_performance_section(n, current_style):
    if not current_style: 
        current_style = {"display": "block"}
    return {"display": "none"} if current_style["display"] == "block" else {"display": "block"}

# === CALLBACK AGGIORNAMENTO WEEKLY PERFORMANCE ===
@app.callback(
    Output('weekly-performance-status', 'children'),
    Input('refresh-weekly-performance', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_weekly_performance_callback(n_clicks):
    """Aggiorna l'analisi delle performance settimanali"""
    if n_clicks:
        analysis = load_weekly_performance_analysis()
        
        if analysis['available']:
            return html.Div([
                html.Span("✅ Performance settimanali aggiornate!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"📊 {analysis['total_recommendations']} raccomandazioni | {len(analysis['accuracy_by_asset'])} asset analizzati", 
                         style={'fontSize': '12px', 'color': '#7f8c8d'}),
                html.Span(f" - {datetime.datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
        else:
            return html.Div([
                html.Span("⚠️ Nessun dato performance trovato", style={'color': '#e67e22', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span("I file salvataggiwallet non contengono dati sufficienti", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
    return html.Div()

# === CALLBACK CONTENUTO WEEKLY PERFORMANCE ===
@app.callback(
    Output('weekly-performance-section', 'children'),
    Input('refresh-weekly-performance', 'n_clicks'),
    Input('toggle-weekly-performance', 'n_clicks')
)
def update_weekly_performance_content(refresh_clicks, toggle_clicks):
    """Aggiorna il contenuto della sezione performance settimanali"""
    analysis = load_weekly_performance_analysis()
    
    if not analysis['available']:
        return html.Div([
            html.Div([
                html.H4("🚫 Nessuna Analisi Performance Disponibile", style={"color": "#e74c3c", "textAlign": "center"}),
                html.P("Per visualizzare le performance settimanali:", style={"textAlign": "center", "margin": "20px 0"}),
                html.Ol([
                    html.Li("1. Assicurati che il sistema di raccomandazioni sia attivo da almeno una settimana"),
                    html.Li("2. Verifica che esistano i file 'raccomandazioni_storiche.csv' e 'performance_storiche.csv'"),
                    html.Li("3. Clicca 'Aggiorna Analisi' per ricaricare i dati"),
                ], style={"textAlign": "left", "margin": "20px auto", "maxWidth": "500px"}),
                html.P("📁 I file cercati in:", style={"fontWeight": "bold", "marginTop": "30px"}),
                html.P("salvataggiwallet/", style={"fontFamily": "monospace", "backgroundColor": "#f8f9fa", "padding": "10px", "borderRadius": "5px"})
            ], style={"padding": "40px", "backgroundColor": "#fef5e7", "borderRadius": "10px", "margin": "20px"})
        ])
    
    content_sections = []
    
    # === STATISTICHE GENERALI ===
    stats = analysis['summary_stats']
    content_sections.append(
        html.Div([
            html.H4("📊 Statistiche Generali (Ultimi 7 giorni)", style={"color": "#2c3e50", "marginBottom": "15px"}),
            html.Div([
                html.Div([
                    html.H5(str(stats.get('total_recommendations', 0)), style={"color": "#e67e22", "fontSize": "32px", "margin": "0"}),
                    html.P("Raccomandazioni Totali", style={"fontSize": "14px", "color": "#7f8c8d", "margin": "5px 0"})
                ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#fff", "borderRadius": "8px", "border": "1px solid #e67e22", "width": "23%", "display": "inline-block", "margin": "0 1%"}),
                
                html.Div([
                    html.H5(str(stats.get('unique_assets', 0)), style={"color": "#3498db", "fontSize": "32px", "margin": "0"}),
                    html.P("Asset Analizzati", style={"fontSize": "14px", "color": "#7f8c8d", "margin": "5px 0"})
                ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#fff", "borderRadius": "8px", "border": "1px solid #3498db", "width": "23%", "display": "inline-block", "margin": "0 1%"}),
                
                html.Div([
                    html.H5(f"{stats.get('avg_daily_recommendations', 0)}", style={"color": "#9b59b6", "fontSize": "32px", "margin": "0"}),
                    html.P("Media/Giorno", style={"fontSize": "14px", "color": "#7f8c8d", "margin": "5px 0"})
                ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#fff", "borderRadius": "8px", "border": "1px solid #9b59b6", "width": "23%", "display": "inline-block", "margin": "0 1%"}),
                
                html.Div([
                    html.H5(str(stats.get('high_risk_recommendations', 0)), style={"color": "#e74c3c", "fontSize": "32px", "margin": "0"}),
                    html.P("Alto Rischio", style={"fontSize": "14px", "color": "#7f8c8d", "margin": "5px 0"})
                ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#fff", "borderRadius": "8px", "border": "1px solid #e74c3c", "width": "23%", "display": "inline-block", "margin": "0 1%"})
            ], style={"marginBottom": "20px"})
        ], style={"marginBottom": "30px"})
    )
    
    # === TABELLA ACCURACY PER ASSET ===
    if analysis['accuracy_by_asset']:
        accuracy_data = []
        for asset, metrics in analysis['accuracy_by_asset'].items():
            accuracy_data.append({
                "Asset": asset,
                "🎯 Segnali BUY": metrics['buy_signals'],
                "🔴 Segnali SELL": metrics['sell_signals'], 
                "📊 Totale": metrics['total_signals'],
                "📈 Perf. Media 1w": f"{metrics['avg_performance_1w']}%",
                "🎭 Consistenza": f"{metrics['consistency_score']:.2f}",
                "🕒 Ultima Azione": metrics['last_action'][:20] + "..." if len(str(metrics['last_action'])) > 20 else metrics['last_action']
            })
        
        content_sections.append(
            html.Div([
                html.H4("📈 Performance per Asset (Ultimi 7 giorni)", style={"color": "#2c3e50", "marginBottom": "15px"}),
                dash_table.DataTable(
                    data=accuracy_data,
                    columns=[
                        {"name": col, "id": col} for col in accuracy_data[0].keys()
                    ],
                    style_cell={
                        'textAlign': 'center',
                        'padding': '10px',
                        'fontFamily': 'Arial',
                        'fontSize': '12px'
                    },
                    style_header={
                        'backgroundColor': '#e67e22',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{📈 Perf. Media 1w} contains "+"'},
                            'backgroundColor': '#d5f4e6',
                            'color': '#27ae60'
                        },
                        {
                            'if': {'filter_query': '{📈 Perf. Media 1w} contains "-"'},
                            'backgroundColor': '#fadbd8', 
                            'color': '#e74c3c'
                        }
                    ],
                    page_size=10
                )
            ], style={"marginBottom": "30px"})
        )
    
    # === INFO AGGIORNAMENTO ===
    content_sections.append(
        html.Div([
            html.P(f"📅 Ultimo aggiornamento: {stats.get('last_update', 'N/A')}", 
                   style={"fontSize": "12px", "color": "#7f8c8d", "textAlign": "center", "marginTop": "20px"}),
            html.P(f"🔄 I dati vengono aggiornati automaticamente ogni volta che viene eseguita un'analisi del portafoglio", 
                   style={"fontSize": "11px", "color": "#95a5a6", "textAlign": "center", "fontStyle": "italic"})
        ])
    )
    
    return html.Div(content_sections)

# === CALLBACK TOGGLE WEEKLY SUMMARY SECTION ===
@app.callback(
    Output("weekly-summary-section", "style"),
    Input("toggle-weekly-summary", "n_clicks"),
    State("weekly-summary-section", "style")
)
def toggle_weekly_summary_section(n, current_style):
    if not current_style: 
        current_style = {"display": "block"}
    return {"display": "none"} if current_style["display"] == "block" else {"display": "block"}

# === CALLBACK AGGIORNAMENTO WEEKLY SUMMARY ===
@app.callback(
    Output('weekly-summary-status', 'children'),
    Input('refresh-weekly-summary', 'n_clicks'),
    prevent_initial_call=True
)
def refresh_weekly_summary_callback(n_clicks):
    """Aggiorna il riepilogo settimanale"""
    if n_clicks:
        summary = load_weekly_summary_analysis()
        
        if summary['available']:
            return html.Div([
                html.Span("✅ Riepilogo settimanale aggiornato!", style={'color': '#27ae60', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span(f"🎯 {len(summary['weekly_insights'])} insights | {len(summary['asset_focus'])} asset principali", 
                         style={'fontSize': '12px', 'color': '#7f8c8d'}),
                html.Span(f" - {datetime.datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
        else:
            return html.Div([
                html.Span("⚠️ Nessun dato riepilogo trovato", style={'color': '#e67e22', 'fontWeight': 'bold'}),
                html.Br(),
                html.Span("Dati insufficienti per generare il riepilogo", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ])
    return html.Div()

# === CALLBACK CONTENUTO WEEKLY SUMMARY ===
@app.callback(
    Output('weekly-summary-section', 'children'),
    Input('refresh-weekly-summary', 'n_clicks'),
    Input('toggle-weekly-summary', 'n_clicks')
)
def update_weekly_summary_content(refresh_clicks, toggle_clicks):
    """Aggiorna il contenuto del riepilogo settimanale"""
    summary = load_weekly_summary_analysis()
    
    if not summary['available']:
        return html.Div([
            html.Div([
                html.H4("🚫 Nessun Riepilogo Disponibile", style={"color": "#e74c3c", "textAlign": "center"}),
                html.P("Il sistema necessita di almeno una settimana di dati per generare insights significativi.", 
                       style={"textAlign": "center", "margin": "20px 0", "color": "#7f8c8d"}),
                html.P("📊 Dati richiesti: raccomandazioni_storiche.csv", 
                       style={"textAlign": "center", "fontFamily": "monospace", "backgroundColor": "#f8f9fa", "padding": "10px", "borderRadius": "5px"})
            ], style={"padding": "40px", "backgroundColor": "#eafaf1", "borderRadius": "10px", "margin": "20px"})
        ])
    
    content_sections = []
    
    # === INSIGHTS AUTOMATICI ===
    if summary['weekly_insights']:
        content_sections.append(
            html.Div([
                html.H4("🎯 Insights Settimanali", style={"color": "#2c3e50", "marginBottom": "15px"}),
                html.Div([
                    html.Div([
                        html.P(insight, style={"margin": "10px 0", "fontSize": "14px", "color": "#2c3e50"})
                    ], style={"padding": "15px", "backgroundColor": "#fff", "borderRadius": "8px", 
                             "border": "1px solid #27ae60", "margin": "5px 0", "boxShadow": "0 1px 3px rgba(0,0,0,0.1)"}) 
                    for insight in summary['weekly_insights']
                ])
            ], style={"marginBottom": "30px"})
        )
    
    # === DISTRIBUZIONE AZIONI ===
    if summary['action_frequency']:
        actions = summary['action_frequency']
        total_actions = sum(actions.values())
        
        if total_actions > 0:
            content_sections.append(
                html.Div([
                    html.H4("⚖️ Distribuzione Azioni (Ultimi 7 giorni)", style={"color": "#2c3e50", "marginBottom": "15px"}),
                    html.Div([
                        html.Div([
                            html.H5(f"{actions['BUY']}", style={"color": "#27ae60", "fontSize": "24px", "margin": "0"}),
                            html.P("🟢 BUY", style={"fontSize": "12px", "color": "#7f8c8d", "margin": "5px 0"}),
                            html.P(f"{(actions['BUY']/total_actions)*100:.1f}%", style={"fontSize": "11px", "color": "#27ae60", "fontWeight": "bold"})
                        ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#d5f4e6", "borderRadius": "8px", "width": "30%", "display": "inline-block", "margin": "0 1.5%"}),
                        
                        html.Div([
                            html.H5(f"{actions['SELL']}", style={"color": "#e74c3c", "fontSize": "24px", "margin": "0"}),
                            html.P("🔴 SELL", style={"fontSize": "12px", "color": "#7f8c8d", "margin": "5px 0"}),
                            html.P(f"{(actions['SELL']/total_actions)*100:.1f}%", style={"fontSize": "11px", "color": "#e74c3c", "fontWeight": "bold"})
                        ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#fadbd8", "borderRadius": "8px", "width": "30%", "display": "inline-block", "margin": "0 1.5%"}),
                        
                        html.Div([
                            html.H5(f"{actions['HOLD']}", style={"color": "#f39c12", "fontSize": "24px", "margin": "0"}),
                            html.P("🟡 HOLD", style={"fontSize": "12px", "color": "#7f8c8d", "margin": "5px 0"}),
                            html.P(f"{(actions['HOLD']/total_actions)*100:.1f}%", style={"fontSize": "11px", "color": "#f39c12", "fontWeight": "bold"})
                        ], style={"textAlign": "center", "padding": "15px", "backgroundColor": "#fdeaa7", "borderRadius": "8px", "width": "30%", "display": "inline-block", "margin": "0 1.5%"})
                    ], style={"marginBottom": "20px"})
                ], style={"marginBottom": "30px"})
            )
    
    # === FOCUS ASSET ===
    if summary['asset_focus']:
        content_sections.append(
            html.Div([
                html.H4("🎯 Focus Asset (Più Raccomandati)", style={"color": "#2c3e50", "marginBottom": "15px"}),
                html.Div([
                    html.Div([
                        html.H6(asset, style={"color": "#2c3e50", "margin": "5px 0", "fontSize": "14px", "fontWeight": "bold"}),
                        html.P(f"{count} raccomandazioni", style={"fontSize": "12px", "color": "#7f8c8d", "margin": "0"})
                    ], style={"padding": "12px", "backgroundColor": "#fff", "borderRadius": "6px", "border": "1px solid #ddd", "margin": "5px", "width": "22%", "display": "inline-block"})
                    for asset, count in list(summary['asset_focus'].items())[:4]
                ])
            ], style={"marginBottom": "30px"})
        )
    
    # === DISTRIBUZIONE RISCHI ===
    if summary['risk_distribution']:
        content_sections.append(
            html.Div([
                html.H4("⚠️ Distribuzione Livelli di Rischio", style={"color": "#2c3e50", "marginBottom": "15px"}),
                html.Div([
                    html.Div([
                        html.P(f"📊 {risk_level}: {count}", style={"margin": "8px 0", "fontSize": "13px", "color": "#34495e"})
                    ], style={"padding": "10px", "backgroundColor": "#f8f9fa", "borderRadius": "5px", "margin": "3px", "width": "48%", "display": "inline-block"})
                    for risk_level, count in summary['risk_distribution'].items()
                ])
            ], style={"marginBottom": "30px"})
        )
    
    return html.Div(content_sections)

if __name__ == "__main__":
    print("💼 Avvio Wallet Dashboard...")
    print("🌍 Accesso: http://localhost:8051")
    app.run(debug=True, port=8051)
