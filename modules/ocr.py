import pytesseract
import cv2
import numpy as np
import sys
import os

# Configuration for Tesseract based on common Windows install paths
# Users might need to adjust this.
possible_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\AppData\Local\Tesseract-OCR\tesseract.exe'
]

tesseract_cmd = None
for path in possible_paths:
    if os.path.exists(path):
        tesseract_cmd = path
        break

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
# Else, rely on PATH

def extract_text(image):
    """Extracts text from a preprocessed image using Tesseract."""
    try:
        if image is None:
            return "Error: No image provided for OCR"
        
        # Ensure image is in uint8 format
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        
        # Configuration: 
        # --oem 3: Default OCR Engine Mode
        # --psm 6: Assume a single uniform block of text (good for docs)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text.strip() if text else "No text detected"
    except Exception as e:
        return f"OCR Error: {str(e)}"
