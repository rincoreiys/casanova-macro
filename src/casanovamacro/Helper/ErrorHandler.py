
import ctypes
from threading import Thread
# from Helper.Types import InteruptableThread as IT
from ..Helper.Macro import *
from time import sleep
from dataclasses import dataclass


class InteruptableThread():
    def raise_exception(self, e = Exception):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident,  ctypes.py_object(e))

class CharacterDieException(Exception): pass
class CharacterLoginStuckException(Exception): pass
class CharacterConflictException(Exception): pass
class CharacterDisconnectedException(Exception): pass
class CharacterLoginFailedException(Exception): pass
class ActivityTimeoutException(Exception):pass

LOGIN_EXCEPTIONS = [
    {
        "type" : CharacterLoginStuckException,
        "recognition" : "character_login_stuck",
    },
    {
        "type" : CharacterConflictException,
        "recognition" : "character_conflict",
    }
]
         
def run_thread(target):
    t = Thread(target=target, daemon=True)
    t.start()
    #print(t)
    return t

# @dataclass
# class ErrorHandler:
#     prelogin_listener:bool = True
#     postlogin_listener:bool = False
#     def __post_init__(self):
#         run_thread(self.chrome_dialog_closer)
#         run_thread(self.interupt_listener)

#     def ping_status(self):
#         status = subprocess.getstatusoutput("ping -n 1 " + "r2cdn-encs.r2games.com")
#         return True if status[0] == 0 else False

#     #PRELOGIN
#     def handle_prelogin(self):
#         self.prelogin_listener = True
#         run_thread(self.maintenance_detector)
#         sleep(25) #GIVE BROWSER SOMETIME TO LOAD WEB BEFORE RUN ANOTHER DETECTOR
#         run_thread(self.detect_login_error)

#     def maintenance_detector(self):
#         while self.prelogin_listener:
#             if "?ac=toGame"  in _.driver.current_url:
#                 # time.sleep(15)
#                 _.macro_thread.raise_exception(GameMaintenanceException)
#                 break
#             time.sleep(0.5)
        

#     def detect_login_error(self): 
#         while self.prelogin_listener:
#             for ex in LOGIN_EXCEPTIONS:
#                 res = check_image_existance(asset_path(f"Exception/{ex['recognition']}"))
                
#                 if res: 
#                     print(ex, res)
#                     return _.macro_thread.raise_exception(ex["type"])
#             time.sleep(1)
#         #print("ERROR LOGIN DETECTOR CLOSED")
            
#     #POST LOGIN 
#     def handle_postlogin(self):
#         self.postlogin_listener = True
#         self.prelogin_listener = False #TURN OFF PRELOGIN LISTENER
        
#         run_thread(self.online_checker)
#         sleep(10) #GIVE BROWSER SOMETIME TO LOAD WEB BEFORE RUN ANOTHER DETECTOR
#         run_thread(self.handle_in_game_annoying_dialog)
        
#     def online_checker(self):
#         rto_count = 0
#         while self.postlogin_listener:
#             ps = self.ping_status()
#             ind =  wait_for_image(imagePath=asset_path(f"State/online_indicator"), region=(160,80 ,40,40), timeout=40)
#             # #print("ps", ps, "ind", ind)
#             if not ind or  rto_count >= 60:
#                 _.macro_thread.raise_exception(CharacterDisconnectedException)
#                 break
#             if not ps: rto_count += 0.5
#             else: rto_count = 0
#             sleep(0.5)
       
        
#         print("ONLINE CHECKER CLOSED")            
    
#     def handle_in_game_annoying_dialog(self):
#         die_emit_delay = 0
#         while self.postlogin_listener:
#             if check_image_existance(imagePath=asset_path("Exception/require_party"), region=(611, 347, 145, 42)):
#                 #CONFIRM
#                 click(682,411)
                
#             if check_image_existance(imagePath=asset_path("Exception/die")): 
#                 if _.macro_thread is not None and die_emit_delay <= 0 : 
#                     _.macro_thread.raise_exception(CharacterDieException)
#                     die_emit_delay = 10
                
#             if check_image_existance(imagePath=asset_path("Exception/require_kill_all"), region=(583, 318, 199, 131)):
#                 click(682,411)

#             if check_image_existance(imagePath=asset_path("Exception/cant_teleport"), region=(583, 318, 199, 131)):
#                 click(682,411)
                
#             if check_image_existance(imagePath=asset_path("Exception/require_unmounted"), region=(615, 328, 138, 115)):
#                 click(682,411)
#                 set_mounting(False)

#             time.sleep(1)
#             die_emit_delay -= 1
            
#         #print("IN-GAME POP UP CLOSED CLOSED")

#     def interupt_listener(self):
#         while True:
#             if ((keyboard.is_pressed("alt") and keyboard.is_pressed("ctrl")) or (keyboard.is_pressed("c") and keyboard.is_pressed("ctrl"))):
#                 print("c.trl + alt pressed")
#                 # self.close()
#                 if  _.macro_thread is  not None :
#                     _.macro_thread.raise_exception(NodeTerminatedException)
#                 if _.log_mode : 
#                     for thread in threading.enumerate(): print(thread, thread.is_alive())
#                 break
#             sleep(0.5)

#         # time.sleep(5)
       
#         logger("INTERUPT LISTENER CLOSED")
        
#     def close(self):
#         self.postlogin_listener = False
#         self.prelogin_listener = False
        
