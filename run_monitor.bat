```bat
@echo off

cd /d "C:\Users\siddh\OneDrive\Desktop\AI Bussiness Anamoly Monitor"

call "venv\Scripts\activate.bat"

python scheduled_analysis.py

deactivate

exit /b %ERRORLEVEL%
```
