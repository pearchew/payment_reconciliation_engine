import pandas as pd
import numpy as np

def run_batched_reconciliation():
    print("--- Starting V2 Engine: Batched Reconciliation ---")
    internal_df = pd.read_csv('../data/Batched_Internal_Ledger.csv')
    bank_df = pd.read_csv('../data/Batched_Bank_Statement.csv')
    internal_df['Date'] = pd.to_datetime(internal_df['Date'])
    bank_df['Settlement_Date'] = pd.to_datetime(bank_df['Settlement_Date'])
    
    print("Aggregating internal transactions by day...")
    internal_df['Date'] = internal_df['Date'].dt.date
    
    internal_daily = internal_df.groupby('Date').agg(
        Total_Gross_Amount=('Amount', 'sum'),
        Transaction_Count=('Amount', 'count')
    ).reset_index()
    
    expected_fees = (internal_daily['Total_Gross_Amount'] * 0.029) + (internal_daily['Transaction_Count'] * 0.30)
    internal_daily['Expected_Settlement'] = round(internal_daily['Total_Gross_Amount'] - expected_fees, 2)
    
    internal_daily['Expected_Settlement_Date'] = pd.to_datetime(internal_daily['Date']) + pd.to_timedelta(2, unit='D')

    # Matching
    print("Matching expected batches against actual bank deposits...")
    batched_match = pd.merge(
        internal_daily,
        bank_df,
        left_on='Expected_Settlement_Date',
        right_on='Settlement_Date',
        how='left' 
    )
    
    # Validation
    batched_match['Is_Perfect_Match'] = np.isclose(
        batched_match['Expected_Settlement'], 
        batched_match['Total_Settled_Amount'], 
        atol=0.01
    )
    print("\n--- Final Batched Reconciliation Report ---")
    
    display_cols = ['Date', 'Total_Gross_Amount', 'Expected_Settlement', 'Total_Settled_Amount', 'Is_Perfect_Match']
    print(batched_match[display_cols].to_string(index=False))
    
    return batched_match

if __name__ == "__main__":
    run_batched_reconciliation()