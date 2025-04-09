from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Transaction(BaseModel):
    bank_name: str
    transaction_id: str
    amount: float
    date: datetime
    status: str = "valid"
    
class AuditSummary(BaseModel):
    date: datetime
    total_transactions: int
    total_amount: float
    failed_transactions: List[str]