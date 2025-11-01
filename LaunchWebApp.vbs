Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c StartWebAppLAN.bat", 0, False

' Wait a few seconds for the server to start
WScript.Sleep 5000

Set objShell = CreateObject("WScript.Shell")

' Find local IP
Set execObj = objShell.Exec("cmd /c for /f ""tokens=2 delims=: "" %A in ('ipconfig ^| findstr IPv4') do @echo %A")
Do While execObj.Status = 0
    WScript.Sleep 100
Loop

ip = Trim(execObj.StdOut.ReadAll)
url = "http://" & ip & ":8501"
objShell.Run url
