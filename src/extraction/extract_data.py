# extract_data.py
import re
from typing import List, Dict
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
        amount_pattern = re.compile(r"[-]?\d{1,3}(?:,\d{3})*\.\d{2}\s*USD") # Handles comma separators
        date_pattern = re.compile(r"Transaction date: \s*(\w{3}\s+\d{1,2},\s+\d{4})\s+(\d{1,2}:\d{2}\s*(?:AM|PM))")

        # Split the extracted text into lines or relevant blocks if needed for better parsing
        lines = extracted_text.splitlines()

        transaction = {}
        for line in lines:
            id_match = id_pattern.search(line)
            if id_match:
                transaction['transaction_id'] = id_match.group(1)

            amount_match = amount_pattern.search(line)
            if amount_match:
                amount_str = amount_match.group(0).replace(",", "").replace(" USD", "")
                try:
                    transaction['amount'] = float(amount_str)
                except ValueError:
                    print(f"Error converting amount: {amount_str}")

            date_match = date_pattern.search(line)
            if date_match:
                transaction['date'] = date_match.group(1)
                transaction['time'] = date_match.group(2)

            # You might need more sophisticated logic to identify the end of a transaction
            # and append it to extracted_transactions. This depends heavily on the statement format.
            # For a simple case where each transaction spans a few lines and has all info,
            # you might need to implement a state machine or look for specific delimiters.

        # Simple approach: If we found some key information, consider it a transaction.
        if transaction.get('transaction_id') or transaction.get('amount') or transaction.get('date'):
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
        extracted_text = pytesseract.image_to_string(Image.fromarray(image), lang='eng') # Specify language if needed

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

def extract_data(image: np.ndarray, bank_name: str = None) -> List[Dict]:
    if bank_name == "ABA Bank":
        return extract_data_aba(image)
    elif bank_name == "ACLEDA Bank":
        return extract_data_aclida(image)
    else:
        print(f"Bank '{bank_name}' not recognized for data extraction.")
        return []