@echo off
chcp 65001 > nul
echo ========================================
echo   Установка приложения
echo ========================================
echo.

echo Проверка Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Python не установлен!
    echo Установите Python 3.8 или выше с https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Создание виртуального окружения...
python -m venv venv

echo.
echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo   Установка завершена!
echo ========================================
echo.
echo Для запуска приложения используйте: run.bat
echo.
pause




