updatebuild:
	cp ../frontend/build/index.html templates/ && cp -r ../frontend/build/_app static/

updatereqs:
	pipreqs --force .

installreqs:
	venv/Scripts/pip.exe install -r requirements.txt

updateautomation:
	venv/Scripts/pip.exe install --upgrade --force-reinstall git+https://github.com/48302-DiogoJesus/DesktopMacroFramework