Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDirectory = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
WshShell.CurrentDirectory = scriptDirectory
WshShell.Run "python main.py ..\editor\Code.exe", 0, True
