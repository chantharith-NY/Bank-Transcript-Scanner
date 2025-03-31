from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    file_paths = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(file_path)
    
    # Simulate OCR + Classification + Extraction
    extracted_data = [
        {"bank_name": "ABA Bank", "transaction_id": "TX12345", "date": "2024-03-31", "amount": 100.50, "status": "Complete"},
        {"bank_name": "National Bank", "transaction_id": "TX67890", "date": "2024-03-30", "amount": 200.75, "status": "Missing Data"},
    ]

    for data in extracted_data:
        db_transaction = Transaction(**data)
        db.add(db_transaction)
    
    db.commit()

    return {
        "message": "Files uploaded and processed",
        "total_amount": sum(t["amount"] for t in extracted_data),
        "total_transcripts": len(extracted_data),
        "total_missing_info": sum(1 for t in extracted_data if t["status"] == "Missing Data"),
        "missing_info_transcripts": [t for t in extracted_data if t["status"] == "Missing Data"]
    }
