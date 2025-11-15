@echo off
echo ========================================
echo   CYBERGUARD SV - INICIAR DASHBOARD
echo ========================================
echo.

cd /d "%~dp0"
cd dashboard

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado
    pause
    exit /b 1
)

echo.
echo Iniciando servidor...
echo.
python app_integrated.py

pause

