# Bank API Frontend

React dashboard for the FastAPI customer/account service in the parent folder.

## Run it locally

1. Start the FastAPI app from `fast-api-task`.

   ```powershell
   uvicorn customers:app --reload
   ```

2. Install frontend dependencies.

   ```powershell
   cd bank-frontend
   npm install
   ```

3. Start the React development server.

   ```powershell
   npm run dev
   ```

The frontend expects the API at `http://127.0.0.1:8000`. To point it somewhere else, create a `.env` file in this folder:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```
