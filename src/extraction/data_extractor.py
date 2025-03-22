import re 

def extract_transaction_data(extracted_txt: str, bank_name: str) -> list:
    transactions = []
    
    transaction_pattern = re.compile(r"(\\d{2}/\\d{2}/\\d{4})\\s+([A-Za-z0-9]+)\\s+([-+]?[0-9,.]+)")
    
    for match in transaction_pattern.finditer(extracted_txt):
        date, transaction_id, amount = match.groups()
        transactions.append({
            "date": date,
            "transaction_id": transaction_id,
            "amount": amount
        })
        
    return transactions