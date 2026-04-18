import numpy as np

# =============================
# INDICATORS
# =============================

def calculate_ema(prices, period=14):
    ema = []
    k = 2 / (period + 1)

    for i in range(len(prices)):
        if i == 0:
            ema.append(prices[i])
        else:
            ema.append(prices[i] * k + ema[i - 1] * (1 - k))

    return ema


def calculate_macd(prices):
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)

    macd = np.array(ema12) - np.array(ema26)
    signal = calculate_ema(macd.tolist(), 9)

    return macd[-1], signal[-1]


def calculate_bollinger(prices, period=20):
    if len(prices) < period:
        return prices[-1], prices[-1]

    sma = np.mean(prices[-period:])
    std = np.std(prices[-period:])

    upper = sma + (2 * std)
    lower = sma - (2 * std)

    return upper, lower


def calculate_momentum(prices):
    if len(prices) < 5:
        return 0
    return prices[-1] - prices[-5]


def calculate_trend_strength(prices):
    # simple slope
    x = np.arange(len(prices[-10:]))
    y = np.array(prices[-10:])
    slope = np.polyfit(x, y, 1)[0]
    return slope


# =============================
# MAIN AI SIGNAL
# =============================

def generate_signal(df):
    try:
        # 🔒 safety
        if not df or len(df) < 30:
            return {"signal": "HOLD", "confidence": 50}

        closes = [c.get("close", 0) for c in df]
        rsi_values = [c.get("rsi", 50) for c in df]

        last = closes[-1]
        prev = closes[-2]

        rsi = rsi_values[-1]

        ema_fast = calculate_ema(closes, 9)[-1]
        ema_slow = calculate_ema(closes, 21)[-1]

        macd, macd_signal = calculate_macd(closes)
        upper_bb, lower_bb = calculate_bollinger(closes)
        momentum = calculate_momentum(closes)
        trend = calculate_trend_strength(closes)

        score = 0

        # =============================
        # RSI (Dynamic)
        # =============================
        if rsi < 30:
            score += 3
        elif rsi < 40:
            score += 1
        elif rsi > 70:
            score -= 3
        elif rsi > 60:
            score -= 1

        # =============================
        # EMA CROSSOVER
        # =============================
        if ema_fast > ema_slow:
            score += 3
        else:
            score -= 3

        # =============================
        # MACD
        # =============================
        if macd > macd_signal:
            score += 2
        else:
            score -= 2

        # =============================
        # MOMENTUM
        # =============================
        if momentum > 0:
            score += 1
        else:
            score -= 1

        # =============================
        # BOLLINGER
        # =============================
        if last < lower_bb:
            score += 2
        elif last > upper_bb:
            score -= 2

        # =============================
        # TREND STRENGTH
        # =============================
        if trend > 0:
            score += 2
        else:
            score -= 2

        # =============================
        # PRICE ACTION
        # =============================
        if last > prev:
            score += 1
        else:
            score -= 1

        # =============================
        # FINAL DECISION
        # =============================

        # 🔥 reduce HOLD (more aggressive)
        if score >= 4:
            return {
                "signal": "BUY",
                "confidence": min(90, 70 + score * 2)
            }

        elif score <= -4:
            return {
                "signal": "SELL",
                "confidence": min(90, 70 + abs(score) * 2)
            }

        else:
            # 👉 convert weak HOLD into direction
            if score > 0:
                return {"signal": "BUY", "confidence": 55}
            elif score < 0:
                return {"signal": "SELL", "confidence": 55}
            else:
                return {"signal": "HOLD", "confidence": 50}

    except Exception as e:
        print("AI ERROR:", str(e))
        return {"signal": "HOLD", "confidence": 50}