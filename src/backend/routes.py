from fastapi import APIRouter
from models import Transaction, AuditSummary
from database import transactions_collection, summary_collection

router = APIRouter()

@router.post("/transactions")
def save_transaction(transaction: Transaction):
    result = transactions_collection.insert_one(transaction.dict())
    return {"transaction_id": str(result.inserted_id)}

@router.post("/summary")
def save_summary(summary: AuditSummary):
    result = summary_collection.insert_one(summary.dict())
    return {"summary_id": str(result.inserted_id)}

@router.get("/transactions")
def get_transactions():
    return list(transactions_collection.find({}, {"_id": 0}))