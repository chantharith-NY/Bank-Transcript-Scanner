from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from typing import List
import uuid
from datetime import datetime
import zipfile
import os
import json
import csv
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
from io import BytesIO
import pandas as pd

from .backend.database import create_extraction_batch, store_extracted_data, get_extraction_results, get_all_extraction_batches, store_zip_file_path, store_report_file_path, get_transactions_by_upload_id
from .backend.models import FileUploadResponse, ExtractionResult, ValidationError, ProcessingReportResponse, HistoryItem, Transaction
from .backend.bank_classifier import classify_bank as classify_bank_module
from .backend.preprocess import preprocess_image
from .extraction.extract_data import extract_data as extract_data_module
from .extraction.validation import validate_data as validate_data_module
from .backend.routes import router

app = FastAPI(
    title="Bank Transaction Scanner",
    description="API for extracting, validation, and storing bank transaction data.",
    version="1.0.0"
)

TEMP_UPLOAD_DIR = "temp_uploads"
TEMP_PROCESS_DIR = "temp_processing"
TEMP_ZIP_DIR = "temp_zip"
TEMP_REPORTS_DIR = "temp_reports"

os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_PROCESS_DIR, exist_ok=True)
os.makedirs(TEMP_ZIP_DIR, exist_ok=True)
os.makedirs(TEMP_REPORTS_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def classify_bank(image_path: str) -> str:
    try:
        bank_name = classify_bank_module(image_path)
        return bank_name
    except Exception as e:
        print(f"Error classifying bank: {e}")
        return None

async def extract_data(image: np.ndarray, bank_name: str = None) -> List[dict]:
    try:
        extracted_transactions = extract_data_module(image, bank_name)
        return extracted_transactions
    except Exception as e:
        print(f"Error during data extraction (bank: {bank_name}): {e}")
        return []

async def validate_data(extracted_transactions: List[dict]) -> tuple[List[ExtractionResult], List[ValidationError]]:
    try:
        valid_transactions, errors = validate_data_module(extracted_transactions)
        return [ExtractionResult(**item) for item in valid_transactions], [ValidationError(transaction_data=err["transaction_data"], missing_fields=err["missing_fields"]) for err in errors]
    except Exception as e:
        print(f"Error during data validation: {e}")
        return [], []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bank Transaction Scanner API!"}

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(files: List[UploadFile] = File(...)):
    upload_id = str(uuid.uuid4())
    upload_date = datetime.now()
    total_files = len(files)
    await create_extraction_batch(upload_id, upload_date, total_files)
    extracted_data_all = []
    validation_errors_all = []

    for file in files:
        file_type = file.content_type
        file_name = file.filename
        upload_file_path = os.path.join(TEMP_UPLOAD_DIR, file_name)

        try:
            with open(upload_file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            bank_name = None
            processed_image = None

            if "image" in file_type:
                processed_image = preprocess_image(upload_file_path)
                bank_name = await classify_bank(upload_file_path)
                print(f"Classified bank for {file_name}: {bank_name}")
                extracted_transactions = await extract_data(processed_image, bank_name)
                valid_transactions, errors = await validate_data(extracted_transactions)
                extracted_data_all.extend(valid_transactions)
                validation_errors_all.extend(errors)

            elif file_type == "application/pdf":
                try:
                    images_from_pdf = convert_from_path(upload_file_path)
                    print(f"Converted PDF {file_name} to {len(images_from_pdf)} images.")
                    for i, image in enumerate(images_from_pdf):
                        intermediate_image_name = f"{file_name}_page_{i+1}.png"
                        intermediate_image_path = os.path.join(TEMP_PROCESS_DIR, intermediate_image_name)
                        image.save(intermediate_image_path, 'PNG')
                        preprocessed_image = preprocess_image(intermediate_image_path)
                        if i == 0:
                            bank_name = await classify_bank(intermediate_image_path)
                            print(f"Classified bank for PDF {file_name} (page 1): {bank_name}")
                        extracted_transactions = await extract_data(preprocessed_image, bank_name)
                        valid_transactions, errors = await validate_data(extracted_transactions)
                        extracted_data_all.extend(valid_transactions)
                        validation_errors_all.extend(errors)
                        os.remove(intermediate_image_path)
                except Exception as e:
                    print(f"Error processing PDF {file_name}: {e}")
            else:
                print(f"Unsupported file type: {file_type} for {file_name}")
                continue

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
        finally:
            if os.path.exists(upload_file_path):
                os.remove(upload_file_path)

    # Convert ExtractionResult and ValidationError objects to dictionaries before storing
    serialized_extracted_data = [item.model_dump() for item in extracted_data_all]
    serialized_validation_errors = [item.model_dump() for item in validation_errors_all]

    await store_extracted_data(upload_id, serialized_extracted_data, serialized_validation_errors)

    # Fetch the extraction results to include in the response
    results = await get_extraction_results(upload_id)
    summary = results.get("summary", {})
    extracted_transactions = results.get("extracted_transactions", [])

    # Prepare transaction info for the response (just missing info for brevity)
    transaction_info_list = []
    for txn in extracted_transactions:
        missing = txn.get("info", {}).get("missing_fields", [])
        transaction_info_list.append({
            "transaction_id": txn.get("transaction_id"),
            "date": txn.get("date"),
            "amount": txn.get("amount"),
            "missing_fields": missing
        })

    return {
        "upload_id": upload_id,
        "message": "Files processed successfully.",
        "upload_date": upload_date,
        "total_files": total_files,
        "total_amount": summary.get("total_amount"),
        "missing_info_count": summary.get("missing_info_count"),
        "transaction_info": transaction_info_list[:5] # Limit to a few for the response
    }

@app.get("/results/{upload_id}", response_model=ProcessingReportResponse)
async def get_results(upload_id: str):
    """
    Retrieves the processing results for a specific upload ID.
    """
    results = await get_extraction_results(upload_id)
    print(f"DEBUG: get_extraction_results output: {results}")
    if results:
        return ProcessingReportResponse(
            summary=results.get("summary"),
            extracted_transactions=[Transaction(**item) for item in results.get("extracted_transactions", [])],
        )
    else:
        return ProcessingReportResponse(
            summary=None,
            extracted_transactions=[],
        )

@app.get("/history", response_model=List[HistoryItem])
async def get_history():
    history_data = await get_all_extraction_batches()
    return history_data

@app.get("/transactions/{upload_id}", response_model=List[Transaction])
async def read_transactions(upload_id: str):
    """
    Retrieves all transaction details for a specific upload ID.
    """
    transactions = await get_transactions_by_upload_id(upload_id)
    if transactions:
        return [Transaction(**item) for item in transactions]
    else:
        raise HTTPException(status_code=404, detail="Transactions not found for this upload ID")

@app.get("/download/{extract_id}")
async def download_zip(extract_id: str):
    results = await get_extraction_results(extract_id)
    if not results:
        raise HTTPException(status_code=404, detail="Extraction results not found")

    extracted_data = results.get("extracted_transactions", [])
    zip_filename = f"extracted_data_{extract_id}.zip"
    zip_path = os.path.join(TEMP_ZIP_DIR, zip_filename)
    os.makedirs(TEMP_ZIP_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            data_json = json.dumps(extracted_data, indent=4)
            zipf.writestr(f"extracted_data_{extract_id}.json", data_json)

        await store_zip_file_path(extract_id, zip_path)
        return FileResponse(path=zip_path, filename=zip_filename, media_type="application/zip")
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        raise HTTPException(status_code=500, detail="Error creating ZIP file")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

@app.get("/download/excel/{extract_id}")
async def download_excel(extract_id: str):
    results = await get_extraction_results(extract_id)
    if not results or not results.get("extracted_transactions"):
        raise HTTPException(status_code=404, detail="Extraction results not found")

    df = pd.DataFrame(results["extracted_transactions"])
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Extracted Data")
    excel_file.seek(0)

    headers = {
        'Content-Disposition': f'attachment; filename="extracted_data_{extract_id}.xlsx"',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }
    return StreamingResponse(excel_file, headers=headers)

@app.get("/download/csv/{extract_id}")
async def download_csv(extract_id: str):
    results = await get_extraction_results(extract_id)
    if not results or not results.get("extracted_transactions"):
        raise HTTPException(status_code=404, detail="Extraction results not found")

    df = pd.DataFrame(results["extracted_transactions"])
    csv_file = BytesIO()
    df.to_csv(csv_file, index=False, encoding="utf-8")
    csv_file.seek(0)

    headers = {
        'Content-Disposition': f'attachment; filename="extracted_data_{extract_id}.csv"',
        'Content-Type': 'text/csv; charset=utf-8',
    }
    return StreamingResponse(csv_file, headers=headers)

app.include_router(router)