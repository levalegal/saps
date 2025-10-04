@echo off
chcp 65001 > nul
cd /d "%~dp0dist"
echo Starting EmployeeDirectory_Premium.exe...
echo.
.\EmployeeDirectory_Premium.exe
echo.
echo Application closed or crashed.
echo Press any key to exit...
pause > nul
