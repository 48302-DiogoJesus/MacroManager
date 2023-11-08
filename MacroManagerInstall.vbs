' Add script to Startup
Set WshShell = CreateObject("WScript.Shell")
scriptDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
scriptFileName = "MacroManagerRun.vbs"
scriptPath = scriptDirectory & "\" & scriptFileName
registryKeyPath = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run"
registryEntryName = "Macro Manager App"
WshShell.RegWrite registryKeyPath & "\" & registryEntryName, """" & scriptPath & """", "REG_SZ"
