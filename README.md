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
│   ├── 📂 raw                # Original scanned PDFs or images
│   ├── 📂 processed          # Text extracted from OCR
│── 📁 models                # Trained models for classification & extraction
│── 📁 notebooks             # Jupyter Notebooks for exploration and testing
│── 📁 src                   # Source code
│   ├── 📂 ocr               # OCR processing scripts
│   ├── 📂 classification    # Bank classification model
│   ├── 📂 extraction        # Data extraction logic
│   ├── 📂 backend           # Backend API (FastAPI)
│   ├── 📂 frontend          # Frontend (Next.js)
│   ├── main.py              # Entry point of the pipeline
│── 📁 tests                 # Unit tests for OCR, classification, extraction
│── 📁 deployment            # Deployment configurations (Docker, cloud, etc.)
│── requirements.txt         # Dependencies
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