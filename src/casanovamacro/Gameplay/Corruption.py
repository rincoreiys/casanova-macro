from .Template import *
from ..Core.ErrorHandler import  run_thread
import random
def fight_boss(): return check_image_existance(["dungeon/corruption/boss", (604, 0, 61, 50 )], grayscale=False)
def fight_mob(): return check_image_existance(["dungeon/corruption/mob", (604, 0, 61, 50 )], confidence=.95)
def is_in_middle(): return  check_image_existance(["Common/character_on_minimap",(1272, 124, 40, 25)])
def is_in_end(): return check_image_existance(["Common/character_on_minimap", (1223, 33, 75, 92)], grayscale=False)
def is_in_start(): return not is_in_middle() and  not is_in_end()
CLAIMED_STATE = ["dungeon/corruption/claimed" , NOTIFICATION_CENTER_SCREEN_DIALOG_REGION]
@dataclass
class Corruption(Activity):
    floor_limit:int = config.character.corruption_limit
    max_floor:int = 25
    current_floor:int = 0
    first_time_claim:bool = True
    claimed:bool = False
    category:str = "Dungeon" #IMPORTANT
    activity_asset_directory:str = "Corruption"
    # need_uncover_attempt = 50
    need_corruption_loot:bool = config.character.need_corruption_loot
    required_space: int = floor_limit + (5 if need_corruption_loot else 0) + 1 #1 FOR BREATHING SPACE ON BAGPACK
    die_tolerance:int = 5
    first_time_read_map:bool = True
    
    position:str = ""
    backtick_state:bool = False
    floor_timeout:int = 300 # 500 SECOND AROUND 5 MIN

    def die_detector(self):      
        print("Macro:Corruption:Die Detector Started")
        while not self.done and self.running:
            if self.is_inside:
                if check_image_existance(["exception/die", (503,377, 341, 237)]):
                    self.in_error_calibration = True
                    self.is_inside = False
                    click(673, 597)
                    wait_map_load()
                    sleep(2)
                    self.is_inside = False  
                    #CLEAR LOCK TARGET (BOSS OR MOB)
                    press(win32con.VK_ESCAPE, mode="unicode") 
                    press(win32con.VK_ESCAPE, mode="unicode") 
                    self.in_error_calibration = False
            sleep(2)
        print("Macro:Corruption:Die Detector Closed")

    def floor_timeout_detector(self):
        while not self.done  and self.running:
            persist_floor = self.current_floor
            counter = 0
            while self.current_floor == persist_floor and self.running and self.is_inside:
                if counter >= self.floor_timeout:
                    self.in_error_calibration = True
                    self.first_time_claim = True
                    self.claimed = False
                    if is_in_middle(): afk_if_mob_exist()
                    self.in_error_calibration = False
                    counter = 0

                sleep(1)
                counter += 1
            sleep(2)

    def read_pointer(self):
        while not self.done and self.running:
            while not self.is_inside  and self.running: sleep(1) #WILL OPERATE IF INSIDE CORRUPTION
            if self.current_floor > 0:
                if is_in_end():   
                    self.position = "end"
                    print("Macro:Corruption:Pointer at end")
                elif is_in_middle():   
                    self.position = "middle"
                    print("Macro:Corruption:Pointer at middle")

                elif not check_map_blank() :  
                    self.position = "start"
                    print("Macro:Corruption:Pointer as start")

                if is_in_end() and  fight_mob() : 
                    press(win32con.VK_ESCAPE, mode="unicode")
                     # ` BACKTICK CODE DOING IT TO GET RID POINTER GLITCH BETWEEN START AND MIDLE ALSO SPAM TO KEEP CHARACTER ATTACK MOB OR BOSS
                elif self.backtick_state:
                    press(192, mode="unicode") 
                    press("1") #PREVENT INVISIBLE GHOST --> RUNNING DIRECTLY TO CLAIM NPC
            else:
                self.position = ""
            sleep(1)
        
    def read_floor(self):
        while not self.done  and self.running:

            if is_in_map("starglade") or is_in_map(self.image_path("hall")) : 
                self.current_floor = 0  
            elif check_map_blank(): 
                wait_map_load()
                sleep(0.5)
            else:
                param =  self.current_floor if self.current_floor >  0 else  1
                for i in range(param, self.max_floor+1, 1):
                    res = is_in_map(self.image_path(f"floors/{i}"))        
                    if res:
                        print(f"Macro:Corruption: Detect floor {i} is {res}, expect to be {self.current_floor}")
                        self.current_floor = i
                        break
                    
                    print(f"Macro:Corruption: Floor progress is { self.current_floor} of {self.max_floor} ")
                    sleep(0.1)
           
            self.is_inside = self.current_floor > 0
            self.first_time_read_map = False
            sleep(4)

    def kill_mob(self):
        if wait_for_condition(fight_mob, timeout=3):
            while fight_mob() and self.position == "middle" and self.running: sleep(1)
        if wait_for_condition(fight_boss, timeout=3):
            while fight_boss()  and self.running: sleep(1)

    def kill_boss(self):
        self.backtick_state = True
        if wait_for_condition(fight_boss, timeout=2):
            while fight_boss()  and self.running: sleep(1)
            # wait_for_condition(fight_boss())
        #self.boss_killed = True
            
    def detect_location(self):
        if self.in_error_calibration: 
            sleep(5)
            return

        if not self.is_inside: 
            if is_in_map("starglade"):    
                self.first_time_claim = True
                self.talk_to_sg_battlemaster()
            elif is_in_map(self.image_path("hall")):   
                self.talk_to_corruption_npc()

        elif self.is_inside: 
            
            print(f"Macro:Corruption:Character is inside of instance")
            if self.position == "middle":   
                self.backtick_state = True
                self.kill_mob() 
            elif self.position == "end":
                # self.need_uncover_attempt -= 1
                # self.kill_boss()
                if not self.claimed : self.claim()
                else: self.upstair()

                # if self.need_uncover_attempt == 0: self.need_uncover_attempt = 50
               
            elif self.position == "start": 
                self.claimed = False #SOLVE BREAKTHOURH WALL ANOMALLY
                self.enter_gate()
        sleep(0.5) #IMPORTANT FOR CPU SAVING
        
    def talk_to_sg_battlemaster(self):
        set_party(False)
        if check_image_existance(MOB_STATE_RECOGNITION_LOCATION, confidence=.95): press(win32con.VK_ESCAPE, mode="unicode") # 
        SG_BATTLEMASTER_DIALOG = ["dialog/battlemaster", NPC_DIALOG_REGION]
        if check_image_existance(SG_BATTLEMASTER_DIALOG): 
            click_npc_option()
            sleep(0.5)
            click_npc_option()
            wait_map(self.image_path("hall"))
            close_all_dialog()
        else:
            talk_to_npc_by_map("battlemaster", 0)
            wait_for_image(SG_BATTLEMASTER_DIALOG)
            
    def talk_to_corruption_npc(self):
        #CLOSE CONFIRM REQUIRE KILL ALL DUE LAG CONNECTION CAUSING LATE SHOWN
        set_frost()
        def check_require_kill():
            if  check_image_existance([self.image_path("require_defeat"), (463,397,424,168)]): #NEED REVISION
                click(675, 512)
                return True
            
        check_require_kill() #FIX UNCLOSED REQUIRE KILL DIALOG

        if check_image_existance([self.image_path("corrupted_guard_dialog") ,NPC_DIALOG_REGION]):
            is_free_attempt_done = check_image_existance([self.image_path("free_attempt_done"), (620, 428, 126 ,32)])
            is_mob_attempt_done = check_image_existance([self.image_path("mob_attempt_done"), (698,458,110,28)]) or config.character.need_corruption_mob_attempt == False
            #CLOSE UNCLOSED DIALOG
            check_require_kill()

            if not is_free_attempt_done or not is_mob_attempt_done: #CORRUPTION DONE
                if not is_free_attempt_done: #FREE ENTRY NOT DONE  
                    click_npc_option()

                elif not is_mob_attempt_done : #MOB ENTRY NOT DONE
                    click_npc_option(2)
                    sleep(1)
                    if  check_require_kill(): 
                        click_npc_option(5)
                        close_all_dialog() #CLOSE UNCLOSED DIALOG 
                        AFK_SPOTS = [
                            (660, 417),
                            (770, 476),
                            (728, 578),
                            (626, 633),
                            (559, 436),
                            (553, 568)

                        ]
                        walk_to_map_coordinate(*(random.choice(AFK_SPOTS)), acknowledge=True) 
                        set_afk()
                        sleep(180)
                        set_afk(False)
                        return
                
                if wait_for_image([self.image_path("hall"), MAP_REGION], timeout=MAP_TIMEOUT, state=False): 
                    wait_for_condition(check_map_blank, False, MAP_TIMEOUT) 
                    #FIXED UNCLOSED DIALOG
                    close_all_dialog()

            else:
                click_npc_option(4)
                # wait_map("map/starglade")
                close_all_dialog()
                self.done = True
                self.running = False
        else:
            talk_to_npc_by_map("corrupted_guard")
            sleep(3)

    def enter_gate(self):
        INNER_BATTLEMASTER_NPC_DIALOG_REGION = [self.image_path("inner_battlemaster_npc_dialog"), NPC_DIALOG_REGION]
        
        if is_in_middle() : return
        if check_image_existance(INNER_BATTLEMASTER_NPC_DIALOG_REGION):
            click_npc_option()
            if self.first_time_claim:
                sleep(0.5)
                if walk_to_map_coordinate(729,555, acknowledge=True, allow_afk=True): 
                    sleep(1)
                    set_map_display(False)
                    set_afk()
                sleep(3)
        else:
            print(f"Macro:Corruption:Talking to Battlemaster at Instance")
            talk_to_npc_by_map("battlemaster", allow_afk=True)
            sleep(1)
            
    def claim(self):
        CLAIM_REWARD_NPC_DIALOG_LOCATION = [self.image_path("claim_npc_dialog") , NPC_DIALOG_REGION] 
        REQUIRE_KILL_ALL_EXCEPTION = ["exception/kill_all", (551, 397, 247, 168)]
        self.backtick_state = False
        if check_image_existance(CLAIM_REWARD_NPC_DIALOG_LOCATION):
            print(f"Macro:Corruption:Claiming Reward of {self.current_floor}")

            if self.current_floor == 18: 
                self.claimed = True
                return True #SKIP LV18 REWARD

            click_npc_option(1 if  self.current_floor == self.max_floor else 2 ) #TEST
            sleep(0.2)
            click_npc_option()
            sleep(2)

            if check_image_existance(CLAIMED_STATE):
                self.claimed = True
                click(527,578) #CLICK CONTINUE ON DIALOG
        
            if check_image_existance(REQUIRE_KILL_ALL_EXCEPTION): #ABNORMALLY HAPPENED
                click(672,513)
                self.kill_boss()
                sleep(0.5)
            else:
                self.claimed = True
                self.first_time_claim = False
                self.position = ""
                wait_for_condition(lambda: self.position == "start")
                return True
        else:
            if check_image_existance(["common/character_on_minimap", (1224,35,39,46)]) and not fight_boss():
                print(f"Macro:Corruption:Settling position beside claim npc #2")
                # if self.need_uncover_attempt == 0 and not self.first_time_claim:
                #     click(698,294) #UNCOVER PIXIE FROM BLOCKING NPC
                sleep(0.5) #GIVE SOME TIME TILL CHARACTER POINTER SETTLED PROPERLY
                if set_map_display(False): click(475, 480)
                sleep(0.5)

            elif self.first_time_claim and not fight_boss():  
                print(f"Macro:Corruption:First time walking to corner beside claim npc #1")
                if wait_for_condition(fight_boss, True): 
                    while(fight_boss() and self.running): sleep(1)
                set_afk(False)
                sleep(1) ##WAIT TILL AFK STATE CHANGED
                if(self.walk_to_upstair_npc()):  
                    sleep(1) ##FIX CHARACTER VISUAL GLITCh
                    self.walk_to_upstair_npc() #MAKE SURE ITS HIT DESTINATION 
                    set_afk()
                    sleep(0.2)
            else:
                self.walk_to_upstair_npc() #FIX MIDDLE MOB KEEP TARGETED WHEN AFK AT END POSITION AND OTHER MINOR BUG

    #UPDATED ON 22/5/24
    def walk_to_upstair_npc(self):
        if not self.running: return
        if not fight_boss() : 
            result =  walk_to_map_coordinate(522, 381, allow_afk=(not self.first_time_claim), acknowledge=True) #FIX UNCOSISTENT COORDINATE WHEN CLICKING ON NPC
            sleep(1) ##FIX CHARACTER VISUAL GLITCh
            result =  walk_to_map_coordinate(522, 381, allow_afk=(not self.first_time_claim), acknowledge=True) ##FIX CHARACTER VISUAL GLITCh
            return result

        return False
        
    def upstair(self):
        #TRY UPSTAIR WHEN POINTER AT END OF MAP
        if not self.running: return

        CLAIM_REWARD_NPC_DIALOG_LOCATION = [self.image_path("claim_npc_dialog") , NPC_DIALOG_REGION] 
        if check_image_existance(CLAIMED_STATE):  click(527,578) #CLICK CONTINUE ON CLAIMED DIALOG, GET RID OF IT FROM BLOCKING NPC OPTION
        if check_image_existance(CLAIM_REWARD_NPC_DIALOG_LOCATION) :
            print(f"Macro:Corruption:Checking  {self.current_floor} is it {self.floor_limit} (MAX) floor?")
            if self.current_floor == self.max_floor or self.current_floor  >= self.floor_limit:
                print(f"Macro:Corruption:Max floor has been reached, exitting instance")
                if self.current_floor == self.max_floor: click_npc_option(2)   
                elif self.current_floor  >= self.floor_limit:  click_npc_option(3)
                sleep(0.2)
                click_npc_option()
                wait_map("map/starglade")
                sleep(2)
                self.is_inside = False
                self.position = ""
                self.backtick_state = False
                set_afk(False)
            else :
                click_npc_option()
                sleep(0.2)
                click_npc_option()
                wait_for_condition(lambda: self.position == "start") 
                self.backtick_state = True
            sleep(1)
            self.claimed = False

        elif check_image_existance(["common/character_on_minimap", (1224,35,39,46)]) and not fight_boss():
            # if self.need_uncover_attempt == 0:
            #     click(698,294) #UNCOVER PIXIE FROM BLOCKING NPC
            sleep(0.5) #GIVE SOME TIME TILL CHARACTER POINTER SETTLED PROPERLY
            if set_map_display(False): click(475, 480)
            sleep(0.5)
        elif fight_mob(): 
            self.walk_to_upstair_npc() 

    def go_to_main_city(self):
        while not is_in_map(MAIN_CITY) and not self.is_inside and self.running:
            if is_in_map("tol"):
                if check_image_existance(["dialog/teleporter", NPC_DIALOG_REGION]):
                    click_npc_option(1)
                    wait_map_changed("map/tol")
                else:
                    talk_to_npc_by_map("teleporter", npc_index=2)
                continue

            if is_in_map("bloodfang"):
                if check_image_existance(["dialog/teleporter", NPC_DIALOG_REGION]):
                    click_npc_option(1)
                    wait_map_changed("map/bloodfang")
                else:
                    talk_to_npc_by_map("teleporter")
                continue

    def prepare(self):
        if not self.running: return
        set_loot_mode(item=self.need_corruption_loot, item_quality=config.character.corruption_loot_quality, radius=3)
        click(1326, 156, clicks=3) #ZOOM OUT MINI MAP
        if self.is_inside == False: self.provide_bag_space()
        self.is_prepared = True
        close_all_dialog()
      
    def init(self):
        self.running=True
        run_thread(self.read_floor)
        run_thread(self.read_pointer)
        run_thread(self.die_detector)
        run_thread(self.floor_timeout_detector)
        
        wait_for_condition(lambda:  self.first_time_read_map, False, 2 )
        if not is_in_map(self.image_path("hall")) and not self.is_inside and not is_in_map(MAIN_CITY):
            if self.faction_shortcut_unlocked: go_to_city_by_shortcut()
            else: 
                self.go_to_main_city()
        try:
            #FOR MAKESURE BAG IS EMPTY AT FIRST START OF ROUTINE
            print(f"Macro:Corruption:Starting")
            self.running = True
            if self.done : return
            if not self.is_prepared :  self.prepare()
                    
            #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
            while not self.done and self.running:   
                self.detect_location()
            print(f"Macro:Corruption:Done")
        
        except Exception as e:
            print(f"Error:Corruption:{e}")
            print(f"Macro:Corruption:Closed")
        
        




