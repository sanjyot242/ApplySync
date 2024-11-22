from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv('MONGO_URI')

def test_mongo_connection():
    try:
        # Replace the connection details with your own MongoDB server information
        client = MongoClient(MONGODB_URI)
        db = client["job_tracker"]
        token_collection = db["user_token"]

        # Perform a simple operation to test the connection
        token_collection.insert_one({"test": "Connection successful"})
        print("MongoDB connection successful!")
        # Remove the test document
        token_collection.delete_one({"test": "Connection successful"})

    except Exception as e:
        print("An error occurred while connecting to MongoDB:", str(e))


test_mongo_connection()