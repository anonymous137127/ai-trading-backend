import numpy as np

def calculate_rsi(data, period=14):
    try:
        # 🔒 safety check
        if not data or len(data) < period + 1:
            for c in data:
                c["rsi"] = 50
            return data

        closes = np.array([c.get("close", 0) for c in data])

        deltas = np.diff(closes)
        gains = np.maximum(deltas, 0)
        losses = -np.minimum(deltas, 0)

        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        rsi_values = [50] * len(data)  # default RSI

        # 🔥 calculate RSI safely
        for i in range(period, len(closes)):
            avg_gain = (avg_gain * (period - 1) + gains[i - 1]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i - 1]) / period

            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))

            rsi_values[i] = rsi

        # 🔥 attach RSI to data
        for i in range(len(data)):
            data[i]["rsi"] = rsi_values[i]

        return data

    except Exception as e:
        print("RSI ERROR:", str(e))

        # fallback safe
        for c in data:
            c["rsi"] = 50

        return data