from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URL, MONGO_DATABASE
from typing import List, Optional, Dict
import datetime

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DATABASE]
batches_collection = db["extraction_batches"]
transactions_collection = db["extracted_transactions"]

async def create_extraction_batch(upload_id: str, upload_date: datetime, total_files: int):
    await batches_collection.insert_one({
        "upload_id": upload_id,
        "upload_date": upload_date,
        "total_files": total_files,
        "extraction_summary": {}
    })

async def store_extracted_data(upload_id: str, all_extracted_data: List[Dict], validation_errors: List[Dict]):
    total_amount = 0
    missing_info_count = 0
    stored_transactions_count = 0

    for transaction in all_extracted_data:
        transaction["upload_id"] = upload_id
        await transactions_collection.insert_one(transaction)
        stored_transactions_count += 1
        if transaction.get("amount") is not None and isinstance(transaction["amount"], (int, float)):
            total_amount += transaction["amount"]
        if transaction.get("info") and transaction["info"].get("missing_fields"):
            missing_info_count += 1

    await batches_collection.update_one(
        {"upload_id": upload_id},
        {"$set": {
            "extraction_summary.total_transactions": stored_transactions_count,
            "extraction_summary.total_amount": total_amount,
            "extraction_summary.missing_info_count": missing_info_count,
        }}
    )

async def get_extraction_results(upload_id: str):
    batch = await batches_collection.find_one({"upload_id": upload_id})
    transactions = await transactions_collection.find({"upload_id": upload_id}).to_list(None)
    return {
        "summary": batch.get("extraction_summary", {}) if batch else {},
        "extracted_transactions": transactions,
        "validation_errors": batch.get("validation_errors", []) if batch else [] # Ensure this key exists
    }

async def get_all_extraction_batches() -> List[Dict]:
    history_data = []
    async for batch in batches_collection.find().sort("upload_date", -1):
        total_amount = batch.get("extraction_summary", {}).get("total_amount")
        missing_info_count = batch.get("extraction_summary", {}).get("missing_info_count", 0)
        history_data.append({
            "upload_id": batch.get("upload_id"),
            "upload_date": batch.get("upload_date"),
            "total_files": batch.get("total_files"),
            "total_amount": total_amount,
            "validation_errors_count": missing_info_count,
        })
    return history_data

async def get_transactions_by_upload_id(upload_id: str) -> List[Dict]:
    return await transactions_collection.find({"upload_id": upload_id}).to_list(None)

async def store_zip_file_path(extract_id: str, zip_file_path: str):
    await batches_collection.update_one({"upload_id": extract_id}, {"$set": {"zip_file_path": zip_file_path}})

async def store_report_file_path(extract_id: str, report_file_path: str):
    await batches_collection.update_one({"upload_id": extract_id}, {"$set": {"report_file_path": report_file_path}})