import time
import pygetwindow as gw

from ..framework.Variables import RWVariables
from ..framework.Decorators.AutomationDecorator import AutomationDecorator

class windows:
    @AutomationDecorator
    @staticmethod
    def wait(partial_title: str, timeout_s: int = 2):
        time_passed_s = 0

        partial_title = partial_title.lower()

        actual_window_title = ""
        while True:
            try:
                actual_window_title = str(gw.getActiveWindowTitle()).lower()
            except: 
                pass

            is_in_expected_window = actual_window_title.find(partial_title) != -1
            if is_in_expected_window:
                RWVariables.expectedWindowTitle = partial_title
                return

            # Not in expected window. Try selecting it
            windows = gw.getWindowsWithTitle(partial_title)

            if windows:
                # Select window
                window = windows[0]
                window.activate()
                window.show()

                # Check if successful
                try:
                    actual_window_title = str(gw.getActiveWindowTitle()).lower()
                except: 
                    pass

                is_in_expected_window = actual_window_title.find(partial_title) != -1
                if is_in_expected_window:
                    # Could go to it
                    RWVariables.expectedWindowTitle = partial_title
                    return
                
            time.sleep(0.1) # 100 ms
            time_passed_s += 0.1

            if time_passed_s > timeout_s:
                raise Exception(f"Window containing '{actual_window_title}' not found")
            else:
                continue

    @AutomationDecorator
    @staticmethod
    def select(partial_title: str):
        partial_title = partial_title.lower()
        windows = gw.getWindowsWithTitle(partial_title)

        if windows:
            window = windows[0]
            window.activate()
            window.show()
            RWVariables.expectedWindowTitle = partial_title
        else:
            raise Exception(f"Window containing '{partial_title}' not found")