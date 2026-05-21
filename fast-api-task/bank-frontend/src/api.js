const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  const text = await response.text();
  const data = text ? JSON.parse(text) : null;

  if (!response.ok) {
    const message = data?.detail ?? `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return data;
}

export const bankApi = {
  getCustomers: () => request("/customers/"),
  getAccounts: () => request("/accounts/"),
  getPremiumAccounts: () => request("/accounts/premium"),
  createCustomer: (name) =>
    request("/customers/", {
      method: "POST",
      body: JSON.stringify({ name }),
    }),
  deleteCustomer: (customerId) =>
    request(`/customers/${customerId}`, {
      method: "DELETE",
    }),
  createAccount: (customerId, account) =>
    request(`/accounts/${customerId}`, {
      method: "POST",
      body: JSON.stringify(account),
    }),
  deleteAccount: (accountId) =>
    request(`/accounts/${accountId}`, {
      method: "DELETE",
    }),
};
