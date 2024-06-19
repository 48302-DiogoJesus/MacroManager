import datetime
import os
import subprocess
import sys
import threading

from DesktopAutomationFramework.framework.types.CustomErrors import MacroStoppedError

from ..MacroMonitorGUI import MacroMonitorGUI
from ..types.MacroStatus import MacroStatus
from ..utils import get_full_source_code, showMacroErrorGUI, tryUpdateMacroStatusGUI, updatePlayButtonsConfigs
from ..Variables import RVariables, RWVariables
from ..SelfUpdate import SelfUpdate
from ...automation.Variables import vars

# Put on macro function
def Macro(*, interval_s: float):
    interval_s_cmd: float | None = None
    
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--interval_s='):
            interval_s_cmd = float(arg.replace('--interval_s=', ''))
            del sys.argv[i]
            break
        
    if interval_s_cmd is not None and interval_s_cmd >= 0:
        RWVariables.time_between_actions_s = interval_s_cmd
    else:
        RWVariables.time_between_actions_s = interval_s
    
    source_code = get_full_source_code()
    
    # Start/Resume
    def onMacroStartResume():
        if RWVariables.macroStatus is MacroStatus.PAUSED or RWVariables.macroStatus is MacroStatus.READY:
            RVariables.resumeMacroFlag.set()
            updatePlayButtonsConfigs()
    def onMacroPause():
        if RWVariables.macroStatus is MacroStatus.RUNNING:
            RVariables.resumeMacroFlag.clear()
            updatePlayButtonsConfigs()
    def onMacroStop(manual_stop: bool):
        if RWVariables.macroStatus is MacroStatus.RUNNING or RWVariables.macroStatus is MacroStatus.PAUSED:
            RWVariables.stopMacro = True
            updatePlayButtonsConfigs()
            if RWVariables.macroStatus is MacroStatus.PAUSED:
                # Make thread resume in order to realize it should stop
                RVariables.resumeMacroFlag.set()
        
        if manual_stop: 
            RWVariables.macroStartLineNumber = None
            if RWVariables.macroMonitorShared is not None:
                RWVariables.macroMonitorShared.updateInstruction(source_code[0][0])
    
    def onMacroSchedule(macroMonitor: MacroMonitorGUI, time: str):
        start_time = datetime.datetime.now() + datetime.timedelta(minutes=float(time))
        start_time_str = start_time.strftime("%H:%M:%S")
        start_time_str_name = start_time.strftime("%H-%M-%S")
        
        abs_script_location = os.path.abspath(sys.argv[0])
        args = ' '.join(sys.argv[1:])
        
        command = f"pythonw \"{abs_script_location}\" {args}"

        schtasks_command = f"schtasks /create /sc once /tn DesktopAutomation_{RVariables.macro_name}_{start_time_str_name} /tr \"{command}\" /st {start_time_str} /F"

        print("Scheduling task:", schtasks_command)

        try:
            result = subprocess.run(schtasks_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Task scheduled successfully.")
            print("Command output:", result.stdout.decode())
            exit()
        except subprocess.CalledProcessError as e:
            print("Error scheduling task:", e.stderr.decode())
            macroMonitor.showPopup(f"Error scheduling task: {e.stderr.decode()}")
    
    def decorator(func):
        def wrapper():
            # Runs once: when macro() is called
            if not os.path.exists(vars.output_folder):
                os.makedirs(vars.output_folder)
                print("Created output folder")
            else:
                print("Output folder already exists")

            def recursive_macro_runner(errored_on_previous_run: bool = False):
                try:
                    updatePlayButtonsConfigs()
                    RWVariables.expectedWindowTitle = None
                    RVariables.logger.new_file()
                    RWVariables.macroStatus = MacroStatus.READY
                    if not errored_on_previous_run:
                        tryUpdateMacroStatusGUI()
                    else:
                        # Reset Error
                        errored_on_previous_run = False
                        # Leave the error message there
                        pass

                    print("[READY]")
                    
                    # Pause and wait until started
                    RVariables.resumeMacroFlag.clear()
                    RVariables.resumeMacroFlag.wait()
                    RWVariables.macroStatus = MacroStatus.RUNNING
                    print("[RUNNING]")
                    tryUpdateMacroStatusGUI()
                    # Call macro() function
                    func()
                    RWVariables.macroStartLineNumber = None           
                except Exception as e:
                    errored_on_previous_run = True
                    error_message = str(e)
                    
                    showMacroErrorGUI(error_message)
                    RVariables.logger.error(error_message)
                    
                    # if RWVariables.macroMonitorShared is not None:
                    #     RWVariables.macroMonitorShared.showPopup(error_message)
                finally:
                    print("[FINISHED]")
                    # Call itself again
                    recursive_macro_runner(errored_on_previous_run)
            
            # Start Macro Runner Thread
            thread = threading.Thread(target=recursive_macro_runner)
            thread.daemon = True # If main thread dies it dies too
            thread.start()
                        
            # ! Blocks the main thread on tkinter GUI
            RWVariables.macroMonitorShared = MacroMonitorGUI(
                RVariables.macro_name,
                source_code,
                onMacroStartResume,
                onMacroPause,
                onMacroStop,
                onMacroSchedule,
                onUpdate=SelfUpdate
            )
            
            updatePlayButtonsConfigs()
            
            RWVariables.macroMonitorShared.launchGUI()
        return wrapper
    
    return decorator
