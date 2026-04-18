from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ai_trading"]

users_collection = db["users"]
subscriptions_collection = db["subscriptions"]
predictions_collection = db["predictions"]