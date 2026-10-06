@echo off
echo ===================================================
echo   Starting MudraAI Cloudflare HTTPS Tunnel
echo   (No Account / No Token Required)
echo ===================================================
echo.
D:\tools\cloudflared.exe tunnel --url http://127.0.0.1:5000
pause
