from datetime import datetime as _td
import os
import sys

from DesktopAutomationFramework.framework.Variables import RVariables

from ..framework.Decorators.AutomationDecorator import AutomationDecorator

class _t:
    @AutomationDecorator
    @property
    def year(self):
        return _td.now().year

    @AutomationDecorator
    @property
    def month(self):
        return _td.now().month

    @AutomationDecorator
    @property
    def day(self):
        return _td.now().day

    @AutomationDecorator
    @property
    def hour(self):
        return _td.now().hour

    @AutomationDecorator
    @property
    def minute(self):
        return _td.now().minute

    @AutomationDecorator
    @property
    def second(self):
        return _td.now().second

    @AutomationDecorator
    def strftime(self, format_str):
        """ 
        %d day    (ex: 02)
        %m month  (ex: 04)
        %Y year   (ex: 2023)
        %y year   (ex: 23)
        %H hour   (ex: 12)
        %M minute (ex: 60)
        %S second (ex: 45)
        """
        return _td.now().strftime(format_str)
    

class vars:
    # Fixed Variables
    time = _t()
    output_folder = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "output")
    user_dir = "%userprofile%"

    # Variables from invocation. Ex: pythonw macro.py reports_number=10 variant=FA
    @staticmethod
    def getString(variable_name: str, accepted_values: list[str] | None = None) -> str:
        """
        Get the variable {variable_name} of type STRING from macro invocation
        raises Error if a value was not found for the variable
        """
        value = getattr(vars, variable_name, None)
        if value is None:
            raise Exception(f"'{variable_name}' is missing. Correct Example: pythonw {sys.argv[0]} {variable_name}=your_value")
        
        if accepted_values is not None and value not in accepted_values:
            raise Exception(f"{variable_name}={value}. '{value}' is not valid. Valid options: {accepted_values}")

        return str(value)

    @staticmethod
    def getNumber(variable_name: str, accepted_values: list[float | int] | None = None) -> float | int:
        """
        Get the variable {variable_name} of type NUMBER from macro invocation
        raises Error if a value was not found for the variable
        """
        value = getattr(vars, variable_name, None)
        if value is None:
            raise Exception(f"'{variable_name}' is missing. Correct Example: pythonw {sys.argv[0]} {variable_name}=your_value")
        try:
            value = float(value)
            if value.is_integer(): value = int(value)
        except Exception as e:
            raise Exception(f"{variable_name} = {value}. The value is not a number")
        
        if accepted_values is not None and value not in accepted_values:
            raise Exception(f"{variable_name}={value}. '{value}' is not valid. Valid options: {accepted_values}")
        return value


def _populate_properties_from_command_line():
    for arg in sys.argv[1:]:
        key, value = arg.split('=')
        setattr(vars, key, value)

_populate_properties_from_command_line()
