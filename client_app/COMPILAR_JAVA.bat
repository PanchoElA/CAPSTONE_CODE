@echo off
echo =====================================
echo  CONFIGURANDO JAVA_HOME Y COMPILANDO
echo =====================================
echo.

REM Buscar Java en ubicaciones comunes
set JAVA_CANDIDATES=
set JAVA_CANDIDATES=%JAVA_CANDIDATES% "%ProgramFiles%\Java\jdk*"
set JAVA_CANDIDATES=%JAVA_CANDIDATES% "%ProgramFiles%\OpenJDK\jdk*"
set JAVA_CANDIDATES=%JAVA_CANDIDATES% "%ProgramFiles%\Eclipse Adoptium\jdk*"
set JAVA_CANDIDATES=%JAVA_CANDIDATES% "%ProgramFiles(x86)%\Java\jdk*"

echo 🔍 Buscando instalacion de Java...

REM Verificar si java esta en PATH
java -version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Java encontrado en PATH
    for /f "tokens=*" %%i in ('where java') do (
        echo    Java ubicado en: %%i
        set "JAVA_PATH=%%i"
        goto :found_java
    )
)

REM Buscar en Program Files
for /d %%D in ("%ProgramFiles%\Java\jdk*") do (
    if exist "%%D\bin\java.exe" (
        echo ✅ Java encontrado en: %%D
        set "JAVA_HOME=%%D"
        set "JAVA_PATH=%%D\bin\java.exe"
        goto :found_java
    )
)

for /d %%D in ("%ProgramFiles%\Eclipse Adoptium\jdk*") do (
    if exist "%%D\bin\java.exe" (
        echo ✅ Java encontrado en: %%D
        set "JAVA_HOME=%%D"
        set "JAVA_PATH=%%D\bin\java.exe"
        goto :found_java
    )
)

echo ❌ JAVA NO ENCONTRADO
echo.
echo Para compilar necesitas:
echo 1. Instalar Java JDK 11 o superior
echo 2. O usar Android Studio que incluye JDK
echo.
echo Descarga Java desde:
echo https://adoptium.net/
echo.
pause
exit /b 1

:found_java
echo.
echo 🚀 COMPILANDO CON GRADLE...
echo.

REM Configurar JAVA_HOME si no esta configurado
if not defined JAVA_HOME (
    for %%i in ("%JAVA_PATH%") do set "JAVA_HOME=%%~dpi.."
)

echo JAVA_HOME: %JAVA_HOME%
echo.

REM Compilar
gradlew.bat assembleDebug

if %errorlevel% == 0 (
    echo.
    echo ✅ COMPILACION EXITOSA!
    echo.
    echo 📱 APK generado en:
    echo app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo 🎯 Para instalar en Android:
    echo 1. Transferir APK al dispositivo
    echo 2. Habilitar "Fuentes desconocidas"
    echo 3. Instalar APK
    echo.
) else (
    echo.
    echo ❌ ERROR EN COMPILACION
    echo Ver errores arriba para detalles
    echo.
)

pause