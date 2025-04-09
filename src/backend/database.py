from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:securepassword123@banktransactioncluster.lx6nlh2.mongodb.net/bank_transcript_scanner?retryWrites=true&w=majority&appName=BankTransactionCluster")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["bank_transcript_scanner"]
daily_totals_collection = db["daily_totals"]

# Test the connection
try:
    client.server_info()
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")