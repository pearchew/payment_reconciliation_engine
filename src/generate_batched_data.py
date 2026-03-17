import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()
Faker.seed(100)
np.random.seed(100)
random.seed(100)

def generate_batched_data(num_records=5000):
    print(f"Generating {num_records} internal ledger records...")
    
    internal_data = []
    for _ in range(num_records):
        internal_data.append({
            "Transaction_ID": fake.uuid4()[:16].upper(),
            "Date": fake.date_time_between(start_date="-5d", end_date="now").replace(microsecond=0),
            "Customer_Name": fake.name(),
            "Amount": round(random.uniform(15.0, 150.0), 2),
            "Gateway": "Stripe"
        })
    
    internal_df = pd.DataFrame(internal_data)

    print("Simulating end-of-day gateway batching...")
    
    internal_df['Date'] = pd.to_datetime(internal_df['Date']).dt.date
    
    daily_batches = internal_df.groupby('Date').agg(
        Total_Gross_Amount=('Amount', 'sum'),
        Transaction_Count=('Amount', 'count')
    ).reset_index()
    
    daily_batches['Total_Fees'] = (daily_batches['Total_Gross_Amount'] * 0.029) + (daily_batches['Transaction_Count'] * 0.30)
    daily_batches['Total_Settled_Amount'] = round(daily_batches['Total_Gross_Amount'] - daily_batches['Total_Fees'], 2)
    

    bank_df = pd.DataFrame({
        "Settlement_Date": pd.to_datetime(daily_batches['Date']) + pd.to_timedelta(2, unit='D'),
        "Description": "STRIPE PAYOUT",
        "Total_Settled_Amount": daily_batches['Total_Settled_Amount']
    })

    os.makedirs('../data', exist_ok=True)
    internal_df.to_csv('../data/Batched_Internal_Ledger.csv', index=False)
    bank_df.to_csv('../data/Batched_Bank_Statement.csv', index=False)
    
    print("Success! Batched data generated.")
    print(f"\nSneak Peek - Bank Statement:\n{bank_df.head()}")

if __name__ == "__main__":
    generate_batched_data()