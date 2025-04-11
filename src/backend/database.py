from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URL, MONGO_DATABASE
from typing import List, Optional, Dict
import datetime

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DATABASE]
collection = db["extraction_batches"]

async def create_extraction_batch(upload_id: str, upload_date: datetime, total_files: int):
    await collection.insert_one({"upload_id": upload_id, "upload_date": upload_date, "total_files": total_files})

async def store_extracted_data(upload_id: str, extracted_data: List[Dict], validation_errors: List[Dict]):
    await collection.update_one(
        {"upload_id": upload_id},
        {"$set": {"extracted_data": extracted_data, "validation_errors": validation_errors}}
    )

async def get_extraction_results(upload_id: str):
    batch = await collection.find_one({"upload_id": upload_id})
    if batch:
        return {
            "extracted_data": batch.get("extracted_data", []),
            "validation_errors": batch.get("validation_errors", []),
            "total_amount": sum(item.get("amount", 0) for item in batch.get("extracted_data", []) if isinstance(item.get("amount"), (int, float))),
        }
    return None

async def get_all_extraction_batches() -> List[Dict]:
    history_data = []
    async for batch in collection.find().sort("upload_date", -1):
        total_amount = 0
        files_with_errors = 0
        extracted_data_for_batch = batch.get("extracted_data", [])
        validation_errors_for_batch = batch.get("validation_errors", [])
        processed_files = set()

        if extracted_data_for_batch:
            total_amount = sum(item.get("amount", 0) for item in extracted_data_for_batch if isinstance(item.get("amount"), (int, float)))

        if validation_errors_for_batch:
            for error in validation_errors_for_batch:
                file_identifier = error.get("file_name") or error.get("source")
                if file_identifier:
                    processed_files.add(file_identifier)
                elif error.get("transaction_data"):
                    pass

            files_with_errors = len(processed_files)

        history_data.append({
            "upload_id": batch.get("upload_id"),
            "upload_date": batch.get("upload_date"),
            "total_files": batch.get("total_files"),
            "total_amount": total_amount,
            "validation_errors_count": files_with_errors,
        })
    return history_data

async def store_zip_file_path(extract_id: str, zip_file_path: str):
    await collection.update_one({"upload_id": extract_id}, {"$set": {"zip_file_path": zip_file_path}})

async def store_report_file_path(extract_id: str, report_file_path: str):
    await collection.update_one({"upload_id": extract_id}, {"$set": {"report_file_path": report_file_path}})