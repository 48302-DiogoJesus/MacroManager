# Library Entrypoint / Expose library functionality

## Automation Functionality
from .automation.Windows import windows
from .automation.Keyboard import keyboard, key
from .automation.GUI import gui
from .automation.Files import files

from .automation.Variables import vars
from .automation.Common import wait, end

## Framework Functionality
from .framework.Decorators.MacroDecorator import Macro