from pymongo import MongoClient, ReturnDocument
from pymongo.errors import BulkWriteError, DuplicateKeyError
from models import Customer, Account, AccountType, CreateCustomerRequest, CreateAccountRequest

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Repository  (MongoDB database store)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomerRepoMongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.client["bank_api_db"]
        self.customers_collection = self.db["customers"]
        self.counters_collection = self.db["counters"]

    # Only ran once, won't work anymore as original data is added now
    def add_original_data(self):
        customers_original_data = [
            {
                "id": 1,
                "name": "Alice Johnson",
                "accounts": [
                    {"id": 101, "type": "Savings", "balance": 15000.00},
                    {"id": 102, "type": "Checkings", "balance": 3200.50}
                ]
            },
            {
                "id": 2,
                "name": "Bob Smith",
                "accounts": [
                    {"id": 103, "type": "Checkings", "balance": 8750.00}
                ]
            },
            {
                "id": 3,
                "name": "Carol White",
                "accounts": [
                    {"id": 104, "type": "Savings", "balance": 52000.00},
                    {"id": 105, "type": "Savings", "balance": 11500.00}
                ]
            }
        ]

        try:
            result = self.customers_collection.insert_many(customers_original_data)
            print("Original data inserted successfully")
        except BulkWriteError:
            print("Original data already exists. Skipping insert.")

    def get_all_customers(self):
        customers = self.customers_collection.find({}, {"_id": 0})
        #print(customers)
        #print()
        return [Customer(**customer) for customer in customers]

    def get_customer_by_id(self, customer_id: int):
        customer = self.customers_collection.find_one(
            {"id": customer_id},
            {"_id": 0}
        )

        if customer is None:
            return None

        #print(customer)
        return Customer(**customer)
    
    def get_all_accounts(self):
        customers = self.customers_collection.find({}, {"_id": 0, "accounts": 1})
        
        accounts = []
        for customer in customers:
            accounts.extend(customer.get("accounts", []))
        
        #print(accounts)

        return [Account(**account) for account in accounts]

    def get_accounts_by_customer_id(self, customer_id: int):
        customer = self.customers_collection.find_one(
            {"id": customer_id},
            {"_id": 0}
        )

        accounts = customer.get("accounts", [])

        return [Account(**account) for account in accounts]
    
    def add_customer(self, customer_name: str):
        new_customer_id = self.get_next_customer_id()

        new_customer = {
            "id": new_customer_id,
            "name": customer_name,
            "accounts": []
        }

        self.customers_collection.insert_one(new_customer)

        return Customer(**new_customer)
    
    def delete_customer(self, customer_id: int):
        result = self.customers_collection.delete_one(
            {"id": customer_id}
        )

        return result.deleted_count == 1 # customer deleted if condition met
    
    def add_account_to_customer(self, type: AccountType, balance: float, customer_id: int):
        customer = self.get_customer_by_id(customer_id)

        if customer is None: return None

        new_account_id = self.get_next_account_id()
        new_account = {
            "id": new_account_id,
            "type": type,
            "balance": balance
        }

        self.customers_collection.update_one(
            {"id":  customer_id},
            {"$push": {"accounts": new_account}}
        )

        return self.get_customer_by_id(customer_id)
    
    def delete_account(self, account_id: int):
        result = self.customers_collection.update_one(
            {"accounts.id": account_id},
            {"$pull": {"accounts": {"id": account_id}}}
        )

        return result.modified_count == 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # HELPER FUNCTIONS
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_next_customer_id(self):
        counter = self.counters_collection.find_one_and_update(
            {"_id": "customer_id_counter"},
            {"$inc": {"value": 1}},
            return_document=ReturnDocument.BEFORE
        )

        return counter["value"]
    
    def get_next_account_id(self):
        counter = self.counters_collection.find_one_and_update(
            {"_id": "account_id_counter"},
            {"$inc": {"value": 1}},
            return_document=ReturnDocument.BEFORE
        )

        return counter["value"]

# repo = CustomerRepoMongoDB()
# res = repo.add_account_to_customer("Checkings", 12345678, 4)
# print(res)