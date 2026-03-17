from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
import os

engine = create_engine('sqlite:///../data/reconciliation.db', echo=True)
Base = declarative_base()

class InternalTransaction(Base):
    __tablename__ = 'internal_ledger' 
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True, nullable=False)
    date = Column(DateTime, nullable=False)
    customer_name = Column(String)
    amount = Column(Float, nullable=False)
    gateway = Column(String)
    status = Column(String, default="Pending")

def init_db():
    print("Connecting to database and building schema...")
    Base.metadata.create_all(engine)
    print("Success! Database schema created.")

if __name__ == "__main__":
    init_db()