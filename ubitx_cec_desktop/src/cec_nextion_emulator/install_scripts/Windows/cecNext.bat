@echo off
SET "VENV_DIR=Documents\CEC\Scripts"
SET "SCRIPT_DIR=%USERPROFILE%\%VENV_DIR%"
CALL "%SCRIPT_DIR%\activate.bat"
python "-m" "cec_nextion_emulator.CECNextionEmulator"
