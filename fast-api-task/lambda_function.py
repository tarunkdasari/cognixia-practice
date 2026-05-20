import os
import json
import pymongo
from pymongo import MongoClient

MONGO_URI = os.environ["MONGO_URI"]
DB_NAME = os.environ.get("DB_NAME", "bank_api_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
customers_collection = db["customers"]

def lambda_handler(event, context):
    customers = list(customers_collection.find({}, {"_id": 0}))

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(customers)
    }
