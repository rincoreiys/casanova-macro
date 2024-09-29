from threading import Thread
from time import sleep

from ..Macro.Base import *
from ..Macro.Const import *

def screenshot_thread():
    print("Event:Screenshot:Thread is Running")
    while True:
        from .Global import config
        if config.screenshot_state: 
            screenshot()
            sleep(0.3)
            if config.only_screenshot: 
                break
        else: 
            break
    print("Event:Screenshot:Thread Stopped")
    sleep(3)
    os._exit(0)

def run_screenshot_thread():
    from .Global import config
    if config.screenshot_state is not True:
        config.screenshot_state = True
        run_thread(screenshot_thread)
   
    
def stop_screenshot_thread():
    from .Global import config
    config.screenshot_state = False
    
def run_thread(target):
    t = Thread(target=target, daemon=True)
    t.start()
    return t