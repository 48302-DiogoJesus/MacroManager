import datetime
import time

from ..utils import get_source_around_line, handleMasterEventsWhileRunning
from ..Variables import RWVariables, RVariables

# Put on Automation functions
def AutomationDecorator(func):
    def wrapper(*args, **kwargs):
        handleMasterEventsWhileRunning(func, args)

        # TODO: Communicate w/ MacroMonitor
        instructions, instruction_idx = get_source_around_line()
        if RWVariables.macroMonitorShared is None: raise Exception("Macro Monitor variable was not initialized (= None)")
        RWVariables.macroMonitorShared.updateInstructionsWindow(instruction_idx, instructions)

        # Execute operation
        try:
            RVariables.logger.write(f"[CALL] {str(func.__module__).replace('DesktopAutomationFramework.', '')}.{func.__name__} {args}")
            result = func(*args, **kwargs)
            # On success
            if result is not None:
                RVariables.logger.write(f"[RESULT] {result}")
        except Exception as e:
            # Logger (log event on error)
            RVariables.logger.error(f"{str(func.__module__).replace('DesktopAutomationFramework.', '')}.{func.__name__} {args} => Threw Exception")
            # Re-raise error
            raise e
        
        handleMasterEventsWhileRunning(func, args)

        # Time Between Actions (with a stop/pause check every 50 ms to improve responsiveness)
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).total_seconds() < RWVariables.time_between_actions_s:
            time.sleep(0.05) # 50 ms
            handleMasterEventsWhileRunning(func, args)
        
        handleMasterEventsWhileRunning(func, args)
        return result
    return wrapper