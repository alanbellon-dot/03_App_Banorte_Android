@echo off
title Menu de Automatizacion Banorte
color 0B

:menu
cls
echo ==============================================
echo       AUTOMATIZACION DE SINIESTROS
echo ==============================================
echo.
echo Selecciona el modulo a ejecutar:
echo.
echo 1. Declaraciones
echo 2. Asegurado
echo 3. Deslinde de Responsabilidad
echo 4. Estimacion Danos y Lesiones
echo 5. Terceros
echo 6. Volantes Digitales
echo 7. Cierre
echo 8. Realizar toda la operacion
echo.
echo 0. Salir
echo.
set /p opcion="Ingresa el numero de tu opcion: "

if "%opcion%"=="1" goto ejecutar_python
if "%opcion%"=="2" goto ejecutar_python
if "%opcion%"=="3" goto ejecutar_python
if "%opcion%"=="4" goto ejecutar_python
if "%opcion%"=="5" goto ejecutar_python
if "%opcion%"=="6" goto ejecutar_python
if "%opcion%"=="7" goto ejecutar_python
if "%opcion%"=="8" goto ejecutar_python
if "%opcion%"=="0" goto salir

echo Opcion no valida, intenta de nuevo.
pause
goto menu

:ejecutar_python
echo.
echo Iniciando automatizacion para la opcion %opcion%...
echo Por favor, no toques el telefono...
echo.
REM Aqui llamamos a tu entorno virtual y ejecutamos el main.py pasandole el numero
call .venv\Scripts\activate
python main.py %opcion%
pause
goto menu

:salir
exit