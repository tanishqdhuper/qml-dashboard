@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\streamlit.exe (
  echo Virtual environment not found. Run the installation commands in README.md first.
  pause
  exit /b 1
)
.venv\Scripts\streamlit.exe run app.py
