from dataclasses import dataclass
from datetime import datetime
import os
import re
import shutil
import subprocess
from typing import Optional, cast

home_dir = os.path.expanduser("~")

PIP_EXEC = "venv\\Scripts\\pip.exe"
PYTHON_EXEC = "venv\\Scripts\\pythonw.exe"

# Join the home directory with "MacroManager" to form the full path
MACROS_BASE_PATH = os.path.join(home_dir, "MacroManager")
MACRO_TEMPLATE_SCRIPT_NAME = 'macro_template.py'
MACRO_TEMPLATE_SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code_templates", MACRO_TEMPLATE_SCRIPT_NAME)
MACRO_TEMPLATE_SCRIPT_DESTINATION_PATH = os.path.join(MACROS_BASE_PATH, MACRO_TEMPLATE_SCRIPT_NAME)

DEFAULT_MACRO_NAME = "macro.py"
DEFAULT_MACRO_SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code_templates", DEFAULT_MACRO_NAME)

PYTHON_FRAMEWORK_NAME = "DesktopAutomationFramework"
PythonFrameworkGithubVersionFile = "https://raw.githubusercontent.com/48302-DiogoJesus/DesktopMacroFramework/main/version.txt"

def create_environment_if_not_exists():
	os.makedirs(MACROS_BASE_PATH, exist_ok=True)

	if not os.path.exists(MACRO_TEMPLATE_SCRIPT_DESTINATION_PATH):
		shutil.copy(MACRO_TEMPLATE_SCRIPT_PATH, MACRO_TEMPLATE_SCRIPT_DESTINATION_PATH)
  
	
	print("Environment created successfully...")

@dataclass
class Macro:
	name: str
	path: str
	last_run: Optional[str]

@dataclass
class MacroInvocationVariableMetadata:
	type: str
	accepted_values: Optional[list[str]]

@dataclass
class MacroInvocationVariablesMetadata:
	variables: dict[str, MacroInvocationVariableMetadata]

@dataclass 
class Versions:
	should_update: bool
	current_version: str
	remote_version: str

