# src/backend/models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExtractionResult(BaseModel):
    date: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    # Add other relevant fields

class ValidationError(BaseModel):
    transaction_data: dict
    missing_fields: List[str]

class FileUploadResponse(BaseModel):
    upload_id: str
    message: str

class ProcessingReportResponse(BaseModel):
    total_amount: Optional[float] = None
    extracted_data: List[ExtractionResult]
    validation_errors: List[ValidationError]

class HistoryItem(BaseModel):
    upload_id: str
    upload_date: datetime
    total_files: int
    total_amount: Optional[float]
    validation_errors_count: int