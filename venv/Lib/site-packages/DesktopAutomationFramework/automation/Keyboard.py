import time
from pynput.keyboard import Key as _k, Controller as _c

from .Keys import convert_to_original_key, MyKey as _mk

from ..framework.Decorators.AutomationDecorator import AutomationDecorator

kboard = _c()
key = _mk

class keyboard:

    @AutomationDecorator
    @staticmethod
    def write(text: str):
        kboard.type(text)

    @AutomationDecorator
    @staticmethod
    def keys(*args: _mk | str, repeat_times: int = 1, repeat_interval_s: float = 0.3):
        keys = [item.lower() if isinstance(item, str) else item for item in args]
        keys = [convert_to_original_key(item) if not isinstance(item, str) else item for item in keys]

        for _ in range(repeat_times):
            # Press all keys
            for key in keys:
                kboard.press(key)

            # Release all keys
            for key in keys:
                try:
                    if kboard.pressed(key): kboard.release(key)
                except: pass

            # Only wait if there will be a second iteration
            if repeat_times > 1:
                time.sleep(repeat_interval_s)
