from sqlalchemy import Column, Integer, String, Float
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, index=True)
    transaction_id = Column(String, unique=True, index=True)
    date = Column(String)
    amount = Column(Float)
    status = Column(String)  # "Complete" or "Missing Data"
