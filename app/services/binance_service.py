import requests

def get_candles(symbol="BTCUSDT", interval="1m"):
    try:
        url = "https://api.binance.com/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": interval,   # ✅ dynamic timeframe
            "limit": 300
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        candles = []

        for c in data:
            candles.append({
                "time": int(c[0]),   # 🔥 important for chart
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5])
            })

        return candles

    except Exception as e:
        print("BINANCE ERROR:", str(e))
        return []