from flask import Blueprint, jsonify

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/payment-status", methods=["GET"])
def payment_status():
    return jsonify({"status": "Payment system ready"})