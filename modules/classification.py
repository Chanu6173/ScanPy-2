import re

def classify_document(text):
    """
    Classifies the document based on keywords found in the OCR text.
    """
    text_lower = text.lower()
    
    if "aadhaar" in text_lower: # or "government of india" in text_lower:
        return "Aadhaar"
    elif "permanent account number" in text_lower or "incometax department" in text_lower:
        return "PAN"
    elif "passport" in text_lower or "republic of india" in text_lower:
        return "Passport"
    elif "driving licence" in text_lower or "union of india" in text_lower:
        return "Driving License"
    else:
        return "Other"

def extract_fields(text, doc_type):
    """
    Extracts specific fields based on the document type using Regex.
    """
    data = {}
    
    # Common patterns
    # Note: These are simplified regex patterns for demonstration.
    # Real-world documents have much more variation.
    
    if doc_type == "Aadhaar":
        # Aadhaar: 12 digit number, often spaces in between
        aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
        match = re.search(aadhaar_pattern, text)
        data['ID Number'] = match.group(0) if match else "Not Found"
        
        # Name is hard to extract without specific layout analysis, 
        # but we can try to look for lines that don't look like dates or numbers.
        # For this demo, we might just return the raw text or a placeholder.
        data['Name'] = "Name Extraction (Beta)" 
        
        # DOB
        dob_pattern = r'\b(\d{2}/\d{2}/\d{4})\b'
        match = re.search(dob_pattern, text)
        data['DOB'] = match.group(1) if match else "Not Found"

    elif doc_type == "PAN":
        # PAN: 5 letters, 4 numbers, 1 letter
        pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        match = re.search(pan_pattern, text)
        data['ID Number'] = match.group(0) if match else "Not Found"
        
        # Name often appears near the top or after "Name"
        data['Name'] = "Name Extraction (Beta)"

    elif doc_type == "Passport":
        # Passport Number
        pp_pattern = r'[A-Z]{1}[0-9]{7}'
        match = re.search(pp_pattern, text)
        data['ID Number'] = match.group(0) if match else "Not Found"
        
    elif doc_type == "Driving License":
        # DL Number format varies state to state
        # A common one: KA-01-2020-0000000
        dl_pattern = r'[A-Z]{2}[- ]\d{2}[- ]\d{4}[- ]\d{7}'
        # or just a generic mix
        match = re.search(dl_pattern, text)
        data['ID Number'] = match.group(0) if match else "Not Found"

    else:
        data['Info'] = "Raw Text Only"

    return data
