import { useEffect, useMemo, useState } from "react";
import { bankApi } from "./api.js";

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

function formatCurrency(value) {
  return currencyFormatter.format(Number(value ?? 0));
}

function getInitialAccountForm(customers) {
  return {
    customerId: customers[0]?.id?.toString() ?? "",
    type: "Savings",
    balance: "",
  };
}

export default function App() {
  const [customers, setCustomers] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [premiumAccounts, setPremiumAccounts] = useState([]);
  const [selectedCustomerId, setSelectedCustomerId] = useState(null);
  const [customerName, setCustomerName] = useState("");
  const [accountForm, setAccountForm] = useState(getInitialAccountForm([]));
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const selectedCustomer = useMemo(
    () => customers.find((customer) => customer.id === selectedCustomerId) ?? customers[0],
    [customers, selectedCustomerId]
  );

  const totalBalance = useMemo(
    () => accounts.reduce((sum, account) => sum + Number(account.balance), 0),
    [accounts]
  );

  const selectedAccounts = selectedCustomer?.accounts ?? [];
  const checkingCount = selectedAccounts.filter((account) => account.type === "Checkings").length;
  const savingsCount = selectedAccounts.filter((account) => account.type === "Savings").length;

  async function loadDashboard(showSpinner = true) {
    if (showSpinner) {
      setLoading(true);
    }

    setError("");
    try {
      const [customerData, accountData, premiumData] = await Promise.all([
        bankApi.getCustomers(),
        bankApi.getAccounts(),
        bankApi.getPremiumAccounts(),
      ]);

      setCustomers(customerData);
      setAccounts(accountData);
      setPremiumAccounts(premiumData);
      setSelectedCustomerId((currentId) => {
        if (customerData.some((customer) => customer.id === currentId)) {
          return currentId;
        }
        return customerData[0]?.id ?? null;
      });
      setAccountForm((currentForm) => ({
        ...currentForm,
        customerId: currentForm.customerId || customerData[0]?.id?.toString() || "",
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  async function handleCreateCustomer(event) {
    event.preventDefault();
    setSaving(true);
    setNotice("");
    setError("");

    try {
      const created = await bankApi.createCustomer(customerName);
      setCustomerName("");
      setNotice(`Created customer ${created.name}.`);
      await loadDashboard(false);
      setSelectedCustomerId(created.id);
      setAccountForm((currentForm) => ({ ...currentForm, customerId: created.id.toString() }));
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleCreateAccount(event) {
    event.preventDefault();
    setSaving(true);
    setNotice("");
    setError("");

    try {
      const customerId = Number(accountForm.customerId);
      await bankApi.createAccount(customerId, {
        type: accountForm.type,
        balance: Number(accountForm.balance),
      });
      setNotice(`Added a ${accountForm.type.toLowerCase()} account.`);
      setAccountForm((currentForm) => ({ ...currentForm, balance: "" }));
      await loadDashboard(false);
      setSelectedCustomerId(customerId);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteCustomer(customerId) {
    setSaving(true);
    setNotice("");
    setError("");

    try {
      await bankApi.deleteCustomer(customerId);
      setNotice(`Deleted customer ${customerId}.`);
      await loadDashboard(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteAccount(accountId) {
    setSaving(true);
    setNotice("");
    setError("");

    try {
      await bankApi.deleteAccount(accountId);
      setNotice(`Deleted account ${accountId}.`);
      await loadDashboard(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">FastAPI bank service</p>
          <h1>Bank API Dashboard</h1>
          <p className="hero-copy">
            Manage customers and accounts from the FastAPI backend, with live totals and premium account visibility.
          </p>
        </div>
        <button className="ghost-button" type="button" onClick={() => loadDashboard()} disabled={loading || saving}>
          Refresh
        </button>
      </section>

      {error && <div className="alert error">{error}</div>}
      {notice && <div className="alert success">{notice}</div>}

      <section className="stats-grid" aria-label="Bank totals">
        <Stat label="Customers" value={customers.length} />
        <Stat label="Accounts" value={accounts.length} />
        <Stat label="Total deposits" value={formatCurrency(totalBalance)} />
        <Stat label="Premium accounts" value={premiumAccounts.length} />
      </section>

      <section className="workspace">
        <aside className="panel customer-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Customers</p>
              <h2>Portfolio</h2>
            </div>
            {loading && <span className="status-pill">Loading</span>}
          </div>

          <div className="customer-list">
            {customers.map((customer) => (
              <button
                className={`customer-row ${selectedCustomer?.id === customer.id ? "active" : ""}`}
                key={customer.id}
                type="button"
                onClick={() => setSelectedCustomerId(customer.id)}
              >
                <span>
                  <strong>{customer.name}</strong>
                  <small>Customer #{customer.id}</small>
                </span>
                <span>{customer.accounts.length}</span>
              </button>
            ))}
          </div>

          <form className="stack-form" onSubmit={handleCreateCustomer}>
            <label htmlFor="customerName">New customer</label>
            <div className="inline-form">
              <input
                id="customerName"
                value={customerName}
                onChange={(event) => setCustomerName(event.target.value)}
                placeholder="Customer name"
                disabled={saving}
              />
              <button type="submit" disabled={saving || !customerName.trim()}>
                Add
              </button>
            </div>
          </form>
        </aside>

        <section className="panel detail-panel">
          {selectedCustomer ? (
            <>
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Customer detail</p>
                  <h2>{selectedCustomer.name}</h2>
                </div>
                <button
                  className="danger-button"
                  type="button"
                  onClick={() => handleDeleteCustomer(selectedCustomer.id)}
                  disabled={saving}
                >
                  Delete customer
                </button>
              </div>

              <div className="account-summary">
                <Stat label="Savings" value={savingsCount} />
                <Stat label="Checkings" value={checkingCount} />
                <Stat
                  label="Customer balance"
                  value={formatCurrency(
                    selectedCustomer.accounts.reduce((sum, account) => sum + Number(account.balance), 0)
                  )}
                />
              </div>

              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Account</th>
                      <th>Type</th>
                      <th>Balance</th>
                      <th aria-label="Actions" />
                    </tr>
                  </thead>
                  <tbody>
                    {selectedCustomer.accounts.map((account) => (
                      <tr key={account.id}>
                        <td>#{account.id}</td>
                        <td>{account.type}</td>
                        <td>{formatCurrency(account.balance)}</td>
                        <td>
                          <button
                            className="link-button"
                            type="button"
                            onClick={() => handleDeleteAccount(account.id)}
                            disabled={saving}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                    {selectedCustomer.accounts.length === 0 && (
                      <tr>
                        <td colSpan="4" className="empty-cell">
                          No accounts yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="empty-state">Create a customer to begin.</div>
          )}
        </section>
      </section>

      <section className="bottom-grid">
        <form className="panel stack-form" onSubmit={handleCreateAccount}>
          <div>
            <p className="eyebrow">Accounts</p>
            <h2>Add account</h2>
          </div>
          <label htmlFor="accountCustomer">Customer</label>
          <select
            id="accountCustomer"
            value={accountForm.customerId}
            onChange={(event) => setAccountForm({ ...accountForm, customerId: event.target.value })}
            disabled={saving || customers.length === 0}
          >
            {customers.map((customer) => (
              <option key={customer.id} value={customer.id}>
                {customer.name}
              </option>
            ))}
          </select>

          <label htmlFor="accountType">Account type</label>
          <select
            id="accountType"
            value={accountForm.type}
            onChange={(event) => setAccountForm({ ...accountForm, type: event.target.value })}
            disabled={saving}
          >
            <option value="Savings">Savings</option>
            <option value="Checkings">Checkings</option>
          </select>

          <label htmlFor="accountBalance">Starting balance</label>
          <input
            id="accountBalance"
            type="number"
            min="0"
            step="0.01"
            value={accountForm.balance}
            onChange={(event) => setAccountForm({ ...accountForm, balance: event.target.value })}
            placeholder="0.00"
            disabled={saving}
          />

          <button type="submit" disabled={saving || !accountForm.customerId || accountForm.balance === ""}>
            Add account
          </button>
        </form>

        <section className="panel">
          <div>
            <p className="eyebrow">Premium</p>
            <h2>Balances over $10,000</h2>
          </div>
          <div className="premium-list">
            {premiumAccounts.map((account) => (
              <div className="premium-row" key={account.id}>
                <span>#{account.id}</span>
                <strong>{formatCurrency(account.balance)}</strong>
                <small>{account.type}</small>
              </div>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

function Stat({ label, value }) {
  return (
    <div className="stat">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
