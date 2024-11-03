from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os
import certifi
from datetime import datetime
from bson import ObjectId

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        try:
            uri = os.getenv('MONGODB_URI')
            if not uri:
                uri = "mongodb+srv://AfshanZubia:AkmZubi18018*@hacknjit2024.6ykxs.mongodb.net/?retryWrites=true&w=majority"
            
            self.client = MongoClient(
                uri,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000
            )
            
            self.db = self.client.hacknjit2024
            
            # Create indexes
            self.db.users.create_index([("email", ASCENDING)], unique=True)
            self.db.users.create_index([("username", ASCENDING)], unique=True)
            
            print("✅ Connected to MongoDB!")
            
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            raise e

    async def create_user(self, user_data: dict) -> dict:
        user_data["created_at"] = datetime.utcnow()
        result = self.db.users.insert_one(user_data)
        return {**user_data, "id": str(result.inserted_id)}

    async def get_user_by_email(self, email: str) -> dict:
        return self.db.users.find_one({"email": email})

    async def get_user_by_username(self, username: str) -> dict:
        return self.db.users.find_one({"username": username})

    async def save_generated_image(self, image_data: dict) -> dict:
        image_data["created_at"] = datetime.utcnow()
        result = self.db.images.insert_one(image_data)
        return {**image_data, "id": str(result.inserted_id)}

    async def get_user_images(self, user_id: str) -> list:
        return list(self.db.images.find({"user_id": user_id}))

# Create database instance
db_manager = DatabaseManager()

if __name__ == "__main__":
    # Test the connection
    if db_manager.db is not None:
        try:
            # Try to create a test document
            test_collection = db_manager.db.test
            result = test_collection.insert_one({"test": "connection"})
            print("Successfully wrote to database!")
            # Clean up
            test_collection.delete_one({"_id": result.inserted_id})
        except Exception as e:
            print(f"Error testing database write: {e}")
    else:
        print("Failed to connect to database")

# Example of how to use the database in other files:
from database import db_manager

def example_operations():
    try:
        # Create a new collection
        users = db_manager.db.users
        
        # Create (Insert)
        new_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        result = users.insert_one(new_user)
        print(f"Created user with id: {result.inserted_id}")
        
        # Read (Find)
        user = users.find_one({"email": "test@example.com"})
        print(f"Found user: {user}")
        
        # Update
        users.update_one(
            {"email": "test@example.com"},
            {"$set": {"name": "Updated Name"}}
        )
        
        # Delete
        users.delete_one({"email": "test@example.com"})
        
    except Exception as e:
        print(f"Error: {e}")