@echo off
echo Stopping DigiLife...
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
echo Done.
pause
