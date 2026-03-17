import pandas as pd
from sqlalchemy.orm import sessionmaker
from database import engine, InternalTransaction

def seed_database():
    print("--- Starting Database Seeding ---")

    # 1. THE SESSION: Open the waiting room -> We bind the session to the engine we created in database.py
    Session = sessionmaker(bind=engine)
    session = Session()

    # 2. INGEST THE CSV -> We are using the V2 batched internal ledger data here
    csv_path = "../data/Batched_Internal_Ledger.csv"
    df = pd.read_csv(csv_path)
    
    print(f"Found {len(df)} records. Preparing for insertion...")

    # 3. TRANSLATE CSV ROWS INTO PYTHON OBJECTS
    records_to_insert = []
    for index, row in df.iterrows():
        # Notice we are using the exact class we defined in database.py!
        db_record = InternalTransaction(
            transaction_id=row['Transaction_ID'],
            date=pd.to_datetime(row['Date']), # Ensure it's a real datetime object
            customer_name=row['Customer_Name'],
            amount=row['Amount'],
            gateway=row['Gateway']
            # We DO NOT need to pass 'id' (it auto-generates) or 'status' (it defaults to 'Pending')
        )
        records_to_insert.append(db_record)

    # 4. BULK INSERT AND COMMIT
    # Put all 5,000 records into the session waiting room at once
    session.add_all(records_to_insert)
    
    try:
        print("Executing SQL INSERT transaction...")
        # Permanently write to the database file
        session.commit()
        print("Success! Data securely committed to the database.")
    except Exception as e:
        # The safety net: If anything violates our schema rules, abort!
        session.rollback()
        print(f"Database Error! Transaction rolled back to protect data integrity.\nError: {e}")
    finally:
        # Always close the connection when you are done to free up memory
        session.close()

if __name__ == "__main__":
    seed_database()