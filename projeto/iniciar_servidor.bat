@echo off
echo Iniciando VS Code e Live Server...
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe" .
timeout /t 5 >nul

echo Iniciando ngrok na porta 5500...
start cmd /k "ngrok http 5500"

echo Aguardando 7 segundos para ngrok iniciar...
timeout /t 7 >nul

echo Abrindo link público do ngrok no navegador...
start "" "https://illiberal-unnecessarily-jeannette.ngrok-free.dev"

pause
