import time
import threading
from flask import current_app

from app.services.binance_service import get_candles
from app.services.indicator_service import calculate_rsi
from app.services.prediction_service import generate_signal
from app.database.mongo import db


def analyze_symbol(symbol="BTCUSDT", interval="1m"):
    try:
        data = get_candles(symbol, interval)

        if not data or len(data) < 50:
            return

        df = calculate_rsi(data)
        result = generate_signal(df)

        payload = {
            "symbol": symbol,
            "interval": interval,
            "signal": result.get("signal", "HOLD"),
            "confidence": result.get("confidence", 50),
            "timestamp": time.time()
        }

        # 🔥 SAVE DB
        db.predictions.update_one(
            {"symbol": symbol, "interval": interval},
            {"$set": payload},
            upsert=True
        )

        print(f"[LIVE AI] {symbol} → {payload}")

        # 🚀 SEND LIVE SIGNAL
        socketio = current_app.socketio
        socketio.emit("ai_signal", payload)

    except Exception as e:
        print("AI ERROR:", e)


def run_ai_loop():
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

    while True:
        for sym in symbols:
            analyze_symbol(sym)

        time.sleep(10)  # 🔥 LIVE TEST (change to 300 later)


def start_ai():
    thread = threading.Thread(target=run_ai_loop)
    thread.daemon = True
    thread.start()