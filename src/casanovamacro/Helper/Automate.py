import datetime, importlib

from casanovamacro.Gameplay.Dungeons.DungeonBlueprint import Dungeon
from casanovamacro.Helper.ErrorHandler import ActivityTimeoutException
from ..Gameplay.Template import Activity
from .Macro import *
from .Global import config
from .Thread import *
from .Socket import emit, socket
# run_screenshot_thread()

class Automate:
   
    def login(self):
        print("loging in")
        timeout = 120
        def handle_charlock_box():
            try:
                if check_image_existance(["dialog/charlock_dialog", (536, 438, 130,54)]):
                        # If the window is minimized, restore it
                    win32gui.SetForegroundWindow(config.flash_hwnd)
                    # if win32gui.IsIconic(config.flash_hwnd):
                    #     win32gui.ShowWindow(config.flash_hwnd, win32con.SW_RESTORE)
                    # Bring the window to the foregrounds
                    sleep(0.05)
                    click(577, 539, 2)
                    pyautogui.press("backspace")
                    sleep(0.2)
                    pyautogui.write("0702")
                    sleep(1)
                    # win32gui.SetWindowPos(config.workspace_hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                    click(613, 573) #CLICK CONFIRM
            except:
                handle_charlock_box()
        x, y = [round(173 + (333 * config.character.character_index  - (333 / 2))), 560]
       
        step = 2
        if check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION) is False:
            while True:
                timeout -= step
                click(x , y, 3)
                print("x, y", x ,y)
                sleep(1)

                handle_charlock_box()

                if timeout <= 0: 
                    print(f"LOGIN FAILED")
                    emit("character_login_timeout", config.character.name )
                    return False
                sleep(step)
                emit("character_loading", config.character.name )
                if check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION): break
                if check_image_existance(CHARACTER_CONFLICT_RECOGNITION):
                    print("Character Conflict")
                    emit("character_conflict", config.character.name)
                    return False
            
            sleep(10) #IMPORTANT TO WAIT FLASH WINDOW IDLE
            emit("character_online", config.character.name)
            return  True
        else: 
            print(f"{config.character.name} ALREADY LOGGED IN ")
            return True

    def proc(self, previous_class=None):
        previous_class:Activity = None
        undone = []
        module = importlib.import_module("casanovamacro")
        undone = [routine for routine in config.character.routines if routine not in   config.character.done ]
        try:
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

                print("init", instance)
                instance.init()
                
                if instance.done:
                    print(type(routine).__name__, "done")
                    config.character.done.append(instance.__class__.__name__)
                    emit("update_done_routine", config.character.done )
                
                previous_class = instance
            
            # print([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ])
            # print(len([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ]) > 0)
            # print(routine, EXCLUSIVE_ROUTINES)
            # exit(0)
            if len([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ]) > 0 and config.character.faction_shortcut_unlocked: 
                self.cleaning()
            emit("character_done")
            sleep(3) #IMPORTANT TO WAIT TILL ALL SOCKET EVENT EMITTED
        except ActivityTimeoutException:
            emit("character_stuck_on_activity", config.character.name)

    def cleaning(self):
        # EXTRA CLEAN EVERY 7 DAY
        if config.character.focus == "item":
            synthesis_gems()
        # day = datetime.now().day
        # if config.character.focus == "item" : 
        #     if day % 10 == 0: clean_bag()  #CLEAN ALL JUNK EVERY 10 DAY
            # if day % 3 == 0: repair_equip()   #REPAIR EQUIP EVERY 3 DAY
                
    def init(self):
        print("PASSED")
    
        
        if  self.login():
            run_online_detector_thread()
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

            print(f"{config.character.name} HAS LOGGED IN ")
            print("Character Routines: ", config.character.routines)
            self.proc()
            
            print(f"AUTOMATION DONE")
        socket.sio.disconnect()


