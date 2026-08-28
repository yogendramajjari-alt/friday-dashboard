' FRIDAY / JARVIS Dashboard Mirror - auto-start at login (hidden, no console).
' Runs via run_hidden.bat (console python.exe, output redirected to a log
' file) rather than pythonw.exe directly -- consistent with this workspace's
' established pattern (pythonw's stdout=None crashes on any print() before
' the port ever binds).
' This is the template. The ACTIVE copy lives in your Startup folder:
'   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\FridayJarvisDashboard.vbs
' Edit the paths below if you move the project, then copy this file into the
' Startup folder. Delete it there to disable auto-start.
Dim shell
Set shell = CreateObject("WScript.Shell")

' Kill anything already on port 9100 first (avoid "address in use" on relaunch)
shell.Run "cmd /c for /f ""tokens=5"" %a in ('netstat -aon ^| find "":9100""') do taskkill /PID %a /F", 0, True
WScript.Sleep 1000

shell.Run """C:\Users\yogendra.majjari\.claude\EPR\jarvis-dashboard\autostart\run_hidden.bat""", 0, False
