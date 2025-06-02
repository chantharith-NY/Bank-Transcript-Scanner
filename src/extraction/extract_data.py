import re
from typing import List, Dict
import pytesseract
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # adjust if needed

def extract_data_aba(image: np.ndarray, debug: bool=False) -> List[Dict]:
    extracted_transactions = []
    try:
        # Khmer + English OCR
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='khm+eng', config=custom_config)

        # Clean up
        lines = [line.strip() for line in extracted_text.splitlines() if line.strip()]

        # Extract Trx ID
        trx_id = None
        for line in lines:
            if "លេខកូដប្រតិបត្តិការ" in line or "លេខកូដ" in line or "Trx. ID" in line:
                match = re.search(r'\d{6,}', line)
                if match:
                    trx_id = match.group()
                    break

        # Extract Transaction Date
        trx_date = None
        for line in lines:
            # More robust date extraction: comma optional, flexible spacing, AM/PM
            match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\s+\d{1,2}:\d{2}\s*(AM|PM)', line)
            if match:
                trx_date = match.group()
                break

        # Extract Amount (top line)
        amount_usd = None
        amount_khr = None
        for line in lines:
            # Check for currency as single letter after the amount (e.g., 1000.00 U or 40000.00 K)
            match = re.search(r'(-?\d{1,3}(,\d{3})*(\.\d{2})?)\s*([UK])\b', line, re.IGNORECASE)
            if match:
                amount_val = match.group(1).replace(',', '')
                currency = match.group(4).upper()
                try:
                    amount_val_abs = abs(float(amount_val))
                    if currency == 'U':
                        amount_usd = amount_val_abs
                    elif currency == 'K':
                        amount_khr = amount_val_abs
                except ValueError:
                    pass
                break
            # Fallback: currency at the end (USD/KHR, any case)
            match = re.search(r'(-?\d{1,3}(,\d{3})*(\.\d{2})?)\s*(USD|KHR)', line, re.IGNORECASE)
            if match:
                amount_val = match.group(1).replace(',', '')
                currency = match.group(4).upper()
                try:
                    amount_val_abs = abs(float(amount_val))
                    if currency == 'USD':
                        amount_usd = amount_val_abs
                    elif currency == 'KHR':
                        amount_khr = amount_val_abs
                except ValueError:
                    pass
                break
        # Compose transaction dict
        transaction = {
            "transaction_id": trx_id,
            "transaction_date": trx_date,
            "amount_usd": amount_usd,
            "amount_khr": amount_khr,
            "full_ocr_text": extracted_text
        }
        if debug:
            print(f"Extracted: {transaction}")
        extracted_transactions.append(transaction)

        if not extracted_transactions:
            print(f"Could not extract any transactions from ABA statement (OCR text):\n{extracted_text[:200]}...")

    except pytesseract.TesseractError as e:
        print(f"Tesseract OCR error (ABA): {e}")
    except Exception as e:
        print(f"Error during OCR or extraction (ABA): {e}")

    return extracted_transactions


def extract_data_aclida(image: np.ndarray) -> List[Dict]:
    extracted_transactions = []
    try:
        # Perform OCR on the image
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='eng', config=custom_config) # Specify language if needed

        # Regular expressions for ACLEDA Bank statement (adjust based on actual format)
        amount_pattern = re.compile(r"Payment Amount\s*:\s*([-]?\d{1,3}(?:,\d{3})*\.\d{2})\s*USD")
        datetime_pattern = re.compile(r"Date\s*:\s*(\w{3}\s+\d{1,2},\s+\d{4})\s+(\d{2}:\d{2}\s*(?:AM|PM))")
        completed_ref_pattern = re.compile(r"Completed\s*:\s*Ref\.\s*(\S+)")
        external_txn_ref_pattern = re.compile(r"External Txn Ref\s*:\s*(\S+)")

        lines = extracted_text.splitlines()
        transaction = {}
        for line in lines:
            amount_match = amount_pattern.search(line)
            if amount_match:
                amount_str = amount_match.group(1).replace(",", "")
                try:
                    transaction['amount'] = float(amount_str)
                except ValueError:
                    print(f"Error converting amount: {amount_str}")

            datetime_match = datetime_pattern.search(line)
            if datetime_match:
                transaction['date'] = datetime_match.group(1)
                transaction['time'] = datetime_match.group(2)

            completed_ref_match = completed_ref_pattern.search(line)
            if completed_ref_match:
                transaction['completed_ref'] = completed_ref_match.group(1)

            external_txn_ref_match = external_txn_ref_pattern.search(line)
            if external_txn_ref_match:
                transaction['external_txn_ref'] = external_txn_ref_match.group(1)

        if transaction.get('amount') and transaction.get('date') and transaction.get('time'):
            extracted_transactions.append(transaction)

        if not extracted_transactions:
            print(f"Could not extract any transactions from ACLEDA statement (OCR text):\n{extracted_text[:200]}...")

    except pytesseract.TesseractError as e:
        print(f"Tesseract OCR error (ACLEDA): {e}")
    except Exception as e:
        print(f"Error during OCR or extraction (ACLEDA): {e}")

    return extracted_transactions

def extract_data(image: np.ndarray, bank_name: str = None, debug: bool = False) -> List[Dict]:
    if bank_name == "ABA Bank":
        return extract_data_aba(image, debug)
    elif bank_name == "ACLEDA Bank":
        return extract_data_aclida(image, debug)
    else:
        print(f"Bank '{bank_name}' not recognized for data extraction.")
        return []