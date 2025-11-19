@echo off
title SweetCookies - Instalacion
color 0B

echo ========================================
echo    SweetCookies - Instalacion
echo ========================================
echo.
echo Instalando dependencias...
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo    Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo    - Doble clic en ejecutar.bat
echo    - O ejecuta: python app.py
echo.

pause