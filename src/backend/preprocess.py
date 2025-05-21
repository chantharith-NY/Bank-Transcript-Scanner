import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply slight Gaussian Blur to remove noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    
    mean_val = np.mean(blurred)
    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    # If background is dark, invert the image
    if mean_val < 127:
        thresh = cv2.bitwise_not(thresh)
    
    return thresh

def preprocess_image_advanced(image_path, debug=False):
    """
    Preprocess an image for OCR, robust to both dark and light backgrounds.
    Crops to the transaction region, resizes, enhances, and inverts if needed.
    Optionally saves intermediate images for debugging.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")
    # Remove cropping to preserve all transaction data
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_LANCZOS4)
    mean_val = np.mean(gray)
    if mean_val < 127:
        gray = cv2.bitwise_not(gray)
    alpha = 0.9
    beta = 60
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(adjusted, -1, kernel)
    normalized = cv2.normalize(sharpened, None, 0, 255, cv2.NORM_MINMAX)
    # Only use thresholding for dark backgrounds
    if mean_val < 127:
        # Try adaptive thresholding as a fallback
        result = cv2.adaptiveThreshold(normalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    else:
        result = normalized
    if debug:
        import os
        debug_dir = os.path.join(os.path.dirname(image_path), 'debug_preprocess')
        os.makedirs(debug_dir, exist_ok=True)
        cv2.imwrite(os.path.join(debug_dir, '01_gray.png'), gray)
        cv2.imwrite(os.path.join(debug_dir, '02_adjusted.png'), adjusted)
        cv2.imwrite(os.path.join(debug_dir, '03_sharpened.png'), sharpened)
        cv2.imwrite(os.path.join(debug_dir, '04_normalized.png'), normalized)
        if mean_val < 127:
            cv2.imwrite(os.path.join(debug_dir, '05_thresh.png'), result)
    return result