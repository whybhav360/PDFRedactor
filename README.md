🔒 PDF Redaction Tool

A Streamlit-based web application that allows you to securely redact sensitive information from PDF files.
It supports both native text redaction and OCR-based detection, ensuring even scanned documents are thoroughly sanitized.

🚀 Features

✅ Keyword-based Redaction
Enter one or more keywords to automatically detect and redact them.

✅ Dual Detection Method

Native PDF text search

OCR (Optical Character Recognition) using Tesseract for scanned PDFs or images

✅ Dynamic Keyword Management

Add keywords via input

Remove keywords using ❌ chips

✅ High-Resolution OCR Processing

Uses 300 DPI rendering for precise OCR bounding boxes

✅ Progress Tracking

Real-time progress bar for large PDFs

✅ Instant Download

Download the final redacted PDF directly from the browser


⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/whybhav360/PDFRedactor.git
cd pdf-redactor

2. Create Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Install Tesseract
🪟 Windows

Download Tesseract OCR

Default install path used in code:

C:\Program Files\Tesseract-OCR\tesseract.exe

🍎 Mac (Homebrew)
brew install tesseract

▶️ Running the Application
Option 1 — Simple (Command Line)
streamlit run app.py

Then open: http://localhost:8501

Option 2 — 🔗 Local LAN Hosting (For Team Use)

Run on your own PC and share with devices on the same Wi-Fi/LAN — completely private.

🧩 Step 1: Add these two files in your project folder

StartWebAppLAN.bat (Check for the right path before launching)

@echo off
cd /d "C:\Users\user\Documents\webapp" 
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 >nul 2>&1


LaunchWebApp.vbs

Set WshShell = CreateObject("WScript.Shell")

' Check if Streamlit is already running
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colItems = objWMIService.ExecQuery("Select * from Win32_Process Where Name='python.exe' OR Name='streamlit.exe'")
isRunning = False
For Each objItem In colItems
    If InStr(LCase(objItem.CommandLine), "streamlit") > 0 Then
        isRunning = True
        Exit For
    End If
Next

' Start silently if not already running
If Not isRunning Then
    WshShell.Run "cmd /c StartWebAppLAN.bat", 0, False
    WScript.Sleep 6000
End If

' Detect local IP (192.168.x.x or 10.x.x.x)
Set execObj = WshShell.Exec("cmd /c ipconfig | findstr /R ""IPv4""")
ip = ""
Do Until execObj.StdOut.AtEndOfStream
    line = execObj.StdOut.ReadLine
    If InStr(line, "192.168.") > 0 Or InStr(line, "10.") > 0 Then
        parts = Split(line, ":")
        ip = Trim(parts(1))
        Exit Do
    End If
Loop
If ip = "" Then ip = "localhost"

' Open browser
url = "http://" & ip & ":8501"
WshShell.Run url

🖱️ Step 2: Run the App

Double-click LaunchWebApp.vbs — it will:

Start the server silently in the background

Detect your local IP

Open the correct URL automatically

Example: http://192.168.1.7:8501

Now anyone on your Wi-Fi can open that same address 🎉

💻 Usage

Upload PDF — Drag and drop your file.

Enter Keywords — Type and press Enter.

Remove Keywords — Click ❌ on any chip.

Start Redaction — Click 🚀 and wait.

Download Result — Click 📥 to save the redacted PDF.

🔐 How It Works

1️⃣ Native Text Search — Finds keyword matches directly in the PDF text layer.
2️⃣ OCR Processing — For scanned PDFs:

Converts each page to 300 DPI image

Runs Tesseract OCR

Maps detected text back to PDF coordinates
3️⃣ Output — Creates a clean, permanent redacted PDF.

🌱 Future Improvements (Open to PRs)

Fuzzy keyword matching (e.g., “passwrd” ≈ “password”)

Multi-language OCR support

Batch PDF processing

Optional cloud deployment

❗ Important Notes

Redacted areas cannot be recovered, so keep an original backup.

OCR accuracy depends on scan quality.

Ensure Tesseract is installed and configured correctly.

LAN hosting keeps data completely private — files never leave your comp

Vibe coded with a lot of bug smashing by yours truly,

Vaibhav Madaan
(Look me up on linkedin)

