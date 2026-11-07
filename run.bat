@echo off
title Verity: News Credibility and Misinformation Analyzer
echo ========================================================
echo   Starting Verity NLP Web Application...
echo ========================================================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" server.py
) else (
    python server.py
)
pause
