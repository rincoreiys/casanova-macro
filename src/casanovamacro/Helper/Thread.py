from threading import Thread
from time import sleep

from .Macro.Base import *
from .Macro.Const import *
from .Socket import emit

def screenshot_thread():
    while True:
        from .Global import config
        # print("config.screenshot_state", config.screenshot_state)
        if config.screenshot_state: 
            # print("SCREENSHOOTI")
            screenshot()
            sleep(0.3)
        else: 
            break
    print("SS THREAD HAS  STOP")

def run_screenshot_thread():
    from .Global import config
    config.screenshot_state = True
    Thread(target=screenshot_thread, daemon=True).start()


def run_online_detector_thread():
    from .Global import config
    config.online_detector_state = True
    Thread(target=online_detector_thread, daemon=True).start()

def online_detector_thread():
    timeout = 120
    while True:
        from .Global import config
        if config.online_detector_state:
            if check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION) == False: 
                timeout -= 1
                if timeout <= 0 : 
                    config.online_detector_state = False
                    break
            else: timeout = 120
            sleep(1)
        else: 
            break
    print("ONLINE DETECTOR THREAD HAS  STOPPED")
    emit("character_disconnected", config.character.__dict__)

def stop_screenshot_thread():
    from .Global import config
    print("stop config.screenshot_state", config.screenshot_state)
    
    config.screenshot_state = False
    print("stop config.screenshot_state", config.screenshot_state)
    
