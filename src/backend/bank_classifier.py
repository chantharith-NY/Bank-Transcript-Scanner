import os
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

MODEL_ID = "1HytjcwkwIgc7r8v0xkptgiJ5mL6lhyiO"
MODEL_URL = f"https://drive.google.com/uc?id={MODEL_ID}&export=download"
MODEL_PATH = "models/bank_classification.h5"
MODEL_DIR = "drive_models/"

CLASS_LABELS = ['ABA Bank', 'ACLIDA Bank', 'OtherBank']

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load the model, downloading if necessary
model = None
try:
    if not os.path.exists(MODEL_PATH):
        print(f"Bank classification model not found at: {MODEL_PATH}")
        print(f"Downloading bank classification model from Google Drive...")
        try:
            response = requests.get(MODEL_URL, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            bytes_downloaded = 0
            with open(MODEL_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    if total_size_in_bytes:
                        progress = (bytes_downloaded / total_size_in_bytes) * 100
                        print(f"Download progress: {progress:.2f}%", end='\r')
            print("\nBank classification model downloaded successfully from Google Drive.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading model from Google Drive: {e}")
        except Exception as e:
            print(f"Error saving downloaded model: {e}")
    else:
        print(f"Bank classification model already exists at: {MODEL_PATH}")

    model = load_model(MODEL_PATH)
    print(f"Bank classification model loaded successfully.")

except Exception as e:
    model = None
    print(f"Error during model loading: {e}")

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
