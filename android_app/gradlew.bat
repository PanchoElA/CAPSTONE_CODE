@echo off
setlocal
set DIRNAME=%~dp0
set APP_HOME=%DIRNAME%
"%APP_HOME%\gradle\wrapper\gradle-wrapper.jar" %*
endlocal
