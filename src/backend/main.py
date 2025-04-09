from database import transactions_collection

sample = {
    "bank": "ABA",
    "transaction_id": "TX9999",
    "amount": 99.99,
    "date": "2025-04-08"
}

transactions_collection.insert_one(sample)
