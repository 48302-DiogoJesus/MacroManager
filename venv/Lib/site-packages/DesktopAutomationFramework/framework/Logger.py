import os
import datetime
import pytz

LOGS_FOLDER_NAME = "logs"

class Logger:
    log_file_name = ""
    logs_path = ""
    local_timezone = pytz.timezone("Europe/London")

    def __init__(self, macro_path: str):
        self.macro_path = macro_path
        self.new_file()

    def new_file(self):
        now = datetime.datetime.now(self.local_timezone)  # Get current datetime in local timezone
        self.log_file_name = now.strftime("%Y-%m-%d %H.%M.%S") + ".txt"

        self.logs_path = os.path.join(self.macro_path, LOGS_FOLDER_NAME)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)

    def write(self, log_content: str):
        now = datetime.datetime.now(self.local_timezone)  # Get current datetime in local timezone
        log_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        file_path = os.path.join(self.logs_path, self.log_file_name)

        with open(file_path, 'a') as file:
            file.write(f"[{log_time}] {log_content}\n")

    def error(self, error_msg: str):
        now = datetime.datetime.now(self.local_timezone)  # Get current datetime in local timezone
        log_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        file_path = os.path.join(self.logs_path, self.log_file_name)

        with open(file_path, 'a') as file:
            file.write(f"[{log_time}] [ERROR] {error_msg}\n")
