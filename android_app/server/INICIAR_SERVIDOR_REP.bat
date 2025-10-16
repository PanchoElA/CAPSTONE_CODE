@echo off
title SERVIDOR REP - Sistema Sustentable
echo =====================================
echo  🌱 SERVIDOR REP - INICIANDO
echo =====================================
echo.

echo 🔧 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo 🔧 Instalando dependencias Flask...
pip install flask flask-cors --quiet

echo ✅ Dependencias instaladas
echo.

echo 🔥 Configurando Firewall (requiere permisos de administrador)...
netsh advfirewall firewall delete rule name="Python REP Server" >nul 2>&1
netsh advfirewall firewall add rule name="Python REP Server" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ Firewall configurado - Puerto 5000 abierto
) else (
    echo ⚠️ No se pudo configurar firewall automáticamente
    echo   Ejecuta como administrador para abrir puerto 5000
)

echo.
echo 🌐 Obteniendo IP del PC...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr "IPv4"') do set IP=%%i
set IP=%IP: =%
echo ✅ IP detectada: %IP%

echo.
echo 🚀 INICIANDO SERVIDOR REP...
echo.
echo 📱 Las aplicaciones deben conectarse a:
echo    http://%IP%:5000
echo.
echo 💡 APLICACIONES CONECTADAS:
echo    • Desktop App (este PC)
echo    • Scanner App (Android)  
echo    • App Sustentable (Android)
echo.
echo ⚠️ IMPORTANTE:
echo    • Mantén esta ventana abierta
echo    • Todas las apps deben estar en la misma WiFi
echo    • Presiona Ctrl+C para detener el servidor
echo.
echo =====================================
echo 🟢 SERVIDOR REP ACTIVO
echo =====================================
echo.

python app.py

echo.
echo 🔴 Servidor REP detenido
pause