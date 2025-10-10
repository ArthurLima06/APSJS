@echo off
echo ======================================
echo Iniciando servidor local (Live Server)...
echo ======================================

REM 🔹 Abra o VS Code no diretório atual
REM ⚠️ Se o caminho abaixo não funcionar, troque para:
REM "C:\Program Files\Microsoft VS Code\Code.exe"
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe" .

echo Aguarde alguns segundos para o servidor iniciar...
timeout /t 5 >nul

echo ======================================
echo Iniciando ngrok na porta 5500...
echo ======================================

REM 🔹 Inicia o ngrok em uma nova janela de CMD
start cmd /k "ngrok http 5500"

echo ======================================
echo Tudo pronto! O servidor e o ngrok estão rodando.
echo ======================================

REM 🔹 Aguarda alguns segundos para o ngrok iniciar e gerar o link
timeout /t 7 >nul

REM 🔹 Tenta abrir automaticamente a interface web do ngrok (opcional)
start "" http://127.0.0.1:4040

echo Abra o link público exibido no terminal do ngrok.
pause
