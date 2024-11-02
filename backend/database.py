from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "steampunk_app")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]

# Collections
users_collection = db.users
images_collection = db.images
sessions_collection = db.sessions

# Create indexes
users_collection.create_index("email", unique=True)
images_collection.create_index([("user_id", 1), ("created_at", -1)])
sessions_collection.create_index("expires_at", expireAfterSeconds=0)

class DatabaseManager:
    @staticmethod
    async def create_user(user_data: dict) -> dict:
        user_data["created_at"] = datetime.utcnow()
        user_data["images"] = []
        result = users_collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data

    @staticmethod
    async def get_user_by_email(email: str) -> dict:
        return users_collection.find_one({"email": email})

    @staticmethod
    async def get_user_by_id(user_id: str) -> dict:
        return users_collection.find_one({"_id": user_id})

    @staticmethod
    async def store_image(image_data: dict) -> dict:
        image_data["created_at"] = datetime.utcnow()
        result = images_collection.insert_one(image_data)
        image_data["_id"] = result.inserted_id
        
        # Update user's images array
        users_collection.update_one(
            {"_id": image_data["user_id"]},
            {"$push": {"images": str(result.inserted_id)}}
        )
        return image_data

    @staticmethod
    async def get_user_images(user_id: str) -> list:
        return list(images_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1))

    @staticmethod
    async def store_session(session_data: dict) -> dict:
        result = sessions_collection.insert_one(session_data)
        session_data["_id"] = result.inserted_id
        return session_data 
