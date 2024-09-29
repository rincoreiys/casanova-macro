import argparse
from time import sleep
import win32ui
import requests
from .Types import *
import json
from threading import Thread


#SERVER
SERVER_ADDRESS = "http://192.168.1.99:3000"


class Config:
    flash_hwnd:int
    flash:object =  None
    character:Character
    nickname:str
    screenshot_state:bool = False
    #PROGRAM SETTING
    only_screenshot:bool = False
    #WEEKLY EVENTS
    torch_event:bool = False

    def __init__(self):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument("-fhwnd", "--flash_hwnd", help="Flash HWND")
            parser.add_argument("-nickname", "--nickname", help="Character Name")
            parser.add_argument("-screenshot", action="store_true")
            
            args = parser.parse_args()
            print("Event:Init:", args)
            
            try:
                if args.screenshot == True: 
                    self.only_screenshot = True
                    self.character = Character()

            except Exception: pass

            self.nickname = args.nickname
            self.flash_hwnd = int(args.flash_hwnd)
            response_attr = ",".join(Character.__annotations__.keys())

            for x in range(2): #MAKE SURE FLASH HANDLE ATTACHED
                try:
                    self.flash = win32ui.CreateWindowFromHandle(self.flash_hwnd)
                    break
                except Exception as flash_window_ex:
                    print("Error:Window:", flash_window_ex)


            if self.only_screenshot == False : 
                response = requests.get(f"{SERVER_ADDRESS}/character/{self.nickname}?only={response_attr}")
              
                if response.status_code == 200: 
                    json_data = response.json()["data"]
                    print("Event:Character Info:",json_data)
                    self.character = Character(**json_data)
                else:
                    print(f"Error:Character Info:Failed to get account {response}")
                    exit(3)
            
        except Exception as args_ex:
            print(f"Error:Init:Arg error: check again argument you passed in {args_ex.__str__}")
            exit(1)
        
#STARTUP
config = Config()








