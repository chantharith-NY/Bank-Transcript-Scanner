# extract_data.py
import re
from typing import List, Dict, Optional
import pytesseract
import numpy as np
from PIL import Image

def extract_data_aba(image: np.ndarray, debug: bool = False) -> List[Dict]:
    extracted_transactions = []
    try:
        # Perform OCR on the image
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='eng')
        if debug:
            print("\n--- OCR OUTPUT START ---\n" + extracted_text + "\n--- OCR OUTPUT END ---\n")
            with open("/tmp/aba_ocr_debug.txt", "w") as f:
                f.write(extracted_text)

        # More robust regex patterns (tolerate OCR errors)
        id_pattern = re.compile(r"Tr[xr][. ]?\s*ID[:：]?\s*([0-9Il]{6,})", re.IGNORECASE)
        amount_pattern = re.compile(r"([-]?\d{1,3}(?:[.,]\d{3})*[.,]\d{2})\s*(USD|KHR)", re.IGNORECASE)
        date_pattern = re.compile(r"Transaction date[:：]?\s*([A-Za-z]{3}\s+\d{1,2},\s+\d{4})\s+(\d{1,2}:\d{2}\s*(?:AM|PM))", re.IGNORECASE)
        
        lines = extracted_text.splitlines()
        transaction: Dict[str, Optional[str | float | dict]] = {}
        for i, line in enumerate(lines):
            # --- Transaction ID extraction (robust, like ACLEDA) ---
            trx_id_match = re.search(r"(?:Tr[xr][. ]?\s*ID|Transaction ID|Original amount|លេខកូដប្រតិបត្តិការ)[:：]?\s*([\wIl]+)", line)
            if not trx_id_match and i + 1 < len(lines):
                trx_id_match = re.search(r"(?:Tr[xr][. ]?\s*ID|Transaction ID|Original amount|លេខកូដប្រតិបត្តិការ)[:：]?\s*([\wIl]+)", lines[i+1])
            if trx_id_match:
                transaction['transaction_id'] = trx_id_match.group(1).replace('I', '1').replace('l', '1')

            # --- Date extraction (same as before) ---
            date_time_match = date_pattern.search(line)
            if not date_time_match and i + 1 < len(lines):
                date_time_match = date_pattern.search(lines[i+1])
            if date_time_match:
                transaction['date'] = date_time_match.group(1)
                transaction['time'] = date_time_match.group(2)

            # --- Amount and currency extraction (same as before) ---
            amount_match = amount_pattern.search(line)
            if amount_match:
                amount_str = amount_match.group(1).replace(",", "").replace(".", ".")
                currency = amount_match.group(2)
                try:
                    transaction['amount'] = float(amount_str.replace(',', ''))
                    transaction['currency'] = currency
                except ValueError:
                    if debug:
                        print(f"Error converting amount: {amount_str}")

            # Description (example)
            if "WANG XINMIN" in line and not transaction.get('description'):
                transaction['description'] = "Payment to WANG XINMIN"

            # Only append if all required fields
            if transaction.get('transaction_id') and transaction.get('date') and transaction.get('amount'):
                extracted_transactions.append(transaction.copy())
                transaction = {}

        if not extracted_transactions:
            print(f"Could not extract any transactions from ABA statement (OCR text):\n{extracted_text[:400]}...")

    except pytesseract.TesseractError as e:
        print(f"Tesseract OCR error (ABA): {e}")
    except Exception as e:
        print(f"Error during OCR or extraction (ABA): {e}")
    return extracted_transactions

def extract_data_aclida(image: np.ndarray) -> List[Dict]:
    extracted_transactions = []
    try:
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='eng')
        lines = extracted_text.splitlines()

        transaction: Dict[str, Optional[str | float | dict]] = {}
        for line in lines:
            # --- Transaction ID extraction for ACLEDA ---
            # Try to extract transaction_id from lines with Khmer or English labels
            trx_id_match = re.search(r"(?:លេខកូដប្រតិបត្តិការ|Transaction ID|Trx\. ID|Original amount)[:：]?\s*(\w+)", line)
            if trx_id_match:
                transaction['transaction_id'] = trx_id_match.group(1)

            amount_match = re.search(r"Payment Amount\s*:\s*([-]?\d{1,3}(?:,\d{3})*\.\d{2})\s*([UK])", line)
            if amount_match:
                amount_str = amount_match.group(1).replace(",", "")
                currency_code = amount_match.group(2)
                currency = 'USD' if currency_code == 'U' else 'KHR' if currency_code == 'K' else ''
                try:
                    transaction['amount'] = float(amount_str)
                    transaction['currency'] = currency
                except ValueError:
                    print(f"Error converting amount: {amount_str}")

            datetime_match = re.search(r"Date\s*:\s*(\w{3}\s+\d{1,2},\s+\d{4})\s+(\d{2}:\d{2}\s*(?:AM|PM))", line)
            if datetime_match:
                transaction['date'] = datetime_match.group(1)
                transaction['time'] = datetime_match.group(2)

            completed_ref_match = re.search(r"Completed\s*:\s*Ref\.\s*(\S+)", line)
            if completed_ref_match:
                transaction['completed_ref'] = completed_ref_match.group(1)

            external_txn_ref_match = re.search(r"External Txn Ref\s*:\s*(\S+)", line)
            if external_txn_ref_match:
                transaction['external_txn_ref'] = external_txn_ref_match.group(1)

            description_match = re.search(r"Description\s*:\s*(.+)", line) # Example - adjust
            if description_match:
                transaction['description'] = description_match.group(1).strip()

            # Only append if transaction_id, amount, and date are present
            if transaction.get('transaction_id') and transaction.get('amount') and transaction.get('date'):
                info: Dict[str, Optional[List[str]]] = {}
                if not transaction.get('date'):
                    info.setdefault('missing_fields', []).append('date')
                if transaction.get('amount') is None:
                    info.setdefault('missing_fields', []).append('amount')
                if not transaction.get('currency'):
                    info.setdefault('missing_fields', []).append('currency')
                if not transaction.get('description'):
                    info.setdefault('missing_fields', []).append('description')
                if info:
                    transaction['info'] = info
                extracted_transactions.append(transaction.copy())
                transaction = {}

        if not extracted_transactions:
            print(f"Could not extract any transactions from ACLEDA statement (OCR text):\n{extracted_text[:200]}...")

    except pytesseract.TesseractError as e:
        print(f"Tesseract OCR error (ACLEDA): {e}")
    except Exception as e:
        print(f"Error during OCR or extraction (ACLEDA): {e}")

    return extracted_transactions

def extract_data(image: np.ndarray, bank_name: str = None) -> List[Dict]:
    if bank_name == "ABA Bank":
        return extract_data_aba(image)
    elif bank_name == "ACLEDA Bank":
        return extract_data_aclida(image)
    else:
        print(f"Bank '{bank_name}' not recognized for data extraction.")
        return []