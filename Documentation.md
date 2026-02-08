# ScanPy Documentation 📘
**Enterprise-Grade Offline Identity Document Processing System**

## 1. Project Overview
ScanPy is a zero-cost, offline web application designed to scan, OCR, classify, and extract data from identity documents (Aadhaar, PAN, Passport, etc.). It mimics the UX of professional tools like Google Drive Scanner but runs entirely on the local machine.

## 2. Technology Stack 🛠
- **Frontend**: Streamlit (Python)
- **OCR Engine**: Tesseract (via `pytesseract`)
- **Image Processing**: OpenCV (`cv2`), NumPy, Pillow
- **PDF Handling**: `pdf2image`, Poppler
- **Database**: SQLite3
- **Styling**: Custom CSS3 (Inter font, Gradient backgrounds)

## 3. Directory Structure
```
ScanPy/
├── app.py                  # Main Application Entry Point
├── requirements.txt        # Python Dependencies
├── assets/
│   └── style.css          # Custom UI Styling
├── data/
│   ├── scanpy.db          # SQLite Database
│   └── uploads/           # Local File Storage
└── modules/
    ├── preprocessing.py    # Image Enhancement Logic
    ├── ocr.py              # Tesseract Integration
    ├── classification.py   # Rule-Based Document Detection
    └── database.py         # DB Operations
```

## 4. Module Details

### 4.1. Preprocessing (`modules/preprocessing.py`)
**Purpose**: Prepare images for OCR by reducing noise and normalizing lighting.

**Key Logic**:
```python
def enhance_image(image):
    # Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gaussian Blur (Noise Reduction)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive Thresholding (Lighting Normalization)
    processed = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    return processed
```

### 4.2. OCR Engine (`modules/ocr.py`)
**Purpose**: Extract raw text from images.
Uses Tesseract with configuration `--oem 3` (Default Engine Mode) and `--psm 6` (Assume a single uniform block of text).

### 4.3. Classification (`modules/classification.py`)
**Purpose**: Identify document type based on keyword analysis.

**Rule Set**:
- **Aadhaar**: Contains "aadhaar"
- **PAN**: Contains "permanent account number" or "incometax"
- **Passport**: Contains "passport" or "republic of india"
- **Driving License**: Contains "driving licence"

### 4.4. Database (`modules/database.py`)
**Schema**:
```sql
CREATE TABLE scans (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    upload_date TEXT,
    doc_type TEXT,
    extracted_text TEXT,
    structured_data TEXT,
    file_path TEXT
)
```

## 5. UI & Styling (`assets/style.css`)
- **Background**: Linear Gradient (`#a1c4fd` to `#c2e9fb`).
- **Font**: Inter (Google Fonts).
- **Components**: Custom rounded cards with box-shadows.

## 6. Setup & Installation
1. Install Python 3.8+.
2. Install Tesseract OCR & Poppler.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.
