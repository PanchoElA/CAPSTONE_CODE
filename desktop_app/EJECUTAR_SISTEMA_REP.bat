@echo off
title SISTEMA REP - Aplicacion de Escritorio
echo =====================================
echo  🌱 SISTEMA REP - GESTION SUSTENTABLE
echo =====================================
echo.
echo 🔧 Verificando Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado
    echo.
    echo Para ejecutar esta aplicacion necesitas:
    echo 1. Instalar Python 3.8 o superior
    echo 2. Descargar desde: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado

echo.
echo 🔧 Instalando dependencias...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo ⚠️ Error instalando dependencias
    echo Intentando instalacion manual...
    pip install requests qrcode[pil] Pillow --quiet
)

echo ✅ Dependencias instaladas

echo.
echo 🚀 Iniciando Sistema REP Desktop...
echo.
echo 💡 FUNCIONALIDADES:
echo    • Generar QRs CODELPA/TERCERO
echo    • Dashboard con estadisticas
echo    • Consulta de clientes
echo    • Reportes mensuales
echo    • Exportacion CSV
echo.
echo 🔗 CONECTADO A:
echo    • App Scanner Android
echo    • App Sustentable Android
echo    • Servidor REP centralizado
echo.
echo =====================================

python sistema_rep_desktop.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error ejecutando la aplicacion
    pause
)

echo.
echo 👋 Sistema REP Desktop cerrado
pause