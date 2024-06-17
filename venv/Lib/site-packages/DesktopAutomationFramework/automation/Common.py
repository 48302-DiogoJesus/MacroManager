import time

from ..framework.Decorators.AutomationDecorator import AutomationDecorator

@AutomationDecorator
def wait(seconds: int):
    time.sleep(seconds)

@AutomationDecorator
def end():
    exit()
