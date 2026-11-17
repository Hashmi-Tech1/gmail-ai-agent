@echo off
REM Runs the agent once from this folder and appends output to log.txt
cd /d "%~dp0"
echo ===== %date% %time% ===== >> log.txt
venv\Scripts\python classify_emails.py >> log.txt 2>&1
venv\Scripts\python reply_drafts.py >> log.txt 2>&1
