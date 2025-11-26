Set WshShell = CreateObject("WScript.Shell")
' Launch the batch file invisibly (0 = Hide Window)
WshShell.Run chr(34) & "run_background.bat" & Chr(34), 0
Set WshShell = Nothing
