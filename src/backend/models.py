from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class TransactionInfo(BaseModel):
    missing_fields: Optional[List[str]] = None
    blur_reason: Optional[str] = None
    # Add other potential info fields

class Transaction(BaseModel):
    id: Optional[str] = None # MongoDB's _id will be a string
    upload_id: str
    transaction_id: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    info: Optional[TransactionInfo] = None # Default to empty info
    # Add other transaction fields

class ExtractionResult(BaseModel):
    date: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    # Add other relevant fields that are part of the *initial* extraction

class ValidationError(BaseModel):
    transaction_data: dict
    missing_fields: List[str]

class FileUploadResponse(BaseModel):
    upload_id: str
    message: str
    upload_date: Optional[datetime] = None
    total_files: Optional[int] = None
    total_amount: Optional[Dict[str, float]] = None  # <-- Accepts dict by currency
    missing_info_count: Optional[int] = None
    transaction_info: Optional[List[Dict]] = None

class ProcessingReportResponse(BaseModel):
    summary: Optional[Dict] = None
    extracted_transactions: List[Transaction]

class HistoryItem(BaseModel):
    upload_id: str
    upload_date: datetime
    total_files: int
    total_amount: Optional[Dict[str, float]] = None
    validation_errors_count: int