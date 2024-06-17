import enum

class MacroStatus(enum.Enum):
    READY = 0
    RUNNING = 1
    PAUSED = 2