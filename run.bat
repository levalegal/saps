@echo off
chcp 65001 > nul
echo ========================================
echo   Каталог контактов сотрудников
echo ========================================
echo.

if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
    echo.
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

if not exist "venv\Lib\site-packages\PyQt6" (
    echo Установка зависимостей...
    pip install -r requirements.txt
    echo.
)

echo Запуск приложения...
echo.
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ошибка при запуске приложения!
    pause
)




