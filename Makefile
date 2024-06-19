SHELL := cmd.exe

updatefrontend:
	cd ../frontend && npm run build && cp build/index.html ../backend/templates/ && cp -r build/_app ../backend/static/

# On "dev" machine
updatereqs:
	pipreqs --force .

# On "target" machine (not required if venv/ also goes)
installreqs:
	venv/Scripts/pip.exe install -r requirements.txt

# should not be needed, as it can be done via "Macro Manager" Web interface
updateautomation:
	venv/Scripts/pip.exe install --upgrade --force-reinstall git+https://github.com/48302-DiogoJesus/DesktopMacroFramework