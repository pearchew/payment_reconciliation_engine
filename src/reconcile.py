import pandas as pd
from clean_data import load_and_clean_data
import numpy as np

from export import generate_excel_report

def run_reconciliation():
    internal_csv = "../data/Internal_Ledger.csv"
    bank_csv = "../data/Bank_Statement.csv"
    internal_df, bank_df = load_and_clean_data(internal_csv, bank_csv)
    print("\n--- Starting Engine: Pass 1 (Exact Matches) ---")
    
    pass_1_matches = pd.merge(
        internal_df, 
        bank_df, 
        left_on=['Transaction_ID', 'Amount'], 
        right_on=['Transaction_ID', 'Settled_Amount'], 
        how='inner'
    )
    print(f"Pass 1: Found {len(pass_1_matches)} exact matches.")
    unmatched_internal = internal_df[~internal_df['Transaction_ID'].isin(pass_1_matches['Transaction_ID'])].copy()
    unmatched_bank = bank_df[~bank_df['Transaction_ID'].isin(pass_1_matches['Transaction_ID'])].copy()
    print(f"Leftovers to investigate -> Internal: {len(unmatched_internal)} | Bank: {len(unmatched_bank)}\n")
    
    print("--- Starting Engine: Pass 2 (Fuzzy Matches) ---")
    
    pass_2_matches = pd.merge(
        unmatched_internal,
        unmatched_bank,
        on='Transaction_ID',
        how='inner'
    )
    pass_2_matches['Delay_Days'] = (pass_2_matches['Settlement_Date'] - pass_2_matches['Date']).dt.days

    print(f"Pass 2: Found {len(pass_2_matches)} transactions with matching IDs but different amounts.")
    
    final_missing_internal = unmatched_internal[~unmatched_internal['Transaction_ID'].isin(pass_2_matches['Transaction_ID'])].copy()
    final_missing_bank = unmatched_bank[~unmatched_bank['Transaction_ID'].isin(pass_2_matches['Transaction_ID'])].copy()
    
    print(f"Final Missing -> Internal (Failed/Dropped API): {len(final_missing_internal)}")
    print(f"Final Missing -> Bank (Ghosts/Manual Deposits): {len(final_missing_bank)}\n")
    
    print("--- Starting Engine: Phase 4 (Exception Handling) ---")
    expected_fee = (pass_2_matches['Amount'] * 0.029) + 0.30
    pass_2_matches['Expected_Settlement'] = pass_2_matches['Amount'] - expected_fee
    is_stripe_fee = np.isclose(
        pass_2_matches['Settled_Amount'], 
        pass_2_matches['Expected_Settlement'], 
        atol=0.01
    )
    
    pass_2_matches['Discrepancy_Reason'] = np.where(
        is_stripe_fee, 
        "Valid Stripe Fee", 
        "Unknown Discrepancy"
    )
    
    valid_fees = pass_2_matches[pass_2_matches['Discrepancy_Reason'] == "Valid Stripe Fee"]
    unknowns = pass_2_matches[pass_2_matches['Discrepancy_Reason'] == "Unknown Discrepancy"]
    
    print(f"Fee Engine: Automatically verified {len(valid_fees)} valid Stripe fees.")
    print(f"Fee Engine: Found {len(unknowns)} truly unknown discrepancies.\n")
    
    
    return pass_1_matches, pass_2_matches, final_missing_internal, final_missing_bank

if __name__ == "__main__":
    p1, p2, missing_int, missing_bank = run_reconciliation()
    generate_excel_report(p1, p2, missing_int, missing_bank)