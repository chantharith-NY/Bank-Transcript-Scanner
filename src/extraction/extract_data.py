# extract_data.py
import re
from typing import List, Dict, Optional
import pytesseract
import numpy as np
from PIL import Image

def extract_data_aba(image: np.ndarray) -> List[Dict]:
    extracted_transactions = []
    try:
        # Perform OCR on the image
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='eng') # Specify language if needed

        # Regular expressions for ABA Bank statement
        id_pattern = re.compile(r"Trx\. ID:\s*(\d+)")
        amount_pattern = re.compile(r"[-]?\d{1,3}(?:,\d{3})*\.\d{2}\s*(USD|KHR)") # Handles comma separators
        date_pattern = re.compile(r"Transaction date: \s*(\w{3}\s+\d{1,2},\s+\d{4})\s+(\d{1,2}:\d{2}\s*(?:AM|PM))")
        
        lines = extracted_text.splitlines()

        transaction: Dict[str, Optional[str | float | dict]] = {}
        for i, line in enumerate(lines):
            if "Trx. ID:" in line:
                id_match = re.search(r"Trx\. ID:\s*(\d+)", line) # Keep on the same line if it appears together
                if not id_match and i + 1 < len(lines):
                    id_match = re.search(r"(\d+)", lines[i+1]) # Check the next line
                if id_match:
                    transaction['transaction_id'] = id_match.group(1)

            if "Transaction date:" in line:
                date_time_match = re.search(r"Transaction date:\s*(\w{3}\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s*(?:AM|PM))", line) # Try same line first
                if not date_time_match and i + 1 < len(lines):
                    date_time_match = re.search(r"(\w{3}\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s*(?:AM|PM))", lines[i+1]) # Check next line
                if date_time_match:
                    transaction['date'] = date_time_match.group(1)
                    transaction['time'] = date_time_match.group(2)

            amount_match = re.search(r"^-?(\d{1,3}(?:,\d{3})*\.\d{2})\s*USD$", line) # Try matching amount on a single line
            if not amount_match: # If not found on a single line, try a broader search
                amount_match = re.search(r"([-]?\d{1,3}(?:,\d{3})*\.\d{2})\s*USD", line)
                if amount_match and "Original amount:" not in line: # Ignore original amount
                    pass # Use this match

            if amount_match:
                amount_str = amount_match.group(1).replace(",", "")
                try:
                    transaction['amount'] = float(amount_str)
                except ValueError:
                    print(f"Error converting amount: {amount_str}")

            # More robust description extraction will be needed based on the layout
            # This is a very basic example - you'll need to analyze the receipt structure
            if "WANG XINMIN" in line and not transaction.get('description'):
                transaction['description'] = "Payment to WANG XINMIN"

            if transaction.get('transaction_id') and transaction.get('date') and transaction.get('amount'):
                extracted_transactions.append(transaction.copy())
                transaction = {}

        print(f"Extracted Transactions (ABA):\n{extracted_transactions}") # Log the extracted transactions
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
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='eng')
        lines = extracted_text.splitlines()

        transaction: Dict[str, Optional[str | float | dict]] = {}
        for line in lines:
            amount_match = re.search(r"Payment Amount\s*:\s*([-]?\d{1,3}(?:,\d{3})*\.\d{2})\s*USD", line)
            if amount_match:
                amount_str = amount_match.group(1).replace(",", "")
                try:
                    transaction['amount'] = float(amount_str)
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

            if transaction.get('amount') and transaction.get('date'):
                info: Dict[str, Optional[List[str]]] = {}
                if not transaction.get('date'):
                    info.setdefault('missing_fields', []).append('date')
                if transaction.get('amount') is None:
                    info.setdefault('missing_fields', []).append('amount')
                if not transaction.get('description'):
                    info.setdefault('missing_fields', []).append('description')

                if info:
                    transaction['info'] = info

                extracted_transactions.append(transaction.copy()) # Append a copy
                transaction = {} # Reset

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