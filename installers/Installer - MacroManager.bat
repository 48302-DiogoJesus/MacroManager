@echo off

echo [Macro Manager Installation - You only need to run this once]
echo.
pause

echo.
echo [1) Download Macro Manager from GitHub]
echo.
pause
git clone https://github.com/48302-DiogoJesus/MacroManager/

echo.
echo [2) Install Macro Manager (run at system startup)]
echo.
pause
cscript MacroManager/installers/MacroManagerInstall.vbs

echo.
echo [3) Run Macro Manager]
echo.
pause
cscript MacroManager/installers/MacroManagerRun.vbs

echo.
echo [DONE] Running on http://localhost:8181/
echo.
pause
