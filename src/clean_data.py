import pandas as pd

def load_and_clean_data(internal_path, bank_path):
    print("Loading datasets...")
    # 1. Ingest the raw data
    internal_df = pd.read_csv(internal_path)
    bank_df = pd.read_csv(bank_path)

    print("Cleaning Internal Ledger...")
    # 2. Clean Internal Ledger
    # Standardize strings: Remove sneaky whitespaces and force uppercase
    internal_df['Transaction_ID'] = internal_df['Transaction_ID'].str.strip().str.upper()
    internal_df['Customer_Name'] = internal_df['Customer_Name'].str.strip().str.upper()
    
    # Standardize dates: Convert the string dates from the CSV back into actual Pandas Datetime objects
    internal_df['Date'] = pd.to_datetime(internal_df['Date'])
    
    # Ensure amounts are strict floats (decimals)
    internal_df['Amount'] = internal_df['Amount'].astype(float)

    print("Cleaning Bank Statement...")
    # 3. Clean Bank Statement
    # We apply the exact same string rules here so they match perfectly later
    bank_df['Transaction_ID'] = bank_df['Transaction_ID'].str.strip().str.upper()
    bank_df['Customer_Name'] = bank_df['Customer_Name'].str.strip().str.upper()
    
    bank_df['Settlement_Date'] = pd.to_datetime(bank_df['Settlement_Date'])
    bank_df['Settled_Amount'] = bank_df['Settled_Amount'].astype(float)

    print("Data cleaning complete!")
    return internal_df, bank_df

if __name__ == "__main__":
    internal_csv = "../data/Internal_Ledger.csv"
    bank_csv = "../data/Bank_Statement.csv"
    
    clean_internal, clean_bank = load_and_clean_data(internal_csv, bank_csv)
    
    # Let's peek at the cleaned data types to prove it worked
    print("\nInternal Ledger Data Types:")
    print(clean_internal.dtypes)
    print("\nBank Statement Data Types:")
    print(clean_bank.dtypes)