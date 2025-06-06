@echo off
echo ============================================
echo Running 002_SGFCMed_benign_Update_06_06_2025.py in a new window...
echo ============================================
cd /d C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\CODE_02
start "SGFCMed_benign" cmd /k "python 002_SGFCMed_benign_Update_06_06_2025.py"

echo ============================================
echo Running 002_SGFCMed_malware_Update_06_06_2025.py in a new window...
echo ============================================
cd /d C:\Users\BMEi\Documents\GitHub\WORK\Windows\CODE_BME\PROJECT_CYBER_SECURITY\CODE_02
start "SGFCMed_malware" cmd /k "python 002_SGFCMed_malware_Update_06_06_2025.py"

echo ============================================
echo Both scripts are running in separate windows...
echo ============================================

pause