from fastapi import FastAPI
from fastapi.testclient import TestClient

from customers import (
    InMemoryCustomerRepository,
    CustomerService,
    create_customer_router,
    create_account_router,
)


def create_test_client():
    repo = InMemoryCustomerRepository()
    service = CustomerService(repo)

    app = FastAPI(title="Test Customers/Accounts API")

    @app.get("/")
    def say_hello():
        return {"message": "hello!"}

    app.include_router(create_customer_router(service))
    app.include_router(create_account_router(service))

    return TestClient(app)


# Tests that the home route returns the hello message
def test_home_route():
    client = create_test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "hello!"}


# Tests that all customers are returned successfully
def test_get_all_customers():
    client = create_test_client()

    response = client.get("/customers/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Alice Johnson"
    assert data[1]["name"] == "Bob Smith"
    assert data[2]["name"] == "Carol White"


# Tests that a customer can be found by a valid customer ID
def test_get_customer_by_id_success():
    client = create_test_client()

    response = client.get("/customers/1")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice Johnson"
    assert len(data["accounts"]) == 2


# Tests that the API returns 404 when customer ID does not exist
def test_get_customer_by_id_not_found():
    client = create_test_client()

    response = client.get("/customers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "ERROR: Customer 999 not found"


# Tests that accounts for a specific customer are returned successfully
def test_get_accounts_by_customer_id_success():
    client = create_test_client()

    response = client.get("/customers/1/accounts")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == 101
    assert data[1]["id"] == 102


# Tests that the API returns 404 when getting accounts for a non-existing customer
def test_get_accounts_by_customer_id_not_found():
    client = create_test_client()

    response = client.get("/customers/999/accounts")

    assert response.status_code == 404
    assert response.json()["detail"] == "ERROR: Customer 999 not found"


# Tests that all accounts across all customers are returned successfully
def test_get_all_accounts():
    client = create_test_client()

    response = client.get("/accounts/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 5
    assert data[0]["id"] == 101
    assert data[0]["type"] == "Savings"


# Tests that premium accounts with balance greater than 10000 are returned
# NOTE: Your current route is spelled "/preimum" in customers.py
def test_get_premium_accounts():
    client = create_test_client()

    response = client.get("/accounts/preimum")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3

    account_ids = [account["id"] for account in data]
    assert account_ids == [101, 104, 105]


# Tests that a new customer can be created successfully
def test_create_customer_success():
    client = create_test_client()

    response = client.post(
        "/customers/",
        json={"name": "David Lee"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 4
    assert data["name"] == "David Lee"
    assert data["accounts"] == []


# Tests that creating a customer also increases the total customer count
def test_create_customer_increases_customer_count():
    client = create_test_client()

    create_response = client.post(
        "/customers/",
        json={"name": "David Lee"}
    )

    assert create_response.status_code == 200

    get_response = client.get("/customers/")

    assert get_response.status_code == 200

    data = get_response.json()
    assert len(data) == 4
    assert data[-1]["name"] == "David Lee"


# Tests that creating a customer with an empty name returns 400
def test_create_customer_empty_name():
    client = create_test_client()

    response = client.post(
        "/customers/",
        json={"name": "   "}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Customer name cannot be empty"


# Tests that a new account can be added to an existing customer
# NOTE: Your current endpoint returns the updated Customer, not just the new Account
def test_add_account_to_customer_success():
    client = create_test_client()

    response = client.post(
        "/accounts/1",
        json={
            "type": "Savings",
            "balance": 5000
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice Johnson"
    assert len(data["accounts"]) == 3

    new_account = data["accounts"][-1]
    assert new_account["id"] == 106
    assert new_account["type"] == "Savings"
    assert new_account["balance"] == 5000


# Tests that adding an account with a negative balance returns 400
def test_add_account_negative_balance():
    client = create_test_client()

    response = client.post(
        "/accounts/1",
        json={
            "type": "Checkings",
            "balance": -100
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Account balance cannot be negative"


# Tests that adding an account to a non-existing customer returns 404
def test_add_account_customer_not_found():
    client = create_test_client()

    response = client.post(
        "/accounts/999",
        json={
            "type": "Savings",
            "balance": 5000
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer 999 not found"


# Tests that an existing customer can be deleted successfully
def test_delete_customer_success():
    client = create_test_client()

    response = client.delete("/customers/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Customer 1 deleted successfully"}


# Tests that deleting a customer removes that customer from the customer list
def test_delete_customer_removes_customer_from_list():
    client = create_test_client()

    delete_response = client.delete("/customers/1")

    assert delete_response.status_code == 200

    get_response = client.get("/customers/")

    assert get_response.status_code == 200

    data = get_response.json()
    customer_ids = [customer["id"] for customer in data]

    assert len(data) == 2
    assert 1 not in customer_ids


# Tests that deleting a non-existing customer returns 404
def test_delete_customer_not_found():
    client = create_test_client()

    response = client.delete("/customers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer 999 not found"


# Tests that an existing account can be deleted successfully
def test_delete_account_success():
    client = create_test_client()

    response = client.delete("/accounts/101")

    assert response.status_code == 200
    assert response.json() == {"message": "Account 101 deleted successfully"}


# Tests that deleting an account removes that account from the full account list
def test_delete_account_removes_account_from_list():
    client = create_test_client()

    delete_response = client.delete("/accounts/101")

    assert delete_response.status_code == 200

    get_response = client.get("/accounts/")

    assert get_response.status_code == 200

    data = get_response.json()
    account_ids = [account["id"] for account in data]

    assert len(data) == 4
    assert 101 not in account_ids


# Tests that deleting a non-existing account returns 404
def test_delete_account_not_found():
    client = create_test_client()

    response = client.delete("/accounts/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Account 999 not found"