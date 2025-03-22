def classify_bank(extracted_text: str) -> str:
    bank_keywords = {
        "ABA Bank": ["ABA BANK", "National Bank of Canada Group"]
    }
    
    for bank, keywords in bank_keywords.items():
        if any(keywords.lower() in extracted_text.lower() for keywords in keywords):
            return bank
    return "Unknown Bank"