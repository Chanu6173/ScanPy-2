import streamlit as st
import numpy as np
import cv2
import os
import time
from PIL import Image

# Custom Modules
from modules.preprocessing import load_image, load_pdf, enhance_image
from modules.ocr import extract_text
from modules.classification import classify_document, extract_fields
from modules.database import init_db, save_scan

# Page Config
st.set_page_config(
    page_title="ScanPy | Identity Processor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize DB
init_db()

# --- Sidebar ---
st.sidebar.markdown("""
    <div class="user-profile-section">
        <h2>👤 User Profile</h2>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div class="user-profile-info">
        <p><strong>Role:</strong> Student Developer</p>
        <p><strong>Mode:</strong> Offline</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
# Custom HTML for System Status to ensure visibility
st.sidebar.markdown("""
    <div class="sidebar-status">
        <h3>🛠 System Status</h3>
        <div class="status-item">
            <span class="status-icon">✅</span>
            <span class="status-label">OCR Engine:</span>
            <span class="status-value">Online</span>
        </div>
        <div class="status-item">
            <span class="status-icon">✅</span>
            <span class="status-label">Database:</span>
            <span class="status-value">Connected</span>
        </div>
        <div class="status-item">
            <span class="status-icon">✅</span>
            <span class="status-label">Pipeline:</span>
            <span class="status-value">Ready</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
with st.sidebar.expander("⚙️ Settings"):
    st.checkbox("Enable Auto-Enhancement", value=True)
    st.checkbox("Debug Mode", value=False)
    st.button("Save Settings")

# --- Main Content ---
st.title("ScanPy")
st.markdown("** Offline Identity Document Processing System**")

# Layout
col1, col2 = st.columns([1, 1])

uploaded_file = st.file_uploader("Upload Document (JPG, PNG, PDF)", type=['jpg', 'png', 'jpeg', 'pdf'])

if uploaded_file is not None:

    # 1. Loading & Local Saving
    with st.spinner('Loading document...'):
        # Create uploads directory if not exists
        upload_dir = os.path.join("data", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Reset file pointer before reading
        uploaded_file.seek(0)
        
        if uploaded_file.name.endswith('.pdf'):
            image = load_pdf(uploaded_file) # Returns numpy array
        else:
            image = load_image(uploaded_file) # Returns numpy array
        
        if image is None:
            st.error("Failed to load document.")
            st.stop()

    # 2. Preprocessing
    with st.spinner('Enhancing image...'):
        processed_image = enhance_image(image)
        # Convert numpy array to PIL Image for display
        # Handle color space conversion (OpenCV uses BGR, PIL uses RGB)
        if len(image.shape) == 3:
            # Color image - convert BGR to RGB
            if image.shape[2] == 3:
                display_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                display_image = Image.fromarray(image)
        else:
            # Grayscale image
            display_image = Image.fromarray(image, mode='L')
        
        # Processed image is grayscale from enhance_image
        if len(processed_image.shape) == 2:
            display_processed = Image.fromarray(processed_image, mode='L')
        else:
            display_processed = Image.fromarray(processed_image)

    # 3. Pipeline Visualization
    st.markdown("### 🚀 Processing Pipeline")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = ["Scanning...", "Optical Character Recognition...", "Classifying...", "Extracting Fields..."]
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.5) # Simulate processing time for UX
    
    status_text.text("Processing Complete ✅")
    
    # 4. Results
    
    # Left Column: Visuals
    with col1:
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("Document Preview")
        toggle = st.radio("View Mode", ["Original", "Enhanced"], horizontal=True)
        
        if toggle == "Original":
            st.image(display_image, use_container_width=True)
        else:
            st.image(display_processed, use_container_width=True)
        
        # Simulating Texture/Grain (visual only)
        st.caption("Rendering at 300 DPI | Paper Texture Applied")
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Data
    with col2:
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("Extracted Data")
        
        # OCR & Classification
        raw_text = extract_text(processed_image)
        doc_type = classify_document(raw_text)
        fields = extract_fields(raw_text, doc_type)
        
        # Display Document Type with Color
        st.markdown(f"**Detected Type:** <span style='color:#2563eb; font-weight:bold; font-size:1.2em'>{doc_type}</span>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Form
        with st.form("extraction_form"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                name = st.text_input("Full Name", value=fields.get("Name", ""))
                dob = st.text_input("Date of Birth", value=fields.get("DOB", ""))
            
            with col_b:
                id_num = st.text_input(f"{doc_type} Number", value=fields.get("ID Number", ""))
                nationality = st.text_input("Nationality", value="India") # Placeholder Logic
            
            raw_edit = st.text_area("Raw Extracted Text", value=raw_text, height=150)
            

            submitted = st.form_submit_button("Verify & Save to Database")
            
            if submitted:
                if save_scan(uploaded_file.name, doc_type, raw_edit, fields, file_path):
                    st.success("Data Saved Successfully to Local Database!")
                    st.balloons()
                else:
                    st.error("Database Error")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty State
    st.markdown("""
    <div class="welcome-message">
        <h2>👋 Welcome!</h2>
        <p>Please upload an identity document to begin.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show Recent Scans
    st.markdown("### 📂 Recent Scans")
    from modules.database import get_recent_scans
    try:
        rows = get_recent_scans()
        if rows:
            for row in rows:
                st.text(f"📄 {row[1]} | {row[3]}")
    except:
        pass
