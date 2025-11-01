Set WshShell = CreateObject("WScript.Shell")

' --- Check if Streamlit is already running ---
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colItems = objWMIService.ExecQuery("Select * from Win32_Process Where Name='python.exe' OR Name='streamlit.exe'")

isRunning = False
For Each objItem In colItems
    If InStr(LCase(objItem.CommandLine), "streamlit") > 0 Then
        isRunning = True
        Exit For
    End If
Next

' --- If not running, start it silently ---
If Not isRunning Then
    WshShell.Run "cmd /c StartWebAppLAN.bat", 0, False
    WScript.Sleep 6000 ' wait for server startup
End If

' --- Get local IP (prefer 192.168.x.x or 10.x.x.x) ---
Set execObj = WshShell.Exec("cmd /c ipconfig | findstr /R ""IPv4""")
ip = ""
Do Until execObj.StdOut.AtEndOfStream
    line = execObj.StdOut.ReadLine
    If InStr(line, "192.168.") > 0 Or InStr(line, "10.") > 0 Then
        parts = Split(line, ":")
        ip = Trim(parts(1))
        Exit Do
    End If
Loop

If ip = "" Then ip = "localhost"

' --- Open browser ---
url = "http://" & ip & ":8501"
WshShell.Run url
