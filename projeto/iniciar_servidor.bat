@echo off
title Calculadora de Carbono - Inicialização Automática
echo ==============================================
echo ABRINDO CALCULADORA DE CARBONO AUTOMATICAMENTE
echo ==============================================
echo.

:: Caminho da pasta do projeto
cd "C:\Users\IDENTIDADTECH\Desktop\VS Code\APSJS\projeto"

:: Abre o VS Code nessa pasta
echo Iniciando VS Code...
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe" .

echo Certifique-se de que o Live Server foi iniciado na porta 5500.
echo Aguarde 5 segundos...
timeout /t 5 >nul

:: Inicia o ngrok na porta 5500
echo Iniciando ngrok...
start cmd /k "ngrok http 5500"

echo.
echo Tudo pronto! O servidor local e o ngrok estão rodando.
pause
