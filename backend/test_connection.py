from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import certifi

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        return None

def test_connection():
    # Use direct URI first
    uri = "mongodb+srv://AfshanZubia:AkmZubi18018*@hacknjit2024.6ykxs.mongodb.net/?retryWrites=true&w=majority"
    
    # Print IP information
    print(f"Local IP: 10.196.16.207")
    public_ip = get_public_ip()
    if public_ip:
        print(f"Public IP: {public_ip}")
    
    try:
        print("\nTesting MongoDB connection...")
        client = MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        
        # Test connection
        print("Pinging database...")
        client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        
        # Test write operation
        print("Testing write operation...")
        db = client.hacknjit2024
        result = db.test.insert_one({"test": "connection"})
        print("✅ Write successful!")
        
        # Cleanup
        db.test.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup successful!")
        
        # Now test environment variable
        env_uri = os.getenv('MONGODB_URI')
        if env_uri == uri:
            print("\n✅ Environment variable matches direct URI")
        else:
            print("\n❌ Environment variable mismatch!")
            print(f"Expected: {uri}")
            print(f"Got from env: {env_uri}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv(verbose=True)  # Added verbose flag
    test_connection() 