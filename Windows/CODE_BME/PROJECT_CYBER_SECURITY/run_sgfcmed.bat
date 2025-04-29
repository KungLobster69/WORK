@echo off
echo ============================================
echo Running 001_sgFCMed_Full_benign.py in a new window...
echo ============================================
cd /d C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY
start "Benign Window" cmd /k "python 001_sgFCMed_Full_benign.py"

echo ============================================
echo Running 001_sgFCMed_Full_malware.py in a new window...
echo ============================================
start "Malware Window" cmd /k "python 001_sgFCMed_Full_malware.py"

echo ============================================
echo Both scripts are running in separate windows...
echo ============================================

pause