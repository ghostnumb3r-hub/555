@echo off
title 555 Dashboard - Google Drive
color 0A

echo.
echo ========================================
echo    🚀 DASHBOARD 555 - GOOGLE DRIVE
echo ========================================
echo.
echo 📁 Posizione: H:\Il mio Drive\555\
echo 💾 Salvataggi: Automatici su Google Drive  
echo 🌐 Server: Locale (porta 8050)
echo.
echo Avvio dashboard...
echo.

cd /d "H:\Il mio Drive\555"
python 555.py

echo.
echo ========================================
echo Dashboard chiusa. Premi un tasto...
echo ========================================
pause
