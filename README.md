# 🏦 Automated Payment Reconciliation Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Advanced-150458.svg)
![FinTech](https://img.shields.io/badge/Domain-FinTech-00C7B7.svg)

## 📌 Project Overview
Millions of dollars are lost annually across the FinTech sector due to payment gateway glitches, double-charges, and hidden fees. This project is a robust **Automated Payment Reconciliation Engine** built in Python. 

It simulates the "financial plumbing" of a modern FinTech company by automatically matching thousands of rows of transactional data between an internal ledger and an external bank statement. By intelligently categorizing discrepancies, catching hidden fee leaks, and outputting clean reports, this engine demonstrates how to automate critical finance operations.

## 🚀 Features
* **Mock Data Generation**: Simulates realistic financial datasets with built-in anomalies (missing rows, T+1/T+2 settlement delays, and fee deductions).
* **Data Normalization**: Cleans and standardizes messy text, currency strings, and timestamps.
* **Multi-Pass Matching Logic**:
  * *Pass 1*: Exact matching on Transaction IDs and Amounts.
  * *Pass 2*: Fuzzy matching handling rolling 3-day settlement windows.
* **Exception Handling**: Automatically detects known payment gateway fee structures (e.g., Stripe's 2.9% + $0.30) to distinguish between genuine errors and standard operational costs.
* **Automated Excel Reporting**: Generates a multi-tab, color-coded Excel report for Finance/Ops teams separating transactions into `Reconciled`, `Missing in Bank`, `Missing Internally`, and `Fee Discrepancies`.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Manipulation:** `pandas`, `numpy`
* **File Export:** `openpyxl` / `xlsxwriter`
* **Data Generation:** `Faker` (for realistic customer names/IDs)

## 📂 Project Structure
```text
├── data/
│   ├── Internal_Ledger.csv       # Generated internal app data
│   ├── Bank_Statement.csv        # Generated external bank data
├── output/                       # Generated Excel reports
├── src/
│   ├── generate_data.py          # Script to create mock datasets
│   ├── clean_data.py             # Data normalization functions
│   ├── reconcile.py              # Core pandas matching logic
│   └── export.py                 # Excel formatting and output logic
├── main.py                       # Entry point to run the pipeline
├── requirements.txt              # Python dependencies
└── README.md