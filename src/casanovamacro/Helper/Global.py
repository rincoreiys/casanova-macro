import argparse
from time import sleep
import win32ui
import requests
from casanovamacro.Helper.Macro.Const import SERVER_ADDRESS
from .Types import *

class Config:
    flash_hwnd:int
    flash_wrapper_hwnd:int
    flash:object =  None
    character:Character
    nickname:str
    active_routine:str
    screenshot_state:bool = False
    workspace_mode:str = ""
    online_detector_state:bool = False

    # IF A FLOOR or A DG INSTANCE OCUR UNHANDLED ERROR FOR LONG TIME 
    # TURN OFF THE CHARACTER AND RESTART THE PROCESS FROM START
    

    #WEEKLY EVENTS
    torch_event:bool = False

    def __init__(self):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("-whwnd", "--workspace_hwnd", help="Workspace HWND")
            parser.add_argument("-wmode", "--workspace_mode", help="Workspace Mode")
            parser.add_argument("-fhwnd", "--flash_hwnd", help="Flash HWND")
            parser.add_argument("-fwhwnd", "--flash_wrapper_hwnd", help="Flash Wrapper HWND")
            parser.add_argument("-nickname", "--nickname", help="Character Name")
            
            args = parser.parse_args()
            print(args)
            self.nickname = args.nickname
            self.flash_hwnd = int(args.flash_hwnd)
            self.flash_wrapper_hwnd = int(args.flash_wrapper_hwnd)
            self.workspace_hwnd = int(args.workspace_hwnd)
            self.workspace_mode = args.workspace_mode
            response_attr = ",".join(Character.__annotations__.keys())

            
            response = requests.get(f"{SERVER_ADDRESS}/character/{self.nickname}?only={response_attr}")
            print(response.json())
            if response.status_code == 200: 
                json_data = response.json()["data"]
                print("jdd", json_data)
                # self.character = Character
                self.character = Character(**json_data)
                
                #OVERWRITE OLD ONLINE DESCRIPTION
                self.character.workspace_mode = self.workspace_mode
                self.character.flash_hwnd = self.flash_hwnd
                print("cdfsd",  self.character)
                print("flash", self.flash)
                while self.flash is None and self.flash_hwnd != 0:
                    try:
                        self.flash = win32ui.CreateWindowFromHandle(self.flash_hwnd)
                    except Exception as flash_window_ex:
                        print("Arg error:", flash_window_ex)
            else:
                print("Failed to get account info")
                exit(3)
            
        except Exception as args_ex:
            print("Arg error: check again argument you passed in",args_ex)
            exit(1)
        
#STARTUP
config = Config()








