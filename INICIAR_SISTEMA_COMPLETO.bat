@echo off
title SISTEMA REP COMPLETO - Inicio Automatico
echo =====================================
echo  🌱 SISTEMA REP - INICIO COMPLETO
echo =====================================
echo.

echo 🚀 Iniciando Sistema REP Completo...
echo.

echo 📊 COMPONENTES A INICIAR:
echo    1. Servidor REP (Flask)
echo    2. Aplicacion Desktop (tkinter)
echo.

echo ⚡ PASO 1: Iniciando Servidor REP...
echo.

start "Servidor REP" cmd /c "cd /d android_app\server && INICIAR_SERVIDOR_REP.bat"

echo ✅ Servidor iniciado en ventana separada
echo.

echo ⏰ Esperando 5 segundos para que el servidor se inicie...
timeout /t 5 /nobreak >nul

echo.
echo ⚡ PASO 2: Iniciando Aplicacion Desktop...
echo.

cd desktop_app
start "Desktop REP" cmd /c "EJECUTAR_SISTEMA_REP.bat"

echo ✅ Aplicacion Desktop iniciada
echo.

echo =====================================
echo 🎉 SISTEMA REP COMPLETO INICIADO
echo =====================================
echo.
echo 📱 COMPONENTES ACTIVOS:
echo    • ✅ Servidor REP (android_app\server)
echo    • ✅ Desktop App (desktop_app)
echo.
echo 🔗 APLICACIONES MOVILES:
echo    • Scanner App (Android) - Listo para conectar
echo    • App Sustentable (Android) - Listo para conectar
echo.
echo 🌐 URL DEL SERVIDOR:
echo    http://192.168.5.53:5000
echo    (o http://localhost:5000 si hay problemas)
echo.
echo 💡 INSTRUCCIONES:
echo    1. Espera a que aparezcan ambas ventanas
echo    2. Verifica conexion en Desktop App
echo    3. Si hay errores, revisa firewall
echo    4. Apps Android deben usar misma WiFi
echo.
echo 🔴 Para detener: Cierra las ventanas del servidor y desktop
echo.
echo =====================================
pause