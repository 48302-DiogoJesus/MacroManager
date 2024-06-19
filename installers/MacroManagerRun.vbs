Set WshShell = CreateObject("WScript.Shell")
scriptDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDirectory
WshShell.Run "venv\Scripts\pythonw.exe main.py", 0, True
