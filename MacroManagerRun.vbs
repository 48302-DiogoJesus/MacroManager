Set WshShell = CreateObject("WScript.Shell")
scriptDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDirectory
WshShell.Run "cmd /c set PATH=%appdata%\nodejs;%PATH% && npm install", 0, True
WshShell.Run "cmd /c set PATH=%appdata%\nodejs;%PATH% && npm run dev", 0, False
