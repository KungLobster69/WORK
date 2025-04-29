@echo off
echo ============================================
echo Running 001_sgFCMed_Full_benign.py ...
echo ============================================
cd /d C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY
start "" python 001_sgFCMed_Full_benign.py

echo ============================================
echo Running 001_sgFCMed_Full_malware.py ...
echo ============================================
start "" python 001_sgFCMed_Full_malware.py

echo ============================================
echo Both scripts are running in parallel ...
echo ============================================

pause
