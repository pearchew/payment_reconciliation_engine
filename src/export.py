import pandas as pd
import os
from datetime import datetime

def generate_excel_report(pass_1, pass_2, missing_internal, missing_bank):
    print("\n--- Starting Engine: Phase 5 (Exporting to Excel) ---")
    
    os.makedirs("../output", exist_ok=True)
    
    today_str = datetime.now().strftime("%Y%m%d")
    file_path = f"../output/Reconciliation_Report_{today_str}.xlsx"
    
    print(f"Writing data to {file_path}...")
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pass_1.to_excel(writer, sheet_name='1_Reconciled_Exact', index=False)
        pass_2.to_excel(writer, sheet_name='2_Fee_Discrepancies', index=False)
        missing_internal.to_excel(writer, sheet_name='3_Missing_Internally', index=False)
        missing_bank.to_excel(writer, sheet_name='4_Missing_in_Bank', index=False)
        
    print("Success!")