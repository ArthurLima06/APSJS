@echo off
title Iniciando servidor local + Ngrok
echo ===============================
echo Iniciando servidor local na porta 5500...
echo ===============================

REM Abre o Live Server pelo Node.js se ele não estiver rodando
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5500" ^| find "LISTENING"') do set PID=%%a
if not defined PID (
    echo Live Server nao detectado. Abrindo servidor local manualmente...
    start "" cmd /c "npx live-server --port=5500"
    echo Aguardando o Live Server iniciar...
    timeout /t 5 >nul
) else (
    echo Live Server ja esta rodando na porta 5500.
)

echo ===============================
echo Iniciando ngrok na porta 5500...
echo ===============================
start "" cmd /c "ngrok http 5500"
echo Link publico sera exibido na janela do ngrok.
pause
