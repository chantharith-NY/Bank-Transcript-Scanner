# Bank Transcript Scanner

Bank Transaction Scanner is an OCR-powered, machine learning-enhanced web platform designed to automatically classify bank receipt images (ABA and ACLEDA) and extract structured transaction data — including date, amount, currency, and transaction ID — from Khmer and English receipts.

---

## 🚀 Features

- 🧠 **Bank Classification** — Identifies the issuing bank using a CNN model.

- 🔍 **OCR & Data Extraction** — Preprocesses images and extracts transaction details.

- 🧾 **Structured Output** — Parses transaction ID, date, amount, and currency.

- 🗃️ **MongoDB Integration** — Stores transaction data and extraction history.

- 🌐 **Web Interface** — Built using FastAPI and Next.js.

- 📦 **Export & Download** — Export results individually or as zipped reports.

---

## 🔀 Flowchart

### Research Flowchart

<img src="Research Flowchart.jpg" alt="Research Flowchart Image">

### System Workflow

<img src="System Workflow.png" alt="System Workflow Image">

---


## 📁 Project Structure

```
bank_transcript_scanner/
│
├── data/
│   ├── raw/                  # Original scanned PDFs/images
│   └── processed/            # OCR-processed text files
│
├── notebooks/                # Jupyter notebooks for model development
│
├── src/
│   ├── models/               # Trained models
│   │   └── bank_classification.h5
│   ├── extraction/           # Transaction field extraction
│   │   ├── extract_data.py
│   │   └── validation.py
│   ├── backend/              # FastAPI backend
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── bank_classifier.py
│   │   ├── preprocess.py
│   │   └── requirements.txt
│   ├── frontend/             # Next.js frontend
│   │   ├── components/
│   │   ├── pages/
│   │   ├── public/
│   │   ├── package.json
│   │   └── next.config.js
│   └── main.py               # CLI entry point for local testing
│
├── docker-compose.yml        # Docker orchestration
├── requirements.txt          # Project-wide dependencies
├── LICENSE                   # Open source license
└── README.md                 # This file
```
---

## 🛠️ Setup Instructions

### With Docker (Recommended)

```
git clone https://github.com/yourusername/bank_transcript_scanner.git
cd bank_transcript_scanner
docker-compose up --build
```

Visit the app at: `http://localhost:3000`

### Manual Setup

1. Clone the repository:
   ```
   git clone https://github.com/chantharith-NY/Bank-Transcript-Scanner.git
   cd bank_transcript_scanner
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run Backend (FastAPI):
   ```
   uvicorn src.main:app --reload
   ```

5. Run Frontend (Next.js):
   ```
   npm run build 
   npm run dev
   ```

   Visit the app at: `http://localhost:3000`

---

## 🧪 How It Works
- **Upload**: User uploads receipt image (PDF/JPG/PNG).

- **Preprocess**: Convert to grayscale, enhance, resize, and apply thresholding.

- **Classify**: CNN model predicts if it’s ABA or ACLEDA.

- **Extract**: Based on bank template, OCR reads and extracts transaction data.

- **Validate**: Ensures data is in valid format (e.g., dates, currency, IDs).

- **Store**: MongoDB logs results with timestamps.

- **Download**: User can download data in Excel, or CSV.

---

## 📈 Results
- ✅ Successful extraction from Khmer and English receipts.

- ✅ High OCR accuracy with advanced preprocessing.

- ✅ Bank classification model achieved high test accuracy.

- ✅ Web UI enabled smooth file upload, tracking, and download.

---

## 🧠 Tech Stack
- **Frontend**: Next.js, Tailwind CSS

- **Backend**: FastAPI (Python)

- **OCR**: Tesseract OCR

- **ML Framework**: TensorFlow / Keras

- **Database**: MongoDB

- **Deployment**: Docker, Docker Compose

---

## 📌 Limitations

- Templates are hardcoded and may not generalize well to unknown layouts.

- Khmer OCR can still produce errors depending on image quality.

- No field-level cropping (future enhancement).

- Currently supports only ABA and ACLEDA banks.

---

## 🧩 Future Improvements

- Add support for more banks.

- Automate template generation using layout detection.

- Improve Khmer OCR accuracy.

- Integrate OCR systems with cropping (e.g., Google Vision, LayoutLM).

- Store uploaded images and link them to results.

---

## 👨‍💻 Contributors
- Project Lead, and Backend: [NY Chantharith]("https://github.com/chantharith-NY/")
- Frontend Development: [LENG Devid]("https://github.com/KIRIKUUU") and [NY Chantharith]("https://github.com/chantharith-NY/")
- ML and Data Pipeline: [NHEN Theary]("https://github.com/nhentheary"), [NANG Chettra]("https://github.com/Chettraa"), [NGOUN Lyhorng]("https://github.com/Ngounlyhorn11") and [LY Chungheang]("https://github.com/Chungheang0980")
- Documentation and QA: [NY Chantharith]("https://github.com/chantharith-NY/")

---
## 📬 Contact Us

For feedback, questions, or collaborations:

📧 Email: [chantharith77@gmail.com](mailto:chantharith77@gmail.com)

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

