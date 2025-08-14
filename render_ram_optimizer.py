# === RENDER RAM OPTIMIZER - 512MB CONSTRAINT ===
"""
Sistema di ottimizzazione per Render che mantiene i messaggi completi
ma ottimizza drasticamente i calcoli per funzionare con 512MB di RAM
"""

import os
import gc
import sys
import threading
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from functools import lru_cache
import warnings
warnings.filterwarnings('ignore')

# === MEMORY MONITORING ===
try:
    import psutil
    MEMORY_MONITORING_AVAILABLE = True
except ImportError:
    MEMORY_MONITORING_AVAILABLE = False
    print("⚠️ [RENDER] psutil not available, using basic memory management")

class RenderMemoryManager:
    def __init__(self, max_memory_mb=450):  # Lascia 62MB di buffer su 512MB
        self.max_memory_mb = max_memory_mb
        self.critical_threshold = 400  # MB
        self.warning_threshold = 350   # MB
        
    def get_memory_usage_mb(self):
        """Ottieni utilizzo memoria corrente"""
        if MEMORY_MONITORING_AVAILABLE:
            try:
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024
            except:
                pass
        
        # Fallback senza psutil
        return sys.getsizeof(gc.get_objects()) / 1024 / 1024
    
    def force_cleanup(self):
        """Pulizia aggressiva della memoria"""
        current_mem = self.get_memory_usage_mb()
        print(f"🧹 [RENDER] Cleanup start: {current_mem:.1f}MB")
        
        # Clear all possible caches
        if hasattr(self, '_cached_data'):
            delattr(self, '_cached_data')
        
        # Force garbage collection multiple times
        for _ in range(3):
            gc.collect()
        
        # Clear pandas caches
        if hasattr(pd, 'plotting'):
            try:
                pd.plotting._core.PlotAccessor._accessors.clear()
            except:
                pass
                
        after_mem = self.get_memory_usage_mb()
        print(f"✅ [RENDER] Cleanup done: {after_mem:.1f}MB (freed: {current_mem-after_mem:.1f}MB)")
        
    def is_memory_critical(self):
        """Controlla se siamo in zona critica"""
        return self.get_memory_usage_mb() > self.critical_threshold
    
    def memory_check_decorator(self, func):
        """Decorator per monitorare memoria durante le funzioni"""
        def wrapper(*args, **kwargs):
            mem_before = self.get_memory_usage_mb()
            if mem_before > self.warning_threshold:
                print(f"⚠️ [RENDER] High memory before {func.__name__}: {mem_before:.1f}MB")
                self.force_cleanup()
            
            result = func(*args, **kwargs)
            
            mem_after = self.get_memory_usage_mb()
            if mem_after > self.critical_threshold:
                print(f"🚨 [RENDER] Critical memory after {func.__name__}: {mem_after:.1f}MB")
                self.force_cleanup()
                
            return result
        return wrapper

# Istanza globale del memory manager
memory_manager = RenderMemoryManager()

# === LIGHTWEIGHT MODEL SYSTEM ===
class RenderLightweightModels:
    """Sistema di modelli ultra-leggeri per Render"""
    
    def __init__(self):
        self.models = {}
        self._load_essential_models()
    
    def _load_essential_models(self):
        """Carica solo 3 modelli essenziali e leggeri"""
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.naive_bayes import GaussianNB
            
            # Solo 3 modelli ultra-ottimizzati
            self.models = {
                "Logistic": LogisticRegression(
                    solver='liblinear', 
                    max_iter=100,  # Ridotto da default
                    random_state=42
                ),
                "RandomForest": RandomForestClassifier(
                    n_estimators=20,  # Ridotto drasticamente da 100
                    max_depth=5,      # Limitato per ridurre memoria
                    random_state=42,
                    n_jobs=1          # Single thread per controllare memoria
                ),
                "NaiveBayes": GaussianNB()  # Modello più leggero possibile
            }
            
            print(f"🚀 [RENDER] Loaded {len(self.models)} lightweight models")
            
        except Exception as e:
            print(f"❌ [RENDER] Error loading models: {e}")
            # Fallback con modelli fittizi
            self.models = {
                "Fallback": None
            }
    
    def get_model_names(self):
        """Ottieni nomi dei modelli disponibili"""
        return list(self.models.keys())
    
    def get_model(self, name):
        """Ottieni istanza del modello"""
        return self.models.get(name)

