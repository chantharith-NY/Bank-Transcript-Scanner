import os
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

MODEL_PATH = "models/bank_classification.h5"

CLASS_LABELS = ['ABA Bank', 'ACLIDA Bank', 'OtherBank']

# Load the model when the module is imported (optional, but efficient)
try:
    model = load_model(MODEL_PATH)
    print(f"Bank classification model loaded from: {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Error loading bank classification model: {e}")

def classify_bank(image_path: str, model=model, class_indices=CLASS_LABELS) -> str:
    if model is None:
        print("Bank classification model not loaded. Returning 'Unknown'.")
        return "Unknown"

    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))  # Adjust size based on your model's input size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        predicted_bank = class_indices[predicted_class_index]
        confidence = predictions[0][predicted_class_index]

        print(f"Predicted bank: {predicted_bank} with confidence: {confidence:.2f}")
        return predicted_bank

    except Exception as e:
        print(f"Error during bank classification: {e}")
        return "Unknown"