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

:: Inicia o ngrok e captura o link
echo Iniciando ngrok na porta 5500...
for /f "tokens=2 delims= " %%A in ('ngrok http 5500 --log=stdout ^| find "url="') do (
    set "URL=%%A"
    goto abrir
)

:abrir
:: Abre o navegador com o link público (se encontrado)
if defined URL (
    echo Abrindo no navegador: %URL%
    start "" %URL%
) else (
    echo Nao foi possivel capturar o link automaticamente.
    echo Abra manualmente o link exibido no prompt do ngrok.
)

echo.
echo Tudo pronto! O servidor local e o ngrok estão rodando.
pause
