import requests
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import get_bedrock_llm

class TechnicalAnalysisAgent:  # Removed () after class name
    def __init__(self):
        # Removed super().__init__("technical_analyzer") - this was causing the error!
        
        # Initialize Bedrock LLM
        try:
            self.llm = get_bedrock_llm(
                temperature=0.2,  # Lower for precise technical analysis
                max_tokens=2000
            )
            logging.info("✅ TechnicalAnalysisAgent initialized with Bedrock LLM")
        except Exception as e:
            logging.error(f"❌ Failed to initialize Bedrock LLM: {e}")
            self.llm = None
    
    def get_crypto_id(self, crypto_name):
        """Search for crypto ID dynamically using CoinGecko search API"""
        try:
            # First, try the search API to find the correct ID
            search_url = "https://api.coingecko.com/api/v3/search"
            params = {'query': crypto_name}
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                search_data = response.json()
                coins = search_data.get('coins', [])
                
                if coins:
                    # Return the first match (most relevant)
                    return coins[0]['id']
            
            # Fallback: try the input as-is (lowercase)
            return crypto_name.lower().replace(' ', '-')
            
        except Exception as e:
            logging.warning(f"Error in crypto search: {e}")
            # Fallback: return input as-is
            return crypto_name.lower().replace(' ', '-')
    
    def fetch_ohlcv_data(self, crypto_input, days=90):
        """Fetch OHLCV data from CoinGecko"""
        crypto_id = self.get_crypto_id(crypto_input)
        
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/ohlc"
            params = {'vs_currency': 'usd', 'days': days}
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                return {"error": f"Failed to fetch OHLC data for {crypto_input}"}
            
            data = response.json()
            
            if not data:
                return {"error": "No OHLC data available"}
            
            # Convert to pandas DataFrame for easier analysis
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            logging.error(f"Error fetching OHLCV data: {e}")
            return {"error": str(e)}
    
    def calculate_sma(self, prices, period):
        """Calculate Simple Moving Average"""
        return prices.rolling(window=period).mean()
    
    def calculate_ema(self, prices, period):
        """Calculate Exponential Moving Average"""
        return prices.ewm(span=period).mean()
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        macd_line = ema_fast - ema_slow
        signal_line = self.calculate_ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        sma = self.calculate_sma(prices, period)
        std = prices.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def calculate_support_resistance(self, df, window=10):
        """Calculate support and resistance levels"""
        highs = df['high'].rolling(window=window, center=True).max()
        lows = df['low'].rolling(window=window, center=True).min()
        
        # Find local peaks and troughs
        resistance_levels = df[df['high'] == highs]['high'].dropna().unique()
        support_levels = df[df['low'] == lows]['low'].dropna().unique()
        
        # Get the most recent and significant levels
        current_price = df['close'].iloc[-1]
        
        # Filter levels within reasonable range (±50% of current price)
        resistance_levels = [r for r in resistance_levels if current_price * 0.5 <= r <= current_price * 1.5]
        support_levels = [s for s in support_levels if current_price * 0.5 <= s <= current_price * 1.5]
        
        # Sort and get most relevant levels
        resistance_levels = sorted(resistance_levels, reverse=True)[:3]
        support_levels = sorted(support_levels, reverse=True)[:3]
        
        return {
            'resistance': resistance_levels,
            'support': support_levels
        }
    
    def analyze_volume_trend(self, crypto_input):
        """Analyze volume trends"""
        try:
            crypto_id = self.get_crypto_id(crypto_input)
            url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
            params = {'vs_currency': 'usd', 'days': '30'}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                volumes = data.get('total_volumes', [])
                if volumes:
                    recent_volume = np.mean([v[1] for v in volumes[-7:]])  # Last 7 days
                    older_volume = np.mean([v[1] for v in volumes[:7]])    # First 7 days
                    volume_trend = "increasing" if recent_volume > older_volume else "decreasing"
                    volume_change = ((recent_volume - older_volume) / older_volume) * 100 if older_volume > 0 else 0
                    
                    return {
                        'trend': volume_trend,
                        'change_percent': volume_change,
                        'recent_avg': recent_volume,
                        'older_avg': older_volume
                    }
        except:
            pass
        
        return {'trend': 'unknown', 'change_percent': 0}
    
    def get_technical_signals(self, df):
        """Generate buy/sell/hold signals based on indicators"""
        if len(df) < 50:
            return {"signal": "insufficient_data", "confidence": 0}
        
        signals = []
        current_price = df['close'].iloc[-1]
        
        # RSI signals
        rsi = self.calculate_rsi(df['close'])
        current_rsi = rsi.iloc[-1]
        if current_rsi < 30:
            signals.append(("buy", "RSI oversold", 0.7))
        elif current_rsi > 70:
            signals.append(("sell", "RSI overbought", 0.7))
        
        # Moving Average signals
        sma_20 = self.calculate_sma(df['close'], 20)
        sma_50 = self.calculate_sma(df['close'], 50)
        
        if len(sma_20) > 1 and len(sma_50) > 1:
            if current_price > sma_20.iloc[-1] > sma_50.iloc[-1]:
                signals.append(("buy", "Price above MAs", 0.6))
            elif current_price < sma_20.iloc[-1] < sma_50.iloc[-1]:
                signals.append(("sell", "Price below MAs", 0.6))
        
        # MACD signals
        macd_data = self.calculate_macd(df['close'])
        if len(macd_data['macd']) > 1:
            current_macd = macd_data['macd'].iloc[-1]
            current_signal = macd_data['signal'].iloc[-1]
            if current_macd > current_signal:
                signals.append(("buy", "MACD bullish crossover", 0.6))
            else:
                signals.append(("sell", "MACD bearish crossover", 0.6))
        
        # Bollinger Bands signals
        bb = self.calculate_bollinger_bands(df['close'])
        if len(bb['lower']) > 1:
            if current_price <= bb['lower'].iloc[-1]:
                signals.append(("buy", "Price at lower Bollinger Band", 0.5))
            elif current_price >= bb['upper'].iloc[-1]:
                signals.append(("sell", "Price at upper Bollinger Band", 0.5))
        
        # Aggregate signals
        buy_signals = [s for s in signals if s[0] == "buy"]
        sell_signals = [s for s in signals if s[0] == "sell"]
        
        if len(buy_signals) > len(sell_signals):
            avg_confidence = np.mean([s[2] for s in buy_signals])
            return {"signal": "buy", "confidence": avg_confidence, "reasons": buy_signals}
        elif len(sell_signals) > len(buy_signals):
            avg_confidence = np.mean([s[2] for s in sell_signals])
            return {"signal": "sell", "confidence": avg_confidence, "reasons": sell_signals}
        else:
            return {"signal": "hold", "confidence": 0.5, "reasons": signals}
    
    def perform_technical_analysis(self, crypto_input):
        """Main method to perform comprehensive technical analysis"""
        if not self.llm:
            return {"error": "LLM not initialized"}
        
        try:
            # Fetch OHLCV data
            df = self.fetch_ohlcv_data(crypto_input, days=90)
            
            if isinstance(df, dict) and 'error' in df:
                return df
            
            if len(df) < 20:
                return {"error": "Insufficient data for technical analysis"}
            
            # Calculate all indicators
            current_price = df['close'].iloc[-1]
            rsi = self.calculate_rsi(df['close'])
            macd_data = self.calculate_macd(df['close'])
            bb = self.calculate_bollinger_bands(df['close'])
            support_resistance = self.calculate_support_resistance(df)
            volume_analysis = self.analyze_volume_trend(crypto_input)
            signals = self.get_technical_signals(df)
            
            # Calculate price changes
            price_24h_change = ((current_price - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100 if len(df) > 1 else 0
            price_7d_change = ((current_price - df['close'].iloc[-8]) / df['close'].iloc[-8]) * 100 if len(df) > 7 else 0
            
            # Create analysis context for LLM
            context = f"""Technical Analysis for {crypto_input.upper()}:

CURRENT PRICE DATA:
- Current Price: ${current_price:.6f}
- 24h Change: {price_24h_change:.2f}%
- 7d Change: {price_7d_change:.2f}%

TECHNICAL INDICATORS:
- RSI (14): {rsi.iloc[-1]:.2f} ({self.interpret_rsi(rsi.iloc[-1])})
- MACD: {macd_data['macd'].iloc[-1]:.6f}
- MACD Signal: {macd_data['signal'].iloc[-1]:.6f}
- MACD Histogram: {macd_data['histogram'].iloc[-1]:.6f}

BOLLINGER BANDS:
- Upper Band: ${bb['upper'].iloc[-1]:.6f}
- Middle Band (SMA20): ${bb['middle'].iloc[-1]:.6f}
- Lower Band: ${bb['lower'].iloc[-1]:.6f}
- Position: {self.get_bb_position(current_price, bb)}

SUPPORT & RESISTANCE:
- Key Resistance: {', '.join([f'${r:.6f}' for r in support_resistance['resistance'][:3]])}
- Key Support: {', '.join([f'${s:.6f}' for s in support_resistance['support'][:3]])}

VOLUME ANALYSIS:
- Volume Trend: {volume_analysis['trend']}
- Volume Change: {volume_analysis['change_percent']:.2f}%

TRADING SIGNALS:
- Primary Signal: {signals['signal'].upper()}
- Confidence: {signals['confidence']:.2f}
- Signal Count: {len(signals.get('reasons', []))} indicators"""

            prompt = f"""{context}

Based on this comprehensive technical analysis, provide a detailed assessment:

**TECHNICAL OVERVIEW:**
- Overall trend direction (bullish/bearish/sideways)
- Momentum analysis (strong/weak/neutral)
- Key technical levels to watch

**INDICATOR ANALYSIS:**
- RSI interpretation and what it suggests
- MACD momentum signals
- Bollinger Bands positioning
- Support/resistance level significance

**TRADING RECOMMENDATIONS:**
- Entry points for long/short positions
- Stop-loss suggestions based on technical levels
- Profit targets using resistance/support
- Risk/reward assessment

**MARKET STRUCTURE:**
- Current market phase (accumulation/distribution/trending)
- Volume confirmation of price movements
- Probability of trend continuation vs reversal

Be specific with price levels and provide actionable insights based purely on technical analysis."""

            # Get LLM analysis
            response = self.llm.invoke(prompt)
            analysis = response.content if hasattr(response, 'content') else str(response)
            
            # Return comprehensive results
            result = {
                'analysis': analysis,
                'current_price': current_price,
                'rsi': rsi.iloc[-1],
                'macd': {
                    'macd': macd_data['macd'].iloc[-1],
                    'signal': macd_data['signal'].iloc[-1],
                    'histogram': macd_data['histogram'].iloc[-1]
                },
                'bollinger_bands': {
                    'upper': bb['upper'].iloc[-1],
                    'middle': bb['middle'].iloc[-1],
                    'lower': bb['lower'].iloc[-1]
                },
                'support_resistance': support_resistance,
                'volume_trend': volume_analysis,
                'signals': signals,
                'price_changes': {
                    '24h': price_24h_change,
                    '7d': price_7d_change
                }
            }
            
            logging.info(f"✅ Generated technical analysis for {crypto_input}")
            return result
            
        except Exception as e:
            error_msg = f"Error performing technical analysis: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}
    
    def interpret_rsi(self, rsi_value):
        """Interpret RSI value"""
        if rsi_value >= 70:
            return "Overbought"
        elif rsi_value <= 30:
            return "Oversold"
        elif rsi_value >= 50:
            return "Bullish"
        else:
            return "Bearish"
    
    def get_bb_position(self, current_price, bb):
        """Determine position relative to Bollinger Bands"""
        upper = bb['upper'].iloc[-1]
        lower = bb['lower'].iloc[-1]
        middle = bb['middle'].iloc[-1]
        
        if current_price >= upper:
            return "Above upper band (overbought)"
        elif current_price <= lower:
            return "Below lower band (oversold)"
        elif current_price > middle:
            return "Above middle (bullish)"
        else:
            return "Below middle (bearish)"