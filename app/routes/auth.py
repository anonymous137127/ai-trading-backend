from flask import Blueprint, request, jsonify
from app.database.mongo import users_collection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = users_collection.find_one({
        "username": data["username"],
        "password": data["password"]
    })

    if user:
        return jsonify({
            "status": "success",
            "role": user.get("role", "user")
        })

    return jsonify({"status": "failed"}), 401