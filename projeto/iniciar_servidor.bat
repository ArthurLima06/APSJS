@echo off
echo ===============================
echo Iniciando servidor local (Live Server)...
echo ===============================

REM Abre o VS Code e inicia o Live Server automaticamente
start "" "C:\Program Files\Microsoft VS Code\Code.exe" .

echo Aguarde alguns segundos para o servidor iniciar...
timeout /t 5 >nul

echo ===============================
echo Iniciando ngrok na porta 5500...
echo ===============================

start cmd /k "ngrok http 5500"

echo Tudo pronto! O servidor e o ngrok estao rodando.
pause
start "" "https://127.0.0.1:5500"
