

# 🔒 PDF Redaction Tool

A **Streamlit-based web application** that allows you to securely redact sensitive information from PDF files.  
It supports both **native text redaction** and **OCR-based detection**, ensuring even scanned documents are permanently sanitized — not just visually hidden.

---

## 🚀 Features

✅ **Keyword-based Redaction**
- Enter one or more keywords to automatically detect and redact them.
- Works across both text-based and scanned PDFs.

✅ **Real Redaction (Non-selectable)**
- Permanently deletes sensitive text and image data instead of simply overlaying black boxes.
- Prevents users from copying or extracting hidden text from the PDF.

✅ **Dual Detection Method**
- **Native PDF text search** for standard documents.  
- **OCR (Optical Character Recognition)** using Tesseract for image-based PDFs or scanned pages.

✅ **Dynamic Keyword Management**
- Add keywords quickly via an input field.
- Remove keywords using clickable ❌ chips.

✅ **High-resolution OCR Processing**
- Uses 300 DPI rendering for precise OCR bounding boxes and accurate keyword detection.

✅ **Progress Tracking**
- Real-time progress bar updates while processing large PDFs.

✅ **Instant Download**
- Download the fully redacted and sanitized PDF directly from your browser.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** – Web app interface  
- **PyMuPDF (fitz)** – PDF manipulation and redaction  
- **Pillow (PIL)** – Image handling  
- **Tesseract OCR** – OCR engine for scanned PDFs  
- **pytesseract** – Python wrapper for Tesseract  

---

## 📂 Project Structure

```

pdf-redactor/
│
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md           # Documentation

````

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/whybhav360/PDFRedactor.git
cd pdf-redactor
````

### 2. Create a Virtual Environment

```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```
```
** `requirements.txt`:**

```
streamlit
pymupdf
pillow
pytesseract
```
```
### 4. Install Tesseract
```
**Windows:**

* [Download here](https://github.com/tesseract-ocr/tesseract)
* Default install path used in the code:


  C:\Program Files\Tesseract-OCR\tesseract.exe
**Mac (Homebrew):**

```bash
brew install tesseract
```

### 5. Run the Application

```
streamlit run app.py
```

---

## 💻 Usage

### 1. Upload PDF

Drag and drop your PDF file into the uploader.

### 2. Enter Keywords

Type a keyword (e.g., `password`, `confidential`) and press **Enter**.
Repeat for multiple keywords.
Remove any keyword by clicking ❌ on its chip.

### 3. Start Redaction

Click 🚀 **Start Redaction** to begin the process.
Wait for the progress bar to complete.

### 4. Download Result

Once done, click 📥 **Download Redacted PDF** to save your sanitized file.

---

## 🔐 How It Works

### 🧩 Native Text Search

* Scans the PDF’s text layer for matches (case-insensitive).
* Applies redaction annotations with solid black fill.
* **Deletes** the underlying text to prevent selection or extraction.

### 🧠 OCR Processing

* Converts each page to a 300 DPI image.
* Runs Tesseract OCR to detect visible text on scanned or image-based pages.
* Maps bounding boxes to PDF coordinates.
* Blackens and removes those areas permanently.

### 🏁 Output

* Produces a new PDF where all sensitive data is **irreversibly removed**.
* Text cannot be selected, copied, or recovered — ensuring total privacy.

---

## 🌱 Future Improvements

* Fuzzy matching for similar keywords (e.g., `passwrd` → `password`).
* Multi-language OCR support.
* Batch (bulk) PDF processing.
* Optional cloud deployment mode.

---

## ❗ Important Notes

* **Redacted areas are permanently removed** — keep a backup of your original PDF before processing.
* OCR accuracy depends on the quality of the scanned document.
* Ensure Tesseract is correctly installed and configured for your operating system.

---

## 🧠 Update Summary (October 2025)

* 🔥 **Real redaction logic added** — text is now **permanently deleted**, not just covered.
* 🧾 Enhanced **regex search** for better keyword matching.
* 🧍‍♂️ Improved **OCR precision** with DPI scaling and coordinate correction.
* ⚡ Optimized processing loop for faster performance.
* 🧹 Clean memory handling and compressed final output for smaller PDF size.

---

> Built with ❤️ by [Vaibhav Madaan](https://github.com/whybhav360)

```

