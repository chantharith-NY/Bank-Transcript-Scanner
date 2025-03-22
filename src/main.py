import argparse
import os
from src.ocr.ocr_processor import extract_text_from_pdf
from src.classification.bank_classifier import classify_bank
from src.extraction.data_extractor import extract_transaction_data
import json

def process_bank_transcript(input_file: str):
    extracted_text = extract_text_from_pdf(input_file)
    print("Extracted text:", extracted_text[:500])
    
    bank_name = classify_bank(extracted_text)
    print(f"Identified Bank: {bank_name}")
    
    transactions = extract_transaction_data(extracted_text, bank_name)
    print("Extracted Transactions:", transactions)
    
    output_file = os.path.join("../data/processed", f"{os.path.basename(input_file)}.json")
    with open(output_file, "w") as f:
        json.dump(transactions, f, indent=4)
        
    print(f"Processed data saved to {output_file}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bank Transcript Scanner")
    parser.add_argument("--input", required=True, help="Path to the input bank transcript PDF")
    args = parser.parse_args()
    process_bank_transcript(args.input)