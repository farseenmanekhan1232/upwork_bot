from pymongo import MongoClient
from config import Config
from bson.objectid import ObjectId

# Initialize MongoDB client
client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DB]
alerts_collection = db["alerts"]

def add_alert(user_id, filters):
    """Add an alert with user preferences."""
    alert = {
        "user_id": user_id,
        "filters": filters,
    }
    alerts_collection.insert_one(alert)

def list_alerts(user_id):
    """List all alerts for a user."""
    return list(alerts_collection.find({"user_id": user_id}))

def delete_alert(alert_id):
    """Delete an alert by ID."""
    alerts_collection.delete_one({"_id": ObjectId(alert_id)})
