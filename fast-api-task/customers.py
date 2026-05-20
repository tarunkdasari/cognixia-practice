from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Customer, Account, AccountType, CreateCustomerRequest, CreateAccountRequest
from customer_repo import CustomerRepoMongoDB
from typing import List

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Repository  (in-memory data store)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class InMemoryCustomerRepository:
    def __init__(self):
        self.customer_id_counter = 4
        self.account_id_counter = 106
        self.customers: List[Customer] = [
            Customer(
                id=1,
                name="Alice Johnson",
                accounts=[
                    Account(id=101, type=AccountType.SAVINGS,   balance=15000.00),
                    Account(id=102, type=AccountType.CHECKINGS, balance=3200.50),
                ],
            ),
            Customer(
                id=2,
                name="Bob Smith",
                accounts=[
                    Account(id=103, type=AccountType.CHECKINGS, balance=8750.00),
                ],
            ),
            Customer(
                id=3,
                name="Carol White",
                accounts=[
                    Account(id=104, type=AccountType.SAVINGS,   balance=52000.00),
                    Account(id=105, type=AccountType.SAVINGS,   balance=11500.00),
                ],
            ),
        ]
    
    def get_all_customers(self):
        return self.customers
    
    def get_customer_by_id(self, customer_id: int):
        
        for customer in self.customers:
            if customer.id == customer_id:
                return customer

        return None
    
    def get_all_accounts(self):
        accounts = []

        for customer in self.customers:
            accounts.extend(customer.accounts)

        return accounts
    
    def get_accounts_by_customer_id(self, customer_id: int):

        for customer in self.customers:
            if customer.id == customer_id:
                return customer.accounts
            
        return None
    
    # NEW
    def add_customer(self, customer_name: str):
        new_customer = Customer(id=self.customer_id_counter, name=customer_name)
        self.customer_id_counter += 1
        self.customers.append(new_customer)
        return new_customer
    
    # NEW
    def delete_customer(self, customer_id: int):
        for i, customer in enumerate(self.customers):
            if customer.id == customer_id:
                self.customers.pop(i)
                return True
            
        return False
    
    # NEW
    def add_account_to_customer(self, type: AccountType, balance: float, customer_id: int):
        customer = self.get_customer_by_id(customer_id)
        if customer is None:
            return None
        
        new_account = Account(id=self.account_id_counter, type=type, balance=balance)
        self.account_id_counter += 1
        customer.accounts.append(new_account)

        return customer # change back to new_account if needed 
    
    # NEW
    def delete_account(self, account_id: int):
        for customer in self.customers:
            for i, account in enumerate(customer.accounts):
                if account.id == account_id:
                    customer.accounts.pop(i)
                    return True
        
        return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Service  (Business Logic)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CustomerService:
    def __init__(self, repo):
        self.repo = repo

    def get_all_customers(self):
        return self.repo.get_all_customers()

    def get_customer_by_id(self, customer_id: int):
        customer = self.repo.get_customer_by_id(customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail=f"ERROR: Customer {customer_id} not found")
        return customer

    def get_all_accounts(self):
        return self.repo.get_all_accounts()
    
    def get_accounts_by_customer_id(self, customer_id: int):
        accounts = self.repo.get_accounts_by_customer_id(customer_id)
        if accounts is None:
            raise HTTPException(status_code=404, detail=f"ERROR: Customer {customer_id} not found")
        return accounts

    def get_premium_account(self):
        premium_accounts = []
        accounts = self.repo.get_all_accounts()
        for account in accounts:
            if account.balance > 10000:
                premium_accounts.append(account)

        return premium_accounts
    
    # NEW
    def add_customer(self, customer_name: str):
        if customer_name is None or len(customer_name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Customer name cannot be empty")
        
        return self.repo.add_customer(customer_name.strip())
    
    # NEW
    def delete_customer(self, customer_id: int):
        # if method returns none, it means customer doesn't exist
        if not self.repo.delete_customer(customer_id):
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        
        return {"message": f"Customer {customer_id} deleted successfully"}

    # NEW
    def add_account_to_customer(self, type: AccountType, balance: float, customer_id: int):
        if balance < 0:
            raise HTTPException(status_code=400, detail="Account balance cannot be negative")
        
        new_account = self.repo.add_account_to_customer(type, balance, customer_id)
        if new_account is None: # none returned if customer doesn't exist
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        return new_account
    
    # NEW
    def delete_account(self, account_id: int):
        if not self.repo.delete_account(account_id):
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")

        return {"message": f"Account {account_id} deleted successfully"}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Controllers  (routers)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_customer_router(service: CustomerService) -> APIRouter:
    router = APIRouter(prefix="/customers", tags=["Customers"])

    @router.get("/", response_model=List[Customer])
    def get_all_customers():
        return service.get_all_customers()

    @router.get("/{customer_id}", response_model=Customer)
    def get_customer_by_id(customer_id: int):
        return service.get_customer_by_id(customer_id)

    @router.get("/{customer_id}/accounts", response_model=List[Account])
    def get_accounts_by_customer_id(customer_id: int):
        return service.get_accounts_by_customer_id(customer_id)
    
    # NEW
    @router.post("/", response_model=Customer)
    def add_customer(req: CreateCustomerRequest):
        return service.add_customer(req.name)
    
    # NEW
    @router.delete("/{customer_id}")
    def delete_customer(customer_id: int):
        return service.delete_customer(customer_id)

    return router    
    
def create_account_router(service: CustomerService) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["Accounts"])

    @router.get("/", response_model=List[Account])
    def get_all_accounts():
        return service.get_all_accounts()
    
    @router.get("/premium", response_model=List[Account])
    def get_premium_account():
        return service.get_premium_account()
    
    # NEW
    @router.post("/{customer_id}", response_model=Customer)
    def add_account(req: CreateAccountRequest, customer_id: int,):
        return service.add_account_to_customer(req.type, req.balance, customer_id)

    # NEW
    @router.delete("/{account_id}")
    def delete_account(account_id: int):
        return service.delete_account(account_id)

    return router

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# App bootstrap
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class LazyCustomerRepository:
    def __init__(self):
        self._repo = None

    def _get_repo(self):
        if self._repo is None:
            self._repo = CustomerRepoMongoDB()
        return self._repo

    def __getattr__(self, name):
        return getattr(self._get_repo(), name)


repo = LazyCustomerRepository()
service = CustomerService(repo)

app = FastAPI(title="Customers/Accounts API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def say_hello():
    return {"message": "hello!"}

app.include_router(create_customer_router(service))
app.include_router(create_account_router(service))
