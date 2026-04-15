@echo off
title Ejecucion Automatica Banorte
color 0B
cls
echo ==============================================
echo       AUTOMATIZACION DE SINIESTROS
echo ==============================================
echo.
echo Iniciando el proceso completo...
echo Por favor, no toques el telefono...
echo.

call .venv\Scripts\activate
python main.py

pause
exit