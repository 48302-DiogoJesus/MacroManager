' Create an object for WMI service
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")

' Query the processes with names containing "python"
Set colProcesses = objWMIService.ExecQuery("SELECT * FROM Win32_Process WHERE Name LIKE '%python%'")

' Loop through each process and terminate it
For Each objProcess in colProcesses
    objProcess.Terminate()
Next
