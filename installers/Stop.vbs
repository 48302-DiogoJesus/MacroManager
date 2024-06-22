Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
Set colProcesses = objWMIService.ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'python.exe'")

For Each objProcess in colProcesses
    ' Check the command line to find the right process
    If InStr(LCase(objProcess.CommandLine), "main.py") > 0 Then
        ' Terminate the process
        objProcess.Terminate()
    End If
Next