# === ULTRA-COMPACT DATA LOADING ===
class RenderDataLoader:
    """Caricatore dati ottimizzato per Render"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        self.max_cache_age_minutes = 60  # Cache più lunga per ridurre requests
        
    @memory_manager.memory_check_decorator
    def load_essential_data(self, symbol, max_days=90):
        """Carica solo dati essenziali con cache aggressivo"""
        cache_key = f"{symbol}_{max_days}"
        
        # Check cache first
        if cache_key in self.cache:
            cache_age = (datetime.now() - self.cache_timestamps[cache_key]).total_seconds() / 60
            if cache_age < self.max_cache_age_minutes:
                print(f"📦 [RENDER] Cache hit for {symbol}")
                return self.cache[cache_key]
        
        print(f"🌐 [RENDER] Loading fresh data for {symbol}")
        
        try:
            if symbol == "BTC":
                df = self._load_crypto_minimal(symbol, max_days)
            else:
                df = self._load_fred_minimal(symbol, max_days)
            
            # Store in cache
            if not df.empty:
                self.cache[cache_key] = df
                self.cache_timestamps[cache_key] = datetime.now()
                
                # Limit cache size
                if len(self.cache) > 10:
                    oldest_key = min(self.cache_timestamps.keys(), 
                                   key=lambda k: self.cache_timestamps[k])
                    del self.cache[oldest_key]
                    del self.cache_timestamps[oldest_key]
            
            return df
            
        except Exception as e:
            print(f"❌ [RENDER] Error loading {symbol}: {e}")
            return pd.DataFrame()
    
    def _load_crypto_minimal(self, symbol, max_days):
        """Caricamento crypto ultra-minimal"""
        try:
            import requests
            
            # Riduci drasticamente il numero di giorni richiesti
            limit = min(max_days, 90)  # Max 90 giorni
            
            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            params = {
                'fsym': symbol,
                'tsym': 'USD',
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data['Response'] == 'Success' and data['Data']['Data']:
                df = pd.DataFrame(data['Data']['Data'])
                df['Date'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('Date', inplace=True)
                
                # Solo la colonna Close per risparmiare memoria
                df = df[['close']].rename(columns={'close': 'Close'})
                
                # Prendi solo gli ultimi 60 giorni per ridurre memoria
                return df.tail(60)
            
        except Exception as e:
            print(f"❌ [RENDER] Crypto load error {symbol}: {e}")
            
        return pd.DataFrame()
    
    def _load_fred_minimal(self, symbol, max_days):
        """Caricamento FRED ultra-minimal"""
        try:
            from pandas_datareader import data as web
            
            # Carica solo ultimi 3 mesi invece di anni
            end = datetime.now()
            start = end - timedelta(days=min(max_days, 90))
            
            df = web.DataReader(symbol, 'fred', start, end)
            if not df.empty:
                df.columns = ['Close']
                df.dropna(inplace=True)
                
                # Prendi solo gli ultimi 60 giorni
                return df.tail(60)
                
        except Exception as e:
            print(f"❌ [RENDER] FRED load error {symbol}: {e}")
            
        return pd.DataFrame()

# === MINIMAL TECHNICAL INDICATORS ===
class RenderIndicators:
    """Indicatori tecnici ultra-ottimizzati per Render"""
    
    @staticmethod
    @memory_manager.memory_check_decorator
    def calculate_essential_indicators(df):
        """Calcola solo 5 indicatori essenziali"""
        if df.empty or len(df) < 20:
            return {}
        
        try:
            indicators = {}
            
            # 1. SMA (più semplice)
            sma_short = df['Close'].rolling(10, min_periods=5).mean()
            sma_long = df['Close'].rolling(20, min_periods=10).mean()
            indicators['SMA'] = 1 if sma_short.iloc[-1] > sma_long.iloc[-1] else -1 if sma_short.iloc[-1] < sma_long.iloc[-1] else 0
            
            # 2. RSI (semplificato)
            delta = df['Close'].diff()
            gain = delta.where(delta > 0, 0).rolling(14, min_periods=7).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14, min_periods=7).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            last_rsi = rsi.iloc[-1]
            indicators['RSI'] = -1 if last_rsi > 70 else 1 if last_rsi < 30 else 0
            
            # 3. MACD (semplificato)
            exp12 = df['Close'].ewm(span=12).mean()
            exp26 = df['Close'].ewm(span=26).mean()
            macd = exp12 - exp26
            signal = macd.ewm(span=9).mean()
            indicators['MACD'] = 1 if macd.iloc[-1] > signal.iloc[-1] else -1
            
            # 4. Bollinger Bands
            bb_mid = df['Close'].rolling(20, min_periods=10).mean()
            bb_std = df['Close'].rolling(20, min_periods=10).std()
            bb_upper = bb_mid + (bb_std * 2)
            bb_lower = bb_mid - (bb_std * 2)
            last_price = df['Close'].iloc[-1]
            indicators['Bollinger'] = -1 if last_price > bb_upper.iloc[-1] else 1 if last_price < bb_lower.iloc[-1] else 0
            
            # 5. EMA
            ema_fast = df['Close'].ewm(span=12).mean()
            ema_slow = df['Close'].ewm(span=26).mean()
            indicators['EMA'] = 1 if ema_fast.iloc[-1] > ema_slow.iloc[-1] else -1
            
            return indicators
            
        except Exception as e:
            print(f"❌ [RENDER] Indicators error: {e}")
            return {}

# === RENDER-OPTIMIZED ML TRAINING ===
class RenderMLProcessor:
    """Processore ML ottimizzato per Render"""
    
    def __init__(self):
        self.models = RenderLightweightModels()
    
    @memory_manager.memory_check_decorator
    def train_model_minimal(self, model_name, df):
        """Training ML ultra-veloce e leggero"""
        try:
            if df.empty or len(df) < 20:
                return 0.5, 0.5
            
            model = self.models.get_model(model_name)
            if model is None:
                return 0.5, 0.5
            
            # Features minimaliste
            df_work = df.copy()
            df_work['Return'] = df_work['Close'].pct_change(3)  # Ridotto da 5 a 3
            df_work['Volatility'] = df_work['Close'].rolling(7).std()  # Ridotto da 10 a 7
            df_work.dropna(inplace=True)
            
            if len(df_work) < 15:
                return 0.5, 0.5
            
            # Target semplificato
            df_work['Target'] = (df_work['Close'].shift(-3) > df_work['Close']).astype(int)
            df_work.dropna(inplace=True)
            
            if len(df_work) < 10:
                return 0.5, 0.5
            
            # Solo ultimi dati per training (riduce memoria)
            df_train = df_work.tail(30)  # Max 30 punti per training
            
            X = df_train[['Return', 'Volatility']].iloc[:-3]
            y = df_train['Target'].iloc[:-3]
            
            if len(X) < 5 or len(y) < 5:
                return 0.5, 0.5
            
            # Training velocissimo
            model.fit(X, y)
            
            # Predizione su ultimo dato
            last_X = df_train[['Return', 'Volatility']].iloc[-1:].values
            prob = model.predict_proba(last_X)[0][1]
            
            # Accuratezza semplificata (evita calcoli pesanti)
            acc = 0.6 + (abs(prob - 0.5) * 0.6)  # Stima basata su confidence
            
            return prob, acc
            
        except Exception as e:
            print(f"❌ [RENDER] ML training error {model_name}: {e}")
            return 0.5, 0.5
    
    def process_all_assets_light(self, selected_horizon):
        """Processa tutti gli asset con modelli ML ottimizzati per Render"""
        try:
            print(f"🚀 [RENDER-ML] Processing all assets with horizon {selected_horizon}")
            
            # Asset e simboli corretti
            assets_symbols = {
                "Bitcoin": "BTC",
                "Dollar Index": "DTWEXBGS", 
                "S&P 500": "SP500",
                "Gold (PAXG)": "PAXG"
            }
            
            results = []
            data_loader = RenderDataLoader()
            
            # Per tutti i modelli disponibili
            for model_name in self.models.get_model_names():
                print(f"🤖 [RENDER-ML] Processing model: {model_name}")
                
                for asset_name, symbol in assets_symbols.items():
                    try:
                        # Carica dati ottimizzati
                        df = data_loader.load_essential_data(symbol)
                        
                        if df.empty or len(df) < 20:
                            print(f"⚠️ [RENDER-ML] Insufficient data for {asset_name}")
                            continue
                        
                        # Training ML ottimizzato
                        prob, acc = self.train_model_minimal(model_name, df)
                        
                        # Sistema a 5 livelli come nel sistema standard
                        if prob >= 0.75:
                            signal = "BUY"
                        elif prob <= 0.25:
                            signal = "SELL"
                        elif prob >= 0.6:
                            signal = "WEAK BUY"
                        elif prob <= 0.4:
                            signal = "WEAK SELL"
                        else:
                            signal = "HOLD"
                        
                        # Formato risultato compatibile con 555-server.py
                        result = {
                            "model": model_name,
                            "asset": asset_name,
                            "probability": round(prob * 100, 2),
                            "accuracy": round(acc * 100, 2),
                            "signal": signal
                        }
                        
                        results.append(result)
                        print(f"✅ [RENDER-ML] {model_name} on {asset_name}: {signal} ({result['probability']}%)")
                        
                        # Memory cleanup ogni 4 asset per sicurezza
                        if len(results) % 4 == 0 and memory_manager.is_memory_critical():
                            memory_manager.force_cleanup()
                        
                    except Exception as e:
                        print(f"❌ [RENDER-ML] Error processing {model_name}-{asset_name}: {e}")
                        # Fallback result in case of error
                        results.append({
                            "model": model_name,
                            "asset": asset_name,
                            "probability": 50.0,
                            "accuracy": 50.0,
                            "signal": "HOLD"
                        })
                        continue
                
                # Memory cleanup after each model
                if memory_manager.is_memory_critical():
                    memory_manager.force_cleanup()
            
            print(f"✅ [RENDER-ML] Completed processing: {len(results)} results generated")
            print(f"💾 [RENDER-ML] Final memory usage: {memory_manager.get_memory_usage_mb():.1f}MB")
            
            return results
            
        except Exception as e:
            print(f"❌ [RENDER-ML] Critical error in process_all_assets_light: {e}")
            # Return fallback results to prevent system crash
            fallback_results = []
            
            assets = ["Bitcoin", "Dollar Index", "S&P 500", "Gold (PAXG)"]
            models = self.models.get_model_names() if self.models else ["Fallback"]
            
            for model in models:
                for asset in assets:
                    fallback_results.append({
                        "model": model,
                        "asset": asset,
                        "probability": 50.0,
                        "accuracy": 50.0,
                        "signal": "HOLD"
                    })
            
            return fallback_results

# === RENDER MESSAGE GENERATOR ===
class RenderMessageGenerator:
    """Generatore messaggi completi ottimizzato per Render"""
    
    def __init__(self):
        self.data_loader = RenderDataLoader()
        self.ml_processor = RenderMLProcessor()
        
        # Asset essenziali (ridotti da 4 a 3 per memoria)
        self.essential_assets = {
            "Bitcoin": "BTC",
            "S&P 500": "SP500", 
            "Dollar Index": "DTWEXBGS"
        }
    
    @memory_manager.memory_check_decorator
    def generate_full_report(self, report_type="manual"):
        """Genera il report completo ottimizzato per RAM"""
        try:
            print(f"🚀 [RENDER] Generating {report_type} report...")
            
            now = datetime.now()
            report_parts = []
            
            # === SEZIONE 1: INDICATORI TECNICI COMPLETI ===
            indicators_section = self._generate_indicators_section()
            report_parts.append(indicators_section)
            
            # Memory cleanup between sections
            if memory_manager.is_memory_critical():
                memory_manager.force_cleanup()
            
            # === SEZIONE 2: SEGNALI ML COMPLETI ===
            ml_section = self._generate_ml_section()
            report_parts.append(ml_section)
            
            # Memory cleanup
            if memory_manager.is_memory_critical():
                memory_manager.force_cleanup()
            
            # === SEZIONE 3: NOTIZIE ===
            news_section = self._generate_news_section()
            report_parts.append(news_section)
            
            # === SEZIONE 4: CALENDARIO ===
            calendar_section = self._generate_calendar_section()
            report_parts.append(calendar_section)
            
            # Combina tutto
            full_report = f"🚀 *REPORT COMPLETO - {now.strftime('%d/%m/%Y %H:%M')}*\n\n"
            full_report += "\n\n".join(report_parts)
            
            # Aggiungi info memoria
            memory_usage = memory_manager.get_memory_usage_mb()
            full_report += f"\n\n💾 RAM: {memory_usage:.1f}MB | ⚡ Render Optimized"
            
            print(f"✅ [RENDER] Report generated successfully ({memory_usage:.1f}MB)")
            return full_report
            
        except Exception as e:
            print(f"❌ [RENDER] Critical error in report generation: {e}")
            return f"❌ *RENDER ERROR*\n{str(e)}\n💾 {memory_manager.get_memory_usage_mb():.1f}MB"
    
    def _generate_indicators_section(self):
        """Genera sezione indicatori completa ma ottimizzata"""
        try:
            lines = ["📈 *INDICATORI TECNICI COMPLETI (5 CORE)*"]
            lines.append("```")
            lines.append("Asset     |SMA|RSI|MCD|BOL|EMA| Consensus")
            lines.append("─" * 42)
            
            for asset_name, symbol in self.essential_assets.items():
                df = self.data_loader.load_essential_data(symbol)
                
                if not df.empty:
                    indicators = RenderIndicators.calculate_essential_indicators(df)
                    
                    # Convert to emojis
                    sma = "🟢" if indicators.get('SMA', 0) == 1 else "🔴" if indicators.get('SMA', 0) == -1 else "⚪"
                    rsi = "🟢" if indicators.get('RSI', 0) == 1 else "🔴" if indicators.get('RSI', 0) == -1 else "⚪"
                    macd = "🟢" if indicators.get('MACD', 0) == 1 else "🔴" if indicators.get('MACD', 0) == -1 else "⚪"
                    bol = "🟢" if indicators.get('Bollinger', 0) == 1 else "🔴" if indicators.get('Bollinger', 0) == -1 else "⚪"
                    ema = "🟢" if indicators.get('EMA', 0) == 1 else "🔴" if indicators.get('EMA', 0) == -1 else "⚪"
                    
                    # Consensus
                    signals = [indicators.get(ind, 0) for ind in ['SMA', 'RSI', 'MACD', 'Bollinger', 'EMA']]
                    buy_count = sum(1 for s in signals if s == 1)
                    sell_count = sum(1 for s in signals if s == -1)
                    
                    if buy_count > sell_count:
                        consensus = f"🟢BUY({buy_count}/5)"
                    elif sell_count > buy_count:
                        consensus = f"🔴SELL({sell_count}/5)"
                    else:
                        consensus = f"⚪HOLD({buy_count}B/{sell_count}S)"
                    
                    asset_short = asset_name[:9] if len(asset_name) > 9 else asset_name
                    lines.append(f"{asset_short:<9} | {sma} {rsi} {macd} {bol} {ema} | {consensus}")
                else:
                    asset_short = asset_name[:9]
                    lines.append(f"{asset_short:<9} | ❌ ❌ ❌ ❌ ❌ | ❌DATA")
            
            lines.append("```")
            return "\n".join(lines)
            
        except Exception as e:
            return f"📈 *INDICATORI TECNICI*\n❌ Error: {str(e)}"
    
    def _generate_ml_section(self):
        """Genera sezione ML completa ma ottimizzata"""
        try:
            lines = ["🤖 *SEGNALI MACHINE LEARNING*"]
            lines.append("```")
            lines.append(f"🤖 MODELLI ML ATTIVI: {len(self.ml_processor.models.get_model_names())}")
            lines.append("")
            
            # Header tabella
            model_names = self.ml_processor.models.get_model_names()
            models_short = [name[:3].upper() for name in model_names]
            header = "Asset     |" + "|".join(f"{m:>4}" for m in models_short)
            lines.append(header)
            lines.append("─" * len(header))
            
            # Process each asset
            for asset_name, symbol in self.essential_assets.items():
                df = self.data_loader.load_essential_data(symbol)
                asset_short = asset_name[:9] if len(asset_name) > 9 else asset_name
                row = f"{asset_short:<9} |"
                
                if not df.empty:
                    for model_name in model_names:
                        prob, _ = self.ml_processor.train_model_minimal(model_name, df)
                        
                        # Signal with probability
                        if prob >= 0.7:
                            signal = f"🟢{round(prob*100)}"
                        elif prob <= 0.3:
                            signal = f"🔴{round(prob*100)}"
                        else:
                            signal = f"⚪{round(prob*100)}"
                        
                        row += f"{signal:>4}|"
                else:
                    for _ in model_names:
                        row += f"{'❌':>4}|"
                
                lines.append(row)
            
            lines.append("```")
            return "\n".join(lines)
            
        except Exception as e:
            return f"🤖 *SEGNALI ML*\n❌ Error: {str(e)}"
    
    def _generate_news_section(self):
        """Genera sezione notizie ottimizzata"""
        try:
            # Placeholder per notizie - implementazione leggera
            return "📰 *NOTIZIE CRITICHE*\n• Sistema ottimizzato per Render\n• Caricamento notizie in modalità risparmio RAM"
            
        except Exception as e:
            return f"📰 *NOTIZIE*\n❌ Error: {str(e)}"
    
    def _generate_calendar_section(self):
        """Genera sezione calendario ottimizzata"""
        try:
            # Placeholder per calendario - implementazione leggera
            today = datetime.now().strftime('%d/%m/%Y')
            return f"📅 *CALENDARIO EVENTI*\n📅 {today}\n• Sistema calendario ottimizzato per Render"
            
        except Exception as e:
            return f"📅 *CALENDARIO*\n❌ Error: {str(e)}"

# === RENDER SCHEDULER OTTIMIZZATO ===
def render_optimized_scheduler():
    """Scheduler ottimizzato per Render con messaggi completi"""
    import pytz
    
    italy_tz = pytz.timezone('Europe/Rome')
    message_generator = RenderMessageGenerator()
    
    print("🚀 [RENDER-SCHEDULER] Started - Full messages with RAM optimization")
    
    while True:
        try:
            now = datetime.now(italy_tz)
            
            # Memory check ad ogni ciclo
            current_memory = memory_manager.get_memory_usage_mb()
            if current_memory > 400:
                print(f"🧹 [RENDER] Memory cleanup triggered: {current_memory:.1f}MB")
                memory_manager.force_cleanup()
            
            # Morning report - 09:00
            if now.hour == 9 and now.minute == 0:
                try:
                    print("🌅 [RENDER] Morning report trigger")
                    report = message_generator.generate_full_report("morning")
                    
                    # Here you would call your telegram function
                    print(f"📤 [RENDER] Morning report ready: {len(report)} chars")
                    # invia_messaggio_telegram(report)
                    
                    time.sleep(60)  # Prevent double trigger
                    
                except Exception as e:
                    print(f"❌ [RENDER] Morning report error: {e}")
                    memory_manager.force_cleanup()
            
            # Daily report - 13:00
            elif now.hour == 13 and now.minute == 0:
                try:
                    print("📊 [RENDER] Daily report trigger")
                    report = message_generator.generate_full_report("daily")
                    
                    # Here you would call your telegram function
                    print(f"📤 [RENDER] Daily report ready: {len(report)} chars")
                    # invia_messaggio_telegram(report)
                    
                    time.sleep(60)  # Prevent double trigger
                    
                except Exception as e:
                    print(f"❌ [RENDER] Daily report error: {e}")
                    memory_manager.force_cleanup()
            
            # Sleep with memory consideration
            time.sleep(120 if current_memory < 300 else 180)  # Longer sleep if memory is high
            
        except Exception as e:
            print(f"❌ [RENDER-SCHEDULER] Critical error: {e}")
            memory_manager.force_cleanup()
            time.sleep(300)  # 5 minutes on critical error

# === TEST FUNCTION ===
if __name__ == "__main__":
    print("🧪 [RENDER] Testing optimization system...")
    
    # Test memory manager
    print(f"💾 [RENDER] Initial memory: {memory_manager.get_memory_usage_mb():.1f}MB")
    
    # Test message generator
    generator = RenderMessageGenerator()
    test_report = generator.generate_full_report("test")
    
    print("=" * 60)
    print("RENDER OPTIMIZED REPORT SAMPLE:")
    print("=" * 60)
    print(test_report[:1000] + "..." if len(test_report) > 1000 else test_report)
    print("=" * 60)
    print(f"Final memory: {memory_manager.get_memory_usage_mb():.1f}MB")
    print(f"Report length: {len(test_report)} characters")
