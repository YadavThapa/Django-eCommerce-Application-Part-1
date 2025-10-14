@echo off
REM Django Management Script - Use this instead of 'python manage.py'
REM This ensures the correct Python environment is used

set PYTHON_PATH=C:\Users\hemja\OneDrive\Desktop\Ecommerce_Project\.venv\Scripts\python.exe

if "%1"=="" (
    echo Usage: django.bat [command] [arguments]
    echo.
    echo Examples:
    echo   django.bat runserver
    echo   django.bat migrate
    echo   django.bat createsuperuser
    echo   django.bat collectstatic
    echo.
    goto end
)

%PYTHON_PATH% manage.py %*

:end