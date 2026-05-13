from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


# ─────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────

class AccountType(str, Enum):
    SAVINGS = "Savings"
    CHECKINGS = "Checkings"


class Account(BaseModel):
    id: int
    type: AccountType
    balance: float


class Customer(BaseModel):
    id: int
    name: str
    accounts: List[Account] = []


class CreateCustomerRequest(BaseModel):
    name: str


class CreateAccountRequest(BaseModel):
    type: AccountType
    balance: float


# ─────────────────────────────────────────────
# Repository  (in-memory data store)
# ─────────────────────────────────────────────

class CustomerRepository:
    def __init__(self):
        self._customer_id_counter = 4
        self._account_id_counter = 106
        self._customers: List[Customer] = [
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

    def get_all_customers(self) -> List[Customer]:
        return self._customers

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return next((c for c in self._customers if c.id == customer_id), None)

    def get_all_accounts(self) -> List[Account]:
        return [account for customer in self._customers for account in customer.accounts]

    def get_accounts_by_customer_id(self, customer_id: int) -> Optional[List[Account]]:
        customer = self.get_customer_by_id(customer_id)
        if customer is None:
            return None
        return customer.accounts

    def add_customer(self, name: str) -> Customer:
        new_customer = Customer(id=self._customer_id_counter, name=name, accounts=[])
        self._customer_id_counter += 1
        self._customers.append(new_customer)
        return new_customer

    def delete_customer(self, customer_id: int) -> bool:
        for i, customer in enumerate(self._customers):
            if customer.id == customer_id:
                self._customers.pop(i)
                return True
        return False

    def add_account_to_customer(self, customer_id: int, account_type: AccountType, balance: float) -> Optional[Account]:
        customer = self.get_customer_by_id(customer_id)
        if customer is None:
            return None
        new_account = Account(id=self._account_id_counter, type=account_type, balance=balance)
        self._account_id_counter += 1
        customer.accounts.append(new_account)
        return new_account

    def delete_account(self, account_id: int) -> bool:
        for customer in self._customers:
            for i, account in enumerate(customer.accounts):
                if account.id == account_id:
                    customer.accounts.pop(i)
                    return True
        return False


# ─────────────────────────────────────────────
# Service  (business logic)
# ─────────────────────────────────────────────

class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self._repo = repo

    def get_all_customers(self) -> List[Customer]:
        return self._repo.get_all_customers()

    def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = self._repo.get_customer_by_id(customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return customer

    def get_all_accounts(self) -> List[Account]:
        return self._repo.get_all_accounts()

    def get_accounts_by_customer_id(self, customer_id: int) -> List[Account]:
        accounts = self._repo.get_accounts_by_customer_id(customer_id)
        if accounts is None:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return accounts

    def get_premium_accounts(self) -> List[Account]:
        return [a for a in self._repo.get_all_accounts() if a.balance > 10_000]

    def add_customer(self, name: str) -> Customer:
        if not name or len(name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Customer name cannot be empty")
        return self._repo.add_customer(name.strip())

    def delete_customer(self, customer_id: int) -> dict:
        if not self._repo.delete_customer(customer_id):
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return {"message": f"Customer {customer_id} deleted successfully"}

    def add_account_to_customer(self, customer_id: int, account_type: AccountType, balance: float) -> Account:
        if balance < 0:
            raise HTTPException(status_code=400, detail="Account balance cannot be negative")
        account = self._repo.add_account_to_customer(customer_id, account_type, balance)
        if account is None:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        return account

    def delete_account(self, account_id: int) -> dict:
        if not self._repo.delete_account(account_id):
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
        return {"message": f"Account {account_id} deleted successfully"}


# ─────────────────────────────────────────────
# Controllers  (routers)
# ─────────────────────────────────────────────

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

    @router.post("/", response_model=Customer)
    def add_customer(req: CreateCustomerRequest):
        return service.add_customer(req.name)

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
    def get_premium_accounts():
        return service.get_premium_accounts()

    @router.post("/{customer_id}", response_model=Account)
    def add_account_to_customer(customer_id: int, req: CreateAccountRequest):
        return service.add_account_to_customer(customer_id, req.type, req.balance)

    @router.delete("/{account_id}")
    def delete_account(account_id: int):
        return service.delete_account(account_id)

    return router


# ─────────────────────────────────────────────
# App bootstrap
# ─────────────────────────────────────────────

repo    = CustomerRepository()
service = CustomerService(repo)

app = FastAPI(title="Customers API")
app.include_router(create_customer_router(service))
app.include_router(create_account_router(service))
