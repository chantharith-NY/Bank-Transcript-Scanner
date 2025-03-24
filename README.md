# Bank Transcript Scanner

## 📌 Objective
This project aims to automate the extraction of key financial data from scanned bank transcripts (PDFs or images) for business auditing. The pipeline consists of:
1. **OCR Processing** – Convert scanned bank transcripts into readable text.
2. **Bank Classification** – Identify the bank to apply specific extraction rules.
3. **Data Extraction** – Extract date, transaction ID, and amount from the transcript.
4. **Validation & Storage** – Ensure extracted data accuracy and store it in a structured format.
5. **Web Deployment** – Deploy the system as a web application for user-friendly access.

## 🏗️ Project Structure
```
📂 bank_transcript_scanner
│── 📁 data                  # Raw and processed data
│   ├── 📂 raw               # Original scanned PDFs/images of bank statements
│   ├── 📂 processed         # Extracted text from OCR
│── 📁 models                # Trained models for classification & extraction
│   ├── bank_classifier.pkl  # Bank classification model
│── 📁 notebooks             # Jupyter Notebooks for exploration and testing
│── 📁 src                   # Source code
│   ├── 📂 ocr               # OCR processing scripts
│   │   ├── preprocess.py    # Preprocess images (grayscale, thresholding, etc.)
│   │   ├── ocr_engine.py    # Extract text using Tesseract OCR
│   │   ├── text_cleaning.py # Clean and format extracted text
│   ├── 📂 classification    # Bank classification model
│   │   ├── train_classifier.py # Train ML model for bank classification
│   │   ├── classify_bank.py    # Classify bank from extracted text
│   │   ├── bank_classifier.pkl # Saved ML model
│   ├── 📂 extraction        # Extract key details from statements
│   │   ├── extract_data.py  # Extract dates, amounts, transaction IDs
│   │   ├── validation.py    # Validate extracted information
│   ├── 📂 backend           # Backend API (FastAPI)
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── routes.py        # API routes for OCR, classification, extraction
│   │   ├── models.py        # Define database models
│   │   ├── database.py      # Database connection setup
│   │   ├── requirements.txt # Backend dependencies
│   ├── 📂 frontend          # Frontend (Next.js)
│   │   ├── 📂 components    # Reusable UI components
│   │   ├── 📂 pages         # Main pages (upload, results, etc.)
│   │   ├── 📂 public        # Static assets (icons, logos)
│   │   ├── 📂 styles        # CSS/Styling files
│   │   ├── package.json     # Frontend dependencies
│   │   ├── next.config.js   # Next.js configuration
│   │   ├── App.js           # Main app file
│   │   ├── index.js         # Home page
│   ├── main.py              # Entry point for running pipeline (CLI)
│── 📁 tests                 # Unit tests for OCR, classification, extraction
│   ├── test_ocr.py          # Test OCR extraction
│   ├── test_classification.py # Test bank classification model
│   ├── test_extraction.py   # Test data extraction
│── 📁 deployment            # Deployment configurations (Docker, cloud, etc.)
│   ├── Dockerfile           # Docker setup
│   ├── docker-compose.yml   # Multi-container setup (DB, API, frontend)
│   ├── config.yaml          # Configuration settings
│── requirements.txt         # Backend dependencies
│── README.md                # Project documentation
│── LICENSE                  # License information

```

## 🛠️ Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/chantharith-NY/Bank-Transcript-Scanner.git
   cd bank_transcript_scanner
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the pipeline (example):
   ```bash
   python src/main.py --input data/raw/sample.pdf
   ```

## 🌐 Web Deployment
- **Frontend**: Built with React or Next.js for a modern and responsive UI.
- **Backend**: Flask or FastAPI for API endpoints handling OCR, classification, and extraction.
- **Deployment**: Dockerized setup with AWS, Vercel, or Heroku hosting.
- **User Interaction**: Upload transcripts, view extracted data, download results, and manage scanned records.

## 🔍 Features
- **OCR Processing**: Uses Tesseract OCR.
- **Bank Classification**: ML model to categorize bank transcripts.
- **Data Extraction**: NLP and regex-based extraction of key financial details.
- **Web Interface**: Allows easy document uploads and review of extracted data.
- **Scalability**: Supports multiple bank formats and integrations.

## 🚀 Next Steps
- Implement OCR pipeline.
- Train classification model.
- Develop robust data extraction logic.
- Build and deploy the full-stack web application.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
👨‍💻 Developed by: 
- LENG Devid
- LY Chungheang
- NANG Chettra
- NGOUN Lyhorng
- NHEN Theary
- NY Chantharith