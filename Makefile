SHELL := cmd.exe

run:
	python.exe main.py

updatefrontend:
	cd ../frontend && npm run build && cp build/index.html ../backend/templates/ && cp -r build/_app ../backend/static/

# On "dev" machine
updatereqs:
	pipreqs --force .

# On "target" machine
installreqs:
	pip install -r requirements.txt

# should NOT BE NEEDED, as it can be done via "Macro Manager" Web interface
updateautomation:
	pip install --upgrade --force-reinstall git+https://github.com/48302-DiogoJesus/DesktopMacroFramework