import os
import subprocess
import sys

def SelfUpdate():
    github_repo_url = "https://github.com/48302-DiogoJesus/DesktopMacroFramework"
    update_command = f"pip install --upgrade --force-reinstall git+{github_repo_url} && pythonw {os.path.abspath(sys.argv[0])} {' '.join(sys.argv[1:])}"
    
    print("Update Command", update_command)

    try:
        # Run the pip command in a separate process
        subprocess.Popen(update_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        pass
    finally:
        sys.exit()