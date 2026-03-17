import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
from database import engine, InternalTransaction

def run_db_reconciliation():
    print("--- Starting V3 Engine: Database-Backed Reconciliation ---")
    
    # 1. THE SESSION: Connect to the database
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Fetching 'Pending' transactions...")
    pending_records = session.query(InternalTransaction).filter_by(status='Pending').all()
    
    if not pending_records:
        print("No pending transactions found! The books are perfectly balanced.")
        session.close()
        return

    # Convert the SQLAlchemy database objects into a Pandas DataFrame for the math engine
    # list of dictionaries, where each dictionary corresponds to a row in the database table, and the keys of the dictionary correspond to the column names in the database.
    internal_data = [{
        'transaction_id': r.transaction_id,
        'date': r.date,
        'amount': r.amount
    } for r in pending_records]
    
    internal_df = pd.DataFrame(internal_data)

    # Match
    bank_df = pd.read_csv('../data/Batched_Bank_Statement.csv')
    bank_df['Settlement_Date'] = pd.to_datetime(bank_df['Settlement_Date'])
    
    # Group our pending internal DB records by day
    internal_df['Just_Date'] = pd.to_datetime(internal_df['date']).dt.date
    daily_batches = internal_df.groupby('Just_Date').agg(
        Total_Gross_Amount=('amount', 'sum'),
        Transaction_Count=('amount', 'count')
    ).reset_index()
    
    # Calculate expected Stripe payout and T+2 settlement date
    expected_fees = (daily_batches['Total_Gross_Amount'] * 0.029) + (daily_batches['Transaction_Count'] * 0.30)
    daily_batches['Expected_Settlement'] = round(daily_batches['Total_Gross_Amount'] - expected_fees, 2)
    daily_batches['Expected_Settlement_Date'] = pd.to_datetime(daily_batches['Just_Date']) + pd.to_timedelta(2, unit='D')

    # Join with the bank
    matched = pd.merge(
        daily_batches, bank_df,
        left_on='Expected_Settlement_Date', right_on='Settlement_Date', how='inner'
    )
    
    # Verify the pennies
    matched['Is_Perfect_Match'] = np.isclose(matched['Expected_Settlement'], matched['Total_Settled_Amount'], atol=0.01)
    
    # Find which dates were successfully matched
    successful_dates = matched[matched['Is_Perfect_Match'] == True]['Just_Date'].tolist()
    print(f"Successfully matched batches for {len(successful_dates)} days.")

    # Write back to database: For every batch that was successfully matched, we want to mark all the individual transactions that belong to that batch as "Reconciled" in our database.
    if successful_dates:
        print("Updating database: Changing status from 'Pending' to 'Reconciled'...")
        
        # We find all original transactions whose dates belong to the successfully matched batches
        # We use a trick to extract the date from the database datetime column to match our successful_dates
        records_to_update = session.query(InternalTransaction).filter(InternalTransaction.status == 'Pending').all()
        
        updated_count = 0
        for record in records_to_update:
            # If this record's date falls on a day that the bank successfully paid us for
            if record.date.date() in successful_dates:
                record.status = 'Reconciled' # Simply change the Python object attribute!
                updated_count += 1
                
        # Commit the massive update to the hard drive
        session.commit()
        print(f"Success! Permanently marked {updated_count} individual transactions as 'Reconciled'.")
    
    # Always close the session
    session.close()

if __name__ == "__main__":
    run_db_reconciliation()