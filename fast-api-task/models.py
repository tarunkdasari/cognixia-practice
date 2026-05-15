from pydantic import BaseModel
from enum import Enum
from typing import List

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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