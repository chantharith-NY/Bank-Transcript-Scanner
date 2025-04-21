from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from bank_classifier import classify_bank, model  # Import model variable
import os
import tempfile
from io import BytesIO
from tensorflow.keras.models import Model  # For type checking

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Check if the bank classification model is loaded.
    """
    if model is not None and isinstance(model, Model):
        return {"status": "healthy", "model_loaded": True, "model_path": "models/bank_classification.h5"}
    else:
        return {"status": "unhealthy", "model_loaded": False, "error": "Model not loaded"}

@app.post("/classify")
async def predict_endpoint(files: List[UploadFile] = File(...)):
    try:
        predictions = []
        for file in files:
            # Read the uploaded file's contents
            contents = await file.read()
            
            # Create a temporary file to store the image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(contents)
                temp_file_path = temp_file.name
            
            try:
                # Call classify_bank with the temporary file path
                prediction = classify_bank(temp_file_path)
                predictions.append(prediction)
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_path)
        
        return {"prediction": predictions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)