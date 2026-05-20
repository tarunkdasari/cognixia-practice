import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

load_dotenv()

mongo_uri = os.getenv("MONGO_ATLAS_URI")

if not mongo_uri:
    raise ValueError("MONGO_ATLAS_URI not found in .env file")

client = MongoClient(mongo_uri)

db = client["bank_api_db"]
customers_collection = db["customers"]
counters_collection = db["counters"]

# Create unique index so customer IDs cannot duplicate
customers_collection.create_index("id", unique=True)

customers = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "accounts": [
            {"id": 101, "type": "Savings", "balance": 15000.00},
            {"id": 102, "type": "Checkings", "balance": 3200.50},
        ],
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "accounts": [
            {"id": 103, "type": "Checkings", "balance": 8750.00},
        ],
    },
    {
        "id": 3,
        "name": "Carol White",
        "accounts": [
            {"id": 104, "type": "Savings", "balance": 52000.00},
            {"id": 105, "type": "Savings", "balance": 11500.00},
        ],
    },
]

counters = [
    {"_id": "customer_id_counter", "value": 4},
    {"_id": "account_id_counter", "value": 106},
]

try:
    customers_collection.insert_many(customers)
    print("Customers inserted successfully.")
except BulkWriteError:
    print("Customers already exist or duplicate ID found. Skipping customers insert.")

for counter in counters:
    counters_collection.update_one(
        {"_id": counter["_id"]},
        {"$setOnInsert": counter},
        upsert=True
    )

print("Counters inserted/verified successfully.")
print("Atlas seed complete.")