from flask import Blueprint, request, jsonify
from app.database.mongo import db

# 🔥 Blueprint
ai_bp = Blueprint("ai", __name__)


# =========================================
# 🔥 SINGLE COIN (FAST - FROM DB)
# =========================================
@ai_bp.route("/ai", methods=["GET"])
def ai_prediction():
    try:
        symbol = request.args.get("symbol", "BTCUSDT")
        interval = request.args.get("interval", "1m")

        print(f"[AI API] Fetching {symbol} ({interval})")

        data = db.predictions.find_one(
            {"symbol": symbol, "interval": interval},
            {"_id": 0}
        )

        # 🔒 IF NOT READY → RETURN SAFE DEFAULT
        if not data:
            return jsonify({
                "symbol": symbol,
                "interval": interval,
                "signal": "HOLD",
                "confidence": 50,
                "status": "waiting"
            })

        return jsonify(data)

    except Exception as e:
        print("AI ERROR:", str(e))

        return jsonify({
            "symbol": symbol,
            "interval": interval,
            "signal": "HOLD",
            "confidence": 50,
            "error": str(e)
        }), 500


# =========================================
# 🔥 MULTI COIN (SCANNER - FIXED)
# =========================================
@ai_bp.route("/ai/all", methods=["GET"])
def ai_all():
    try:
        interval = request.args.get("interval", "1m")

        print(f"[AI SCANNER] interval={interval}")

        data = list(db.predictions.find(
            {"interval": interval},
            {"_id": 0}
        ))

        # 🔥 IF DB EMPTY → RETURN DEFAULT COINS
        if not data or len(data) == 0:
            print("⚠️ No DB data, sending fallback coins")

            symbols = [
                "BTCUSDT", "ETHUSDT", "BNBUSDT",
                "SOLUSDT", "XRPUSDT", "ADAUSDT",
                "DOGEUSDT", "AVAXUSDT", "DOTUSDT",
                "MATICUSDT", "LTCUSDT", "LINKUSDT"
            ]

            data = [
                {
                    "symbol": sym,
                    "signal": "HOLD",
                    "confidence": 50
                }
                for sym in symbols
            ]

        # 🔥 SORT BEST FIRST
        data.sort(key=lambda x: x.get("confidence", 0), reverse=True)

        return jsonify(data)

    except Exception as e:
        print("AI ALL ERROR:", str(e))
        return jsonify([])