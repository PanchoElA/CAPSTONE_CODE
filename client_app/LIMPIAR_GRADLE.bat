@echo off
echo =====================================
echo  LIMPIEZA Y REPARACION GRADLE
echo =====================================
echo.
echo 🔧 LIMPIANDO CACHE GRADLE...
rmdir /s /q "%USERPROFILE%\.gradle\caches" 2>nul
echo ✅ Cache limpiado
echo.
echo 🔧 ELIMINANDO ARCHIVOS BUILD...
rmdir /s /q "app\build" 2>nul
rmdir /s /q "build" 2>nul
rmdir /s /q ".gradle" 2>nul
echo ✅ Archivos build eliminados
echo.
echo 🔧 CONFIGURACION ACTUALIZADA:
echo    - Gradle 8.4 (compatible)
echo    - Android Gradle Plugin 8.1.4
echo    - Java 11 target
echo    - Repositorios Google configurados
echo.
echo =====================================
echo 📱 PASOS PARA ANDROID STUDIO:
echo =====================================
echo.
echo 1. Cerrar Android Studio completamente
echo 2. Abrir Android Studio
echo 3. File > Open > Seleccionar esta carpeta
echo 4. Sync Now
echo 5. Si hay problemas:
echo    - File > Invalidate Caches and Restart
echo    - Build > Clean Project
echo    - Build > Rebuild Project
echo.
echo =====================================
pause