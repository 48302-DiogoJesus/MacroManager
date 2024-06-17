import os
import sys
import threading

from ..framework.MacroMonitorGUI import MacroMonitorGUI
from ..framework.Logger import Logger
from ..framework.types.MacroStatus import MacroStatus

# READ-ONLY
class RVariables:
    macro_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    macro_name = os.path.basename(macro_path)
    logger = Logger(macro_path)
    
    # Control macro pausing (default: not set)
    resumeMacroFlag = threading.Event()

# READ-WRITE
class RWVariables:
    time_between_actions_s: float = 0
    macroMonitorShared: None | MacroMonitorGUI = None
    
    stopMacro: bool = False
    macroStatus: MacroStatus = MacroStatus.READY
    expectedWindowTitle: None | str = None