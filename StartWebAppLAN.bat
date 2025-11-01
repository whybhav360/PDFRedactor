@echo off
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr "IPv4"') do set ip=%%A
set ip=%ip: =%

cd /d "C:\Users\Vaibhav\Documents\webapp"
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 >nul 2>&1
