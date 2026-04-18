from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import logging

# 🔥 ROUTES
from app.routes.market import market_bp
from app.routes.ai import ai_bp
from app.routes.auth import auth_bp
from app.routes.payment import payment_bp

# 🔥 AI TRAINER
from app.services.ai_trainer import start_ai

# =========================================
# 🚀 INIT APP
# =========================================
app = Flask(__name__)
CORS(app)

# 🔥 SOCKET
socketio = SocketIO(app, cors_allowed_origins="*")

# 🔥 SAVE GLOBAL (IMPORTANT)
app.socketio = socketio

# =========================================
# 📝 LOGGING
# =========================================
logging.basicConfig(level=logging.INFO)

# =========================================
# ROUTES
# =========================================
app.register_blueprint(market_bp, url_prefix="/api")
app.register_blueprint(ai_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(payment_bp, url_prefix="/api")

@app.route("/")
def home():
    return {"message": "🚀 AI Trading Backend Running"}

@app.route("/health")
def health():
    return {"status": "OK"}

# =========================================
# START AI
# =========================================
def start_background():
    start_ai()

# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    print("🚀 Starting AI + WebSocket Server...")

    start_background()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )