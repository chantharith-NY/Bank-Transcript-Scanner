import requests
import os
import json  # Added missing import
from pathlib import Path
from typing import List, Dict

def test_classify_endpoint(image_paths: List[str], endpoint: str = "http://localhost:5000/classify"):
    """
    Test the /classify endpoint with image files.
    
    Args:
        image_paths (List[str]): List of paths to image files.
        endpoint (str): API endpoint URL.
        
    Returns:
        None: Prints results or errors.
    """
    files = []
    for img_path in image_paths:
        if not Path(img_path).is_file():
            print(f"Skipping {img_path}: Not a valid file")
            continue
        files.append(("files", (Path(img_path).name, open(img_path, "rb"), "image/jpeg")))
    
    if not files:
        print("No valid images to test")
        return
    
    print(f"\nTesting {len(files)} image(s): {[f[1][0] for f in files]}")
    
    try:
        response = requests.post(endpoint, files=files, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print("Response:", json.dumps(data, indent=2))
        
        if "prediction" in data and isinstance(data["prediction"], list):
            print(f"Success: Received {len(data['prediction'])} predictions")
            for img_name, pred in zip([f[1][0] for f in files], data["prediction"]):
                print(f"  File {img_name}: Classified as {pred}")
        else:
            print("Warning: Unexpected response format")
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Could not connect to the server. Is it running at", endpoint, "?")
    except requests.exceptions.Timeout:
        print("Timeout Error: Request took too long")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}")
    except ValueError as e:
        print(f"JSON Decode Error: {str(e)}")
    finally:
        # Close file handles
        for _, (name, file, _) in files:
            file.close()

def main(input_path: str, endpoint: str = "http://localhost:5000/classify"):
    """
    Test the /classify endpoint with image files.
    
    Args:
        input_path (str): Path to image file or directory.
        endpoint (str): API endpoint URL.
    """
    try:
        # Collect image paths
        input_path = Path(input_path)
        image_paths = []
        
        if input_path.is_file():
            image_paths.append(str(input_path))
        elif input_path.is_dir():
            for file_path in input_path.glob("*.[jJ][pP][gG]") or input_path.glob("*.[pP][nN][gG]"):
                image_paths.append(str(file_path))
        else:
            raise ValueError(f"Input path {input_path} is not a valid file or directory")
        
        if not image_paths:
            print("No images found in", input_path)
            return
        
        # Test the classify endpoint
        print(f"Found {len(image_paths)} images")
        test_classify_endpoint(image_paths, endpoint)
        
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    # Configuration
    input_path = "test.png"  # Updated to match your test image
    endpoint = "http://localhost:5000/classify"  # FastAPI endpoint
    
    main(input_path, endpoint)