@echo off
echo 🌱 SISTEMA REP - INICIO COMPLETO
echo ================================

echo 📡 Iniciando servidor...
cd /d "%~dp0"
start "Servidor REP" python server_rep.py

timeout /t 3 /nobreak >nul

echo 💻 Iniciando aplicación de escritorio...
cd desktop_app
start "Desktop App" python desktop_app.py

echo ✅ Sistema iniciado:
echo    📡 Servidor: http://192.168.5.53:5000
echo    💻 Desktop App: Ventana abierta
echo    📱 Scanner App: Conectar a http://192.168.5.53:5000

pause