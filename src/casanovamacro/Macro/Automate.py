import  importlib
import json
from ..Core.API import update_character
from ..Gameplay.Dungeons.DungeonBlueprint import Dungeon
from ..Core.ErrorHandler import *
from ..Gameplay.Template import Activity
from .Action import *

class Automate:
    def login(self):
        
        ErrorHandling.handle_prelogin()
        
        x, y = [round(173 + (333 * config.character.character_index  - (333 / 2))), 560]
        if check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION) is False:
            while True:
                
                if check_image_existance(["dialog/charlock_dialog", (536, 438, 130,54)]):
                    print("Event:Login:Unlocking")
                    click(577, 539, 2)
                    win32api.PostMessage(config.flash_hwnd, win32con.WM_CHAR, ord("0"), 0)
                    sleep(0.1)
                    win32api.PostMessage(config.flash_hwnd, win32con.WM_CHAR, ord("7"), 0)
                    sleep(0.1)
                    win32api.PostMessage(config.flash_hwnd, win32con.WM_CHAR, ord("0"), 0)
                    sleep(0.1)
                    win32api.PostMessage(config.flash_hwnd, win32con.WM_CHAR, ord("2"), 0)
                    sleep(0.1)
                    click(613, 573) #CLICK CONFIRM
                    print("Event:Login:Loading")

                else:
                    click(x , y, 3)
                    sleep(1)

                sleep(1)
            
                if check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION): 
                    sleep(10) #IMPORTANT TO WAIT FLASH WINDOW IDLE
                    # emit("character_online")
                    update_character({
                        "is_online": True,
                        "flash_hwnd" : config.flash_hwnd
                    })
                    
                    print("Event:Login:OK")
                    return  True
        else: 
            print(f"Event:Login:{config.character.nickname} Already Logged In ")
            return True

    def proc(self, previous_class=None):
        previous_class:Activity = None
        undone = []
        module = importlib.import_module("casanovamacro")
        undone = [routine for routine in config.character.routines if routine not in   config.character.done ]
        for routine in undone:
            class_ = getattr(module, routine)
            instance:Activity | Dungeon = class_()
            if previous_class is not None:
                instance.backpack_settling_attempt = previous_class.backpack_settling_attempt
                instance.bag_already_empty_before = previous_class.bag_already_empty_before
                
            if type(instance) is Dungeon:
                
                # instance.done=True
                if previous_class is not None:
                    if type(previous_class) is Dungeon :
                        # DONT RUN DK KEY IF PREVIOUS ROUTINE RUN OUT DK
                        instance.require_dk = not previous_class.is_dk_empty and instance.require_dk
                        instance.is_dk_empty = previous_class.is_dk_empty 
                        instance.dk_attempt_done = previous_class.is_dk_empty # SKIP DK ATTEMPT IF DK IS EMPTY

                        # WILL USE PREVIOUS LOOT CONFIG IF ITS SAME TO SAVE TIME
                        if previous_class.loot_config == instance.loot_focus : instance.is_prepared = True

            instance.init()
            
            if instance.done:
                config.character.done.append(instance.__class__.__name__)
                update_character({"done" : config.character.done})
                # emit("update_done_routine", config.character.done )
            
            previous_class = instance
        # print([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ])
        # print(len([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ]) > 0)
        # print(routine, EXCLUSIVE_ROUTINES)
        # exit(0)
        if len([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ]) > 0 and config.character.faction_shortcut_unlocked: 
            self.cleaning()
       
            # emit("character_stuck_on_activity", config.character.nickname)

    def cleaning(self):
        # EXTRA CLEAN EVERY 7 DAY
        if config.character.focus == "item":
            synthesis_gems(900) # SET 15 MIN SYNTH TIMEUP
        # day = datetime.now().day
        # if config.character.focus == "item" : 
        #     if day % 10 == 0: clean_bag()  #CLEAN ALL JUNK EVERY 10 DAY
            # if day % 3 == 0: repair_equip()   #REPAIR EQUIP EVERY 3 DAY
                
    def init(self):
        try:
            print(f"Event:Automation:Starting")
            if  self.login():
                ErrorHandling.handle_postlogin()
                #HIDE EFFECT AND PLAYER
            
                click(*HIDE_PLAYER_BUTTON_LOCATION)
                sleep(0.5)
                click(*HIDE_EFFECT_BUTTON_LOCATION)
                #STABILIZE HIDE TOP MENU BUTTON
                
                sleep(1)
                close_all_dialog()

                ## WALK AWAY FROM CROWD AND CHANGE TO LINE 2 TO REDUCE LAG
                if is_in_map("starglade") :
                    set_top_menu(False)
                    walk_to_map_coordinate(719,648, acknowledge=True, timeout=20)
                    change_line()

                self.proc()
                print(f"Event:Automation:Done")
        except Exception as ex:
            print(f"Error:Automation:{ex}")
            
        # socket.sio.disconnect()


