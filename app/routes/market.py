from flask import Blueprint, request, jsonify
import requests

market_bp = Blueprint("market", __name__)

@market_bp.route("/market")
def get_market():
    symbol = request.args.get("symbol", "BTCUSDT")
    interval = request.args.get("interval", "1m")

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 300
    }

    res = requests.get(url, params=params).json()

    data = []
    for c in res:
        data.append({
            "time": int(c[0]),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        })

    return jsonify(data)