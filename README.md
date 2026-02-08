# ScanPy 📄
**Offline Identity Document Processing System**

## link: https://scanpy6173.streamlit.app/
A production-ready, zero-cost, offline document scanner built with Streamlit, OpenCV, and Tesseract.
<img width="1913" height="906" alt="image" src="https://github.com/user-attachments/assets/8492ec4c-a375-49f9-8d67-5c20a0e0daf9" />

## 🚀 Features
- **Offline Processing**: No cloud APIs, data stays on your machine.
- **Smart OCR**: Uses Tesseract for text extraction.
- **Auto-Classification**: Detects Aadhaar, PAN, Passport, etc.
- **Image Enhancement**: Cleans up scans for better readability.
- **Local Database**: Stores extraction results in SQLite.

## 🛠 Prerequisites
You need to have the following installed on your system:

1. **Python 3.8+**
2. **Tesseract OCR**:
   - Download and install from [here](https://github.com/UB-Mannheim/tesseract/wiki).
   - Default path expected: `C:\Program Files\Tesseract-OCR\tesseract.exe`.
3. **Poppler (for PDF support)**:
   - Download from [here](https://github.com/oschwartz10612/poppler-windows/releases/).
   - Add `poppler/bin` to your System PATH or update `modules/preprocessing.py`.

## 📦 Installation
```bash
pip install -r requirements.txt
```

## ▶️ Running the App
```bash
streamlit run app.py
```

## 📂 Project Structure
- `app.py`: Main application UI.
- `modules/`: Core logic (OCR, Processing, Database).
- `assets/`: Custom CSS and images.
- `data/`: Local SQLite database.
