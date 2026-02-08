import cv2
import numpy as np
from PIL import Image
import io
from pdf2image import convert_from_bytes

def load_image(file):
    """Loads an image from a Streamlit uploaded file (BytesIO)."""
    try:
        image = Image.open(file)
        # Convert to RGB if necessary (handles RGBA, P, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        # Convert to numpy array and then to BGR for OpenCV compatibility
        img_array = np.array(image)
        # OpenCV expects BGR, but PIL gives RGB, so we convert
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        return img_bgr
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def load_pdf(file):
    """Converts the first page of a PDF to an image."""
    try:
        # Poppler must be in PATH or configured. 
        # Using a default common path or relying on system PATH.
        file_bytes = file.read()
        images = convert_from_bytes(file_bytes)
        if not images:
            return None
        # Convert PIL Image to numpy array and then to BGR for OpenCV
        img_array = np.array(images[0])
        # If image is RGB, convert to BGR for OpenCV
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            return img_bgr
        return img_array
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return None

def enhance_image(image):
    """Applies grayscale and adaptive thresholding for better OCR."""
    try:
        # Ensure image is in the correct format
        if image is None:
            return None
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Ensure uint8 format
        if gray.dtype != np.uint8:
            gray = (gray * 255).astype(np.uint8) if gray.max() <= 1.0 else gray.astype(np.uint8)

        # Mild blurring to remove noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive thresholding to handle lighting variations
        processed = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return processed
    except Exception as e:
        print(f"Error enhancing image: {e}")
        # Return original grayscale if enhancement fails
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

def perspective_correction(image):
    """
    Placeholder for perspective correction. 
    In a real full implementation, this would find contours and warp.
    For this version, we'll return the original to avoid instability with varied backgrounds.
    """
    return image
