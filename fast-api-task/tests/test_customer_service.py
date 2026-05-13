import pytest
from fastapi import HTTPException

# Implement and practice TDD in current project
# Test Service layer methods in API
# Test Controllers

from customers import CustomerRepository, CustomerService, AccountType

@pytest.fixture
def service():
    repo = CustomerRepository()
    return CustomerService(repo)

# Example 1: test getting all customers
def test_get_all_customers(service):
    customers = service.get_all_customers()

    assert len(customers) == 3
    assert customers[0].name == "Alice Johnson"
    assert customers[1].name == "Bob Smith"
    assert customers[2].name == "Carol White"

# Example 2: test getting customer by ID
def test_get_customer_by_id_success(service):
    customer = service.get_customer_by_id(1)

    assert customer.id == 1
    assert customer.name == "Alice Johnson"
    assert len(customer.accounts) == 2

# Example 3: test customer not found
def test_get_customer_by_id_not_found(service):
    with pytest.raises(HTTPException) as exc_info:
        service.get_customer_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ERROR: Customer 999 not found"

# Example 4: test adding a customer
def test_add_customer_success(service):
    customer = service.add_customer("David Lee")

    assert customer.id == 4
    assert customer.name == "David Lee"
    assert customer.accounts == []

    all_customers = service.get_all_customers()
    assert len(all_customers) == 4

# Example 5: test empty customer name
def test_add_customer_empty_name(service):
    with pytest.raises(HTTPException) as exc_info:
        service.add_customer("   ")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Customer name cannot be empty"

# Example 6: test getting all accounts
def test_get_all_accounts(service):
    accounts = service.get_all_accounts()

    assert len(accounts) == 5
    assert accounts[0].id == 101
    assert accounts[0].type == AccountType.SAVINGS

# Example 7: test premium accounts
def test_get_premium_accounts(service):
    premium_accounts = service.get_premium_account()

    assert len(premium_accounts) == 3

    premium_ids = [account.id for account in premium_accounts]
    assert premium_ids == [101, 104, 105]

# Example 8: test adding account to customer
def test_add_account_to_customer_success(service):
    updated_customer = service.add_account_to_customer(
        AccountType.SAVINGS,
        5000,
        1
    )

    assert updated_customer.id == 1
    assert len(updated_customer.accounts) == 3

    new_account = updated_customer.accounts[-1]
    assert new_account.id == 106
    assert new_account.type == AccountType.SAVINGS
    assert new_account.balance == 5000

# Example 9: test negative balance
def test_add_account_negative_balance(service):
    with pytest.raises(HTTPException) as exc_info:
        service.add_account_to_customer(
            AccountType.CHECKINGS,
            -100,
            1
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Account balance cannot be negative"

# Example 10: test deleting customer
def test_delete_customer_success(service):
    result = service.delete_customer(1)

    assert result == {"message": "Customer 1 deleted successfully"}

    customers = service.get_all_customers()
    assert len(customers) == 2