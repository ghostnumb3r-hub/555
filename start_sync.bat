@echo off
cd /d "C:\Users\valen\555"
echo ⚡ Avvio Sync Sistema 555...
python -c "import sync_system; sync = sync_system.SalvataggieSync('https://five55-mdye.onrender.com'); sync.start_continuous_sync()"
pause
