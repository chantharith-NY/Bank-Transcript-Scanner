from typing import List, Dict

def validate_transaction(transaction: Dict) -> Dict:
    """
    Validates a single extracted transaction for required fields.

    Args:
        transaction: A dictionary representing an extracted transaction.

    Returns:
        A dictionary containing the validation status and missing fields (if any).
        Example:
        {"is_valid": True}
        {"is_valid": False, "missing_fields": ["transaction_id", "date"]}
    """
    missing_fields = []
    if "transaction_id" not in transaction or not transaction.get("transaction_id"):
        missing_fields.append("transaction_id")
    if "date" not in transaction or not transaction.get("date"):
        missing_fields.append("date")
    if "amount" not in transaction or transaction.get("amount") is None:
        missing_fields.append("amount")
    if "currency" not in transaction or not transaction.get("currency"):
        missing_fields.append("currency")

    if missing_fields:
        return {"is_valid": False, "missing_fields": missing_fields, "transaction_data": transaction}
    else:
        return {"is_valid": True, "transaction_data": transaction}

def validate_data(extracted_transactions: List[Dict]) -> tuple[List[Dict], List[Dict]]:
    """
    Validates a list of extracted transactions.

    Args:
        extracted_transactions: A list of dictionaries, where each dictionary
                                represents an extracted transaction.

    Returns:
        A tuple containing two lists:
        - valid_transactions: A list of valid transaction dictionaries.
        - invalid_transactions: A list of dictionaries, where each dictionary
                                contains the invalid transaction data and a list
                                of the missing fields.
    """
    valid_transactions = []
    invalid_transactions = []

    for transaction in extracted_transactions:
        validation_result = validate_transaction(transaction)
        if validation_result["is_valid"]:
            valid_transactions.append(transaction)
        else:
            invalid_transactions.append(validation_result)

    return valid_transactions, [{"transaction_data": err["transaction_data"], "missing_fields": err["missing_fields"]} for err in invalid_transactions]