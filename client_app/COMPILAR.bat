@echo off
echo =====================================
echo   COMPILADOR CLIENTE REP - Android  
echo =====================================
echo.
echo Instrucciones para Android Studio:
echo.
echo 1. Abrir Android Studio
echo 2. File ^> Open ^> Seleccionar esta carpeta
echo 3. Sync Now (esperar sincronizacion)
echo 4. Build ^> Build APK
echo 5. APK generado en: app\build\outputs\apk\debug\
echo.
echo =====================================
echo Presiona cualquier tecla para abrir
echo la carpeta del proyecto...
echo =====================================
pause
start explorer "%~dp0"
echo.
echo =====================================
echo Presiona cualquier tecla para abrir  
echo la carpeta de APKs (despues de compilar)
echo =====================================
pause
start explorer "%~dp0app\build\outputs\apk\debug\"