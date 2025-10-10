@echo off
title Calculadora Carbono - Inicialização Automática
echo ===============================================
echo  ABRINDO CALCULADORA DE CARBONO AUTOMATICAMENTE
echo ===============================================
echo.

REM --- 1. Abrir VS Code no projeto ---
echo Iniciando VS Code...
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "C:\Users\%USERNAME%\Documents\projeto"
timeout /t 5 >nul

REM --- 2. Iniciar o Live Server manualmente dentro do VS Code ---
echo Certifique-se de que o Live Server foi iniciado na porta 5500.
echo.
echo Aguarde 5 segundos...
timeout /t 5 >nul

REM --- 3. Iniciar o ngrok e capturar o link público ---
echo Iniciando ngrok...
for /f "tokens=2 delims= " %%a in ('start /b ngrok http 5500 ^| findstr /r "https://.*ngrok-free.app"') do (
    set "URL=%%a"
)

REM --- Espera o ngrok gerar o link ---
timeout /t 7 >nul

REM --- 4. Capturar o link público corretamente ---
for /f "tokens=2 delims= " %%i in ('curl -s http://127.0.0.1:4040/api/tunnels ^| findstr /r "https://.*ngrok-free.app"') do (
    set "URL=%%i"
)

REM --- 5. Abrir no navegador ---
if defined URL (
    echo Link público encontrado: %URL%
    echo Abrindo no navegador...
    start "" %URL%
) else (
    echo ERRO: Não foi possível capturar o link do ngrok.
    echo Abra manualmente em http://127.0.0.1:4040 para ver o link.
)

echo.
pause
