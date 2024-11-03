from pymongo import MongoClient
import certifi

def test_direct():
    # Direct connection string
    uri = "mongodb+srv://AfshanZubia:AkmZubi18018*@hacknjit2024.6ykxs.mongodb.net/?retryWrites=true&w=majority"
    
    try:
        print("Connecting to MongoDB...")
        client = MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        
        print("Testing connection...")
        client.admin.command('ping')
        print("✅ Connected!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_direct() 