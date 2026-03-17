

import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

def generate_mock_data(num_records=1000):
    print(f"Generating {num_records} internal ledger records...")
    internal_data = []
    for _ in range(num_records):
        internal_data.append({
            "Transaction_ID": fake.uuid4()[:16].upper(),
            "Date": fake.date_time_between(start_date="-30d", end_date="now").replace(microsecond=0),
            "Customer_Name": fake.name(),
            "Amount": round(random.uniform(10.0, 500.0), 2),
            "Status": "Processed"
        })
    internal_df = pd.DataFrame(internal_data)
    
    print(f"Generating {num_records} bank statement anomalies")
    bank_df = internal_df.copy()

    delay_days = np.random.randint(1, 4, size=num_records)
    bank_df['Settlement_Date'] = bank_df['Date'] + pd.to_timedelta(delay_days, unit='D')
    bank_df = bank_df.drop(columns=['Date', 'Status'])
    bank_df.rename(columns={'Amount': 'Settled_Amount'}, inplace=True)
    
    fee_mask = np.random.rand(num_records) < 0.30 
    bank_df.loc[fee_mask, 'Settled_Amount'] = round(bank_df['Settled_Amount'] * (1 - 0.029) - 0.30, 2)
    
    drop_indices = bank_df.sample(frac=0.02, random_state=42).index
    bank_df = bank_df.drop(drop_indices)
    
    ghost_data = []
    for _ in range(5):
        ghost_data.append({
            "Transaction_ID": fake.uuid4()[:16].upper(),
            "Customer_Name": fake.name().upper(), 
            "Settled_Amount": round(random.uniform(10.0, 100.0), 2),
            "Settlement_Date": fake.date_time_between(start_date="-10d", end_date="now").replace(microsecond=0)
        })
    
    bank_df = pd.concat([bank_df, pd.DataFrame(ghost_data)], ignore_index=True)
    internal_df.to_csv('../data/Internal_Ledger.csv', index=False)
    bank_df.to_csv('../data/Bank_Statement.csv', index=False)
    
    print("Success! Data generated and saved to the 'data' folder.")
    
    os.makedirs('../data', exist_ok=True)

if __name__ == "__main__":
    generate_mock_data()
    
    