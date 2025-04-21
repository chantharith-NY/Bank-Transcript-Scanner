import cv2
import numpy as np
from io import BytesIO

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess an image from bytes for bank classification.
    
    Args:
        image_bytes (bytes): Raw image data (e.g., from UploadFile).
        
    Returns:
        np.ndarray: Preprocessed image (thresholded).
        
    Raises:
        ValueError: If the image cannot be processed.
    """
    try:
        # Convert bytes to NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        # Decode image with cv2
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply slight Gaussian Blur to remove noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Use Adaptive Thresholding for better text contrast
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
        )
        
        return thresh
    
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")