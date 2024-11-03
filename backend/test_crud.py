from database import db

def test_crud():
    try:
        # Test collection
        collection = db.test_crud
        
        print("Testing CRUD operations...")
        
        # Create
        print("\nTesting Create:")
        result = collection.insert_one({"test": "data"})
        print(f"✅ Created document with id: {result.inserted_id}")
        
        # Read
        print("\nTesting Read:")
        doc = collection.find_one({"test": "data"})
        print(f"✅ Found document: {doc}")
        
        # Update
        print("\nTesting Update:")
        collection.update_one(
            {"test": "data"},
            {"$set": {"test": "updated"}}
        )
        updated_doc = collection.find_one({"test": "updated"})
        print(f"✅ Updated document: {updated_doc}")
        
        # Delete
        print("\nTesting Delete:")
        collection.delete_one({"test": "updated"})
        print("✅ Deleted document")
        
        print("\n✅ All operations successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_crud() 