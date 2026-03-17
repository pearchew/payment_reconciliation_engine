# Enterprise FinTech Payment Reconciliation Engine

An automated, state-aware payment reconciliation engine built in Python. This project simulates the real-world financial operations of a FinTech company, matching internal ledger transactions against external bank statements and payment gateway (e.g., Stripe) payouts.

## 🚀 Key Features

* **1-to-1 & Many-to-One Matching:** Capable of matching individual transactions as well as aggregated daily gateway batches.
* **Algorithmic Fee Handling:** Automatically identifies and categorizes legitimate payment gateway fees (e.g., Stripe's 2.9% + $0.30) using NumPy floating-point tolerance (`np.isclose`), separating them from true financial anomalies.
* **Database Persistence & State Management:** Utilizes **SQLite** and **SQLAlchemy (ORM)** to permanently store transactions. The engine reads only "Pending" rows and safely updates them to "Reconciled" upon successful matching, preventing duplicate processing.
* **Automated Reporting:** Generates multi-tab Excel reports using `pandas.ExcelWriter` for Finance and Accounting teams to review discrepancies.
* **Data Generation:** Includes robust mock-data generators using `Faker` to simulate both standard API drops and complex end-of-day batching logic.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Data Engineering:** Pandas, NumPy
* **Database & ORM:** SQLite, SQLAlchemy
* **File I/O:** OpenPyXL (Excel), CSV
* **Mocking:** Faker

## 📂 Project Structure

```text
payment_reconciliation_engine/
│
├── data/                       # Contains all CSVs and the SQLite database
├── notebooks/                  # Jupyter notebooks for data exploration
│   └── test_db.ipynb
├── output/                     # Automated Excel reports drop here
├── src/
│   ├── clean_data.py           # Normalizes and cleans raw financial data
│   ├── database.py             # SQLAlchemy schema and engine setup
│   ├── export.py               # Handles multi-tab Excel generation
│   ├── generate_data.py        # Generates V1 (1-to-1) mock transactions
│   ├── generate_batched_data.py# Generates V2 (Many-to-One) batched payouts
│   ├── reconcile.py            # V1 Engine: Matches 1-to-1 CSVs
│   ├── reconcile_batched.py    # V2 Engine: Matches aggregated batches
│   ├── reconcile_db.py         # V3 Engine: State-aware DB reconciliation
│   └── seed_db.py              # Ingests CSVs into the SQLite database
└── README.md
```

## 🧪 Testing the Engines (Step-by-Step Guide)

This project was built in progressive phases. You can test each engine independently to see how the architecture handles increasing levels of financial complexity.

Ensure your virtual environment is active and you are inside the `src/` directory before running these tests:

### Test 1: V1 Engine (1-to-1 Matching & Excel Export)
*Tests basic row-by-row reconciliation, floating-point fee logic, and automated report generation.*

1. **Generate the raw 1-to-1 transaction data:**
   ```bash
   python generate_data.py
2. ** Run the V1 Engine **
   ```bash
   python reconcile.py
3. Verify: Check the output/ folder in the project root. You will find a multi-tab Excel report categorizing exact matches, valid fees, and missing transactions.

### Test 2: V2 Engine (Many-to-One Batch Matching)
Tests pandas aggregation, groupby logic, and simulating payment gateway daily payouts.

1. **Generate the batched daily transaction data:**
  ```bash
  python generate_batched_data.py

2. ** Run the V2 batched engine **
  ```bash
  python reconcile_batched.py

3. ** Verify: The terminal will output a clear table proving the aggregated internal math perfectly matches the single daily bank deposits. **

---

### Test 3: V3 Engine (Database Persistence & State Management)
*Tests SQLite database creation, SQLAlchemy ORM insertion, and preventing duplicate processing.*

1. **Initialize the empty database schema:**
   ```bash
   python database.py

2. ** Seed the database with "Pending" batched transactions: **
  ```bash
  python seed_db.py

3. ** Run the V3 database engine **
  ```bash
  python reconcile_db.py

3. ** The "Amnesia" Test: Run the exact same engine command a second time: **
  ```bash
  python reconcile_db.py

5. ** Verify: The engine will instantly exit, successfully recognizing that all transactions in the database are already marked as "Reconciled". **