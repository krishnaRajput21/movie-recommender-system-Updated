@echo off
REM Run this from the PROJECT ROOT folder (the one that contains
REM backend\, frontend\, and venv_v2\).

echo Starting FastAPI backend in a new window...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && call ..\venv_v2\Scripts\activate.bat && uvicorn main:app --reload"

echo Waiting a few seconds for the backend to come up...
timeout /t 4 /nobreak >nul

echo Starting Streamlit frontend in this window...
cd /d %~dp0frontend
call ..\venv_v2\Scripts\activate.bat
streamlit run app.py
