import time
import threading
from app.services.binance_service import get_klines
from app.services.indicator_service import calculate_indicators
from app.database.mongo import db

def analyze_symbol(symbol="BTCUSDT", interval="1m"):
    try:
        # 🔥 GET MARKET DATA
        data = get_klines(symbol, interval)

        if not data:
            return

        # 🔥 APPLY INDICATORS
        df = calculate_indicators(data)

        last = df.iloc[-1]

        # 🔥 SIMPLE AI LOGIC (UPGRADE LATER)
        signal = "HOLD"
        confidence = 50

        if last["rsi"] < 30 and last["macd"] > 0:
            signal = "BUY"
            confidence = 85

        elif last["rsi"] > 70 and last["macd"] < 0:
            signal = "SELL"
            confidence = 85

        # 🔥 SAVE TO DB
        db.predictions.update_one(
            {"symbol": symbol, "interval": interval},
            {
                "$set": {
                    "signal": signal,
                    "confidence": confidence,
                    "timestamp": time.time()
                }
            },
            upsert=True
        )

        print(f"[AI] {symbol} → {signal} ({confidence}%)")

    except Exception as e:
        print("AI Error:", e)


def run_ai_loop():
    while True:
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

        for sym in symbols:
            analyze_symbol(sym)

        print("✅ AI cycle completed... waiting 5 min")
        time.sleep(300)  # 🔥 5 MINUTES


def start_ai():
    thread = threading.Thread(target=run_ai_loop)
    thread.daemon = True
    thread.start()