class MacroManager:
	# Returns the full path of the macro
	@staticmethod
	def create_macro(macro_name: str) -> str:
		create_environment_if_not_exists()
		folderFullPath = os.path.join(MACROS_BASE_PATH, macro_name)
		pythonFilePath = os.path.join(folderFullPath, DEFAULT_MACRO_NAME)

		# Create the macro folder
		os.makedirs(folderFullPath)
		# Copy macro template script to macro folder
		shutil.copy(DEFAULT_MACRO_SCRIPT_PATH, pythonFilePath)
		
		return pythonFilePath

	@staticmethod
	def open_macros_folder() -> None:
		os.system('explorer "' + MACROS_BASE_PATH + "\"")
			
	@staticmethod
	def open_macro_in_code_editor(absolute_macro_path: str) -> None:
		create_environment_if_not_exists()
		print(absolute_macro_path)
		os.system('code "' + os.path.dirname(absolute_macro_path) + "\"")
	
	@staticmethod
	def open_macro_in_file_explorer(absolute_macro_path: str) -> None:
		create_environment_if_not_exists()
		os.system('explorer "' + os.path.dirname(absolute_macro_path) + "\"")
		
	@staticmethod 
	def open_task_scheduler() -> None:
		create_environment_if_not_exists()
		os.system('taskschd.msc')
	
	@staticmethod
	def open_macro_template() -> None:
		create_environment_if_not_exists()
		create_environment_if_not_exists()
		os.system('code "' + MACRO_TEMPLATE_SCRIPT_DESTINATION_PATH + "\"")
	
	@staticmethod
	def get_macros_flat() -> list[Macro]:
		create_environment_if_not_exists()
		try:
			file_list: list[Macro] = []
   
			def search(directory: str):
				files = os.listdir(directory)

				for file in files:
					file_path = os.path.join(directory, file)

					if os.path.isdir(file_path):
							# Recursively search subdirectories
							search(file_path)
					elif os.path.isfile(file_path) and file.endswith('.py'):
							with open(file_path, 'r', encoding='utf-8') as f:
								file_contents = f.read()
							if '@Macro' in file_contents:
								folder_name = os.path.basename(directory)
								logs_path = os.path.join(directory, 'logs')

								last_run = None

								if os.path.exists(logs_path):
									log_files = os.listdir(logs_path)
									if log_files:
										log_files.sort(reverse=True, key=lambda x: os.path.getmtime(os.path.join(logs_path, x)))
										latest_log_file = os.path.join(logs_path, log_files[0])

										# Extract date and time from file name
										date_time_part = os.path.basename(latest_log_file).replace('.txt', '')
										date_part, time_part = date_time_part.split(' ')

										year, month, day = map(int, date_part.split('-'))
										hour, minute, second = map(int, time_part.split('.'))
										last_run = datetime(year, month, day, hour, minute, second)
										last_run = last_run.strftime('%Y-%m-%d %H:%M:%S')

								file_list.append(Macro(folder_name, file_path, last_run))

			search(MACROS_BASE_PATH)
			return [file for file in file_list if file.path != MACRO_TEMPLATE_SCRIPT_DESTINATION_PATH]
		except Exception as e:
			print(f'Error searching Python files: {e}')
			return []
		
	@staticmethod
	def get_latest_macro_logs(absolute_macro_path: str) -> list[str]:
		create_environment_if_not_exists()
		logs_folder = os.path.join(os.path.dirname(absolute_macro_path), "logs")

		if not os.path.exists(logs_folder):
				raise FileNotFoundError(f"Could not find logs folder at {logs_folder}")

		log_files = os.listdir(logs_folder)

		if not log_files:
				raise FileNotFoundError(f"No log files found in {logs_folder}")

		log_files.sort(reverse=True, key=lambda x: os.path.getmtime(os.path.join(logs_folder, x)))
		latest_log_file = os.path.join(logs_folder, log_files[0])

		with open(latest_log_file, 'r', encoding='utf-8') as f:
				log_contents = f.read().splitlines()

		return log_contents

	@staticmethod
	def get_macro_invocation_variables_metadata(absolute_macro_path: str) -> MacroInvocationVariablesMetadata:
		create_environment_if_not_exists()
		useful_lines = []
		with open(absolute_macro_path, 'r', encoding='utf-8') as file:
				for line in file:
						if "vars.getNumber(" in line or "vars.getString(" in line:
								useful_lines.append(line.strip())

		invocation_variables_metadata: MacroInvocationVariablesMetadata = MacroInvocationVariablesMetadata(variables={})

		# Process each useful line
		for line in useful_lines:
			parts = line.split("(")
			function_call = parts[0].strip()
			# ! Don't like this ! what if python framework changes ?
			if "vars.getNumber" in function_call:
				type_ = "number"
			elif "vars.getString" in function_call:
				type_ = "string"

			args = parts[1].strip()
			varname = re.search(r'"(.*?)"', args).group(1)
			args = args[args.index('"')+1:]
			
			accepted_values: list[str] | None = None
			if args.startswith(","):
				args = args[1:].strip()
				if args.startswith("accepted_values="):
					accepted_values = args.split("=")[1].strip()[1:-1].split(",")
					accepted_values = [value.strip().strip('"') for value in cast(list[str], accepted_values)]

			invocation_variables_metadata.variables[varname] = MacroInvocationVariableMetadata(type_, accepted_values)
		return invocation_variables_metadata

	@staticmethod
	def run_macro(
		absolute_macro_path: str,
		invocation_variables: dict[str, str] = {},
		time_between_instructions_s: Optional[str] = None
	) -> None:
		create_environment_if_not_exists()
		key_value_pairs = " ".join([f'{key}="{value}"' for key, value in invocation_variables.items()])
		command = f'{PYTHON_EXEC} "{absolute_macro_path}" {key_value_pairs}'
		if time_between_instructions_s:
			command += f' --interval_s={time_between_instructions_s}'
				
		os.system(command)

	@staticmethod
	def get_framework_versions() -> Versions:
		remote_version_command = f'curl {PythonFrameworkGithubVersionFile}'
		remote_version_process = subprocess.Popen(remote_version_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		remote_version_stdout, _ = remote_version_process.communicate()
		remote_version = remote_version_stdout.decode().strip()

		current_version_command = f'{PIP_EXEC} show {PYTHON_FRAMEWORK_NAME}'
		current_version_process = subprocess.Popen(current_version_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		current_version_stdout, _ = current_version_process.communicate()
		current_version_output = current_version_stdout.decode().strip()
		version_match = re.search(r'Version: (.+)', current_version_output)
		current_version = (version_match.group(1) if version_match else "").strip()
  
		return Versions(
			# Determine if update is needed
		  	should_update=current_version != remote_version if current_version != "" else False,
		  	current_version=current_version,
		  	remote_version=remote_version
	  	)

	@staticmethod
	def should_update_manager() -> bool:
		# Fetch current version (local HEAD)
		current_version_process = subprocess.Popen("git rev-parse HEAD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		current_version_stdout, _ = current_version_process.communicate()
		current_version = current_version_stdout.decode().replace("HEAD", "").strip()

		# Fetch remote version (origin HEAD)
		remote_version_process = subprocess.Popen("git ls-remote origin HEAD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		remote_version_stdout, _ = remote_version_process.communicate()
		remote_version = remote_version_stdout.decode().replace("HEAD", "").strip()

		# Compare versions
		return current_version != remote_version

	@staticmethod
	def update_framework() -> None:
		command = f"{PIP_EXEC} install --upgrade --force-reinstall git+https://github.com/48302-DiogoJesus/DesktopMacroFramework"
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		print(f"update_framework() => {stdout.decode().strip()}")
		returncode = process.returncode
		if returncode != 0:
			raise RuntimeError(f"Error updating framework. Command returned non-zero exit code {returncode}.")

	@staticmethod
	def update_manager() -> None:
		command = "git pull --ff-only"
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		print(f"update_manager() => {stdout.decode().strip()}")
		returncode = process.returncode
		if returncode != 0:
			raise RuntimeError(f"Error updating manager. Command returned non-zero exit code {returncode}.")
