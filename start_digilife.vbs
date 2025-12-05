Set WshShell = CreateObject("WScript.Shell")
strPath = WshShell.CurrentDirectory

' Start Backend (Hidden)
WshShell.Run "cmd /c cd /d """ & strPath & "\backend"" && uvicorn main:app --reload", 0

' Wait 3 seconds for backend to initialize
WScript.Sleep 3000

' Start Frontend (Hidden window, but opens Browser)
WshShell.Run "cmd /c cd /d """ & strPath & "\frontend"" && npm run dev -- --open", 0
