from dataclasses import dataclass
from threading import Thread
from time import sleep

from ..Macro.Const import *
from ..Macro.Base import *

from ..Core.Thread import run_thread
EXCEPTION_REGION = (332,282,681,432)
#ERROR

@dataclass
class ErrorHandler:
    prelogin_listener:bool = True
    postlogin_listener:bool = False
    #PRELOGIN
    def handle_prelogin(self):
        self.prelogin_listener = True
        run_thread(self.detect_login_error)

    def handle_postlogin(self):
        from .Global import config
        self.postlogin_listener = True
        sleep(1)
        self.prelogin_listener = False #TURN OFF PRELOGIN LISTENER
        
        run_thread(self.online_detector)
        sleep(5) #GIVE BROWSER SOMETIME TO LOAD WEB BEFORE RUN ANOTHER DETECTOR
        run_thread(self.handle_in_game_annoying_dialog)


    def detect_login_error(self): 
        print("Event:Login:Login Detector Running")
        login_timout = 90
        err = None
        while self.prelogin_listener:
            if check_image_existance(  ["exception/character_conflict", EXCEPTION_REGION ] ) or check_image_existance(["exception/related_character_online",EXCEPTION_REGION ]): 
                err = "Conflict"
            elif check_image_existance( ["exception/login_failed", EXCEPTION_REGION ]): 
                err ="Failed"
            
            if err: 
                print(f"Event:Login:{err}")
                os._exit(0)
                break

            sleep(1)
            login_timout -= 1
            if login_timout <= 0:
                print("Event:Login:Timeout")
                os._exit(0)
                break

        print("Event:Login:Login Detector Closed")
        
    def online_detector(self):
        print("Event:Online Detector:Running")
        allowed_idle_timeout = 60
        while True:
            sleep(1)
            if check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION) == False: 
                allowed_idle_timeout -= 1
                if allowed_idle_timeout <= 0 : break
            else: allowed_idle_timeout = 60

        print("Event:Online Detector:Closed")
        print("Error:Disconnected") 
        os._exit(0)
    
    def handle_in_game_annoying_dialog(self):
        while True:
            if check_image_existance(["exception/require_party", BLOCKING_NOTIFICATION_REGION], grayscale=True) : click(675,513)
            if check_image_existance(["exception/require_exit_party", BLOCKING_NOTIFICATION_REGION] , grayscale=True) : click(652,576)
            if check_image_existance(["exception/require_unmount", BLOCKING_NOTIFICATION_REGION] , grayscale=True) : click(674,514)
            sleep(5)
        # while self.postlogin_listener:
        #     if check_image_existance(imagePath=asset_path("Exception/require_party"), region=(611, 347, 145, 42)):
        #         #CONFIRM
        #         click(682,411)
                
        #     if check_image_existance(imagePath=asset_path("Exception/die")): 
        #         if _.macro_thread is not None and die_emit_delay <= 0 : 
        #             _.macro_thread.raise_exception(CharacterDieException)
        #             die_emit_delay = 10
                
        #     if check_image_existance(imagePath=asset_path("Exception/require_kill_all"), region=(583, 318, 199, 131)):
        #         click(682,411)

        #     if check_image_existance(imagePath=asset_path("Exception/cant_teleport"), region=(583, 318, 199, 131)):
        #         click(682,411)
                
        #     if check_image_existance(imagePath=asset_path("Exception/require_unmounted"), region=(615, 328, 138, 115)):
        #         click(682,411)
        #         set_mounting(False)

        #     time.sleep(1)
        #     die_emit_delay -= 1
            
        # #print("IN-GAME POP UP CLOSED CLOSED")

    def close(self):
        self.postlogin_listener = False
        self.prelogin_listener = False
        
ErrorHandling = ErrorHandler()