
from ..Template import *
from dataclasses import dataclass, field
from ...Helper.ErrorHandler import run_thread
# from ...Helper.ErrorHandler import run_thread
from ...Helper.Global import config

@dataclass
class Dungeon(Activity):
    #DUNGEON SETUP
    free_attempt_done:bool = False
    dg2x_attempt_done:bool = False
    dk_attempt_done:bool = False
    require_dk:bool = False
    is_2x_dungeon:bool = False
    dg_page_number:int = 1 # IN DG TELEPORT CLASSING
    dg_index_number:int = 1 # IN DG TELEPORT DG NUMBERING
    loot_time:int = 8
    difficulty:int = 3 #1 normal 2 hard 3 NM (DEFAULT)
    boss_coordinates = {}
    is_dk_empty:bool = False
    category:str = "Dungeon"
    loot_focus:str = config.character.focus
   
    mob_safe_coordinate = None
     #SPOT TO DO TELEPORT FREE FROM INTRUPTION 
    #INSIDE DUNGEON STATE
    inner_position:int = 1
    loot_config:dict =  field(default_factory=lambda: {
        f"{config.character.focus}": True,
        f"{config.character.focus}_quality": 0 if config.character.focus  == "equip" else  config.character.dungeon_loot_quality ,
        "radius": 1 
    })
    ## BASE EVENT HANDLING
    #EVENT
    def on_enter(self):  
        close_all_dialog() 
        self.bag_already_empty_before = False #SPECIAL CASE, D175
        self.on_enter_triggered = True
    def on_move_to_other_position(self): pass #FOR DYNAMIC LOOT TIME
    def on_last_boss(self): pass
    def before_go_to_last_boss(self): pass
    def on_exit(self):
        self.on_enter_triggered = False
        self.inner_position = 1
    def on_done(self):  
        close_all_dialog()
        if(self.faction_shortcut_unlocked): go_to_city_by_shortcut()
        else: self.go_to_main_city()
    
    
    #DUNGEON FLOW
    def go_to_entrance(self):   
        if check_image_existance(DUNGEON_TELEPORTER_DIALOG):
            click_npc_option(self.dg_page_number)
            sleep(1) #FIX WRONG TELEPORTED BECAUSE FPS ISSUE
            click_npc_option(self.dg_index_number )
            wait_map(self.image_path("entrance"), timeout=MAP_TIMEOUT)
        else:
            talk_to_npc_by_map("dungeon_teleporter" ,npc_index=2)
            wait_for_image(DUNGEON_TELEPORTER_DIALOG)

    def enter_instance(self):
        
        set_party(True)
        if check_image_existance([self.image_path("entrance_dialog") , NPC_DIALOG_REGION]):
            def check_attempt( option=1): #NEED REVISION
                click_npc_option(option)
                time.sleep(1)
                theres_attempt =  check_image_existance([self.image_path("zero_attempt"), (463,427 , 422, 83) ]) == False
                #print('attempt', theres_attempt)
                if theres_attempt:
                    # click(difficulty_x , difficulty_y)
                    click_npc_option(self.difficulty)
                    if  option == 2 : 
                        time.sleep(1)
                        if check_image_existance(["exception/require_dk", (553, 398, 243, 168)]):
                            #CLICK CONFIRM
                            click(674, 516)
                            self.is_dk_empty = True
                            return False
                    else:
                        #WAIT UNTIL ENTER DUNGEON
                        wait_for_image([self.image_path("instance"), MAP_REGION])
                        
                else: 
                    click_npc_option(4)#CLICK BACK  
                    # click(590, 415)   
                
                return theres_attempt 
            
            set_mounting(False)
            self.is_2x_dungeon =  check_image_existance(["options/2x_dungeon", NPC_CHOICES_REGION])
            
            #PREFERABLE CHOOSE 2x attempt FIRST
            print("checking 2x dg")
            if not self.dg2x_attempt_done and self.is_2x_dungeon: 
                
                if not check_attempt(3) :  
                    self.dg2x_attempt_done = True
                else: 
                    self.is_inside = wait_for_image([self.image_path("instance"), MAP_REGION], timeout=4)
                    return
            
            #SECOND CHOOSE DK
            print("checking DK dg")
            if not self.dk_attempt_done and self.require_dk and self.is_dk_empty == False:
                if not check_attempt(2) :   
                    self.dk_attempt_done = True
                else: 
                    self.is_inside = wait_for_image([self.image_path("instance"), MAP_REGION], timeout=4)
                return #SPECIAL CASE RETURN

            print("checking normal attempt DG")
            if not self.free_attempt_done: 
                if not check_attempt() : 
                    self.free_attempt_done = True
                else: 
                    self.is_inside = wait_for_image([self.image_path("instance"), MAP_REGION], timeout=4)
                    return

            # #print("Free attempt", self.free_attempt_done , "paid" , self.dk_attempt_done)
            # self.done =  (
            #     self.free_attempt_done and 
            #     (self.dg2x_attempt_done == self.is_2x_dungeon ) and
            #     (self.dk_attempt_done == self.require_dk) 
            # )  #DISABLED TO AVOID ERROR WHEN RECOGNITION 2x DG EVENT STILL ON GOING ACTUALLY ITS ENDED
            self.done = True
            # if self.done :
                #print(f"{self.activity_asset_directory} DONE")
            self.on_done()  #BACK TO CITY BY DEFAULT
            return
        else:
            talk_to_npc_by_map(self.image_path("entrance_link"))
            wait_for_image([self.image_path("entrance_dialog") , NPC_DIALOG_REGION], timeout=2)


    def kill_boss(self):
          
        boss_coordinate = self.boss_coordinates[self.inner_position]
        if  self.inner_position == len(self.boss_coordinates) + 1 :
            if not self.before_go_to_last_boss(): return #LOOT EQUIP CASE , DETECT BAG IS FULL OR NOT IF FULL THEN BACK TO CITY DIRECTLY
        arrive =   walk_to_map_coordinate(*boss_coordinate, acknowledge=True)
  
        if arrive:
            # sleep()
            # print("yuii")
            afk_if_mob_exist(loot_time=self.loot_time, loot_focus=self.loot_focus)
           
            if  self.inner_position == len(self.boss_coordinates) + 1: #LAST BOSS DG 275 SPECIAL CONDITION
                self.on_last_boss()
            self.inner_position += 1
            self.on_move_to_other_position()
           
            if self.inner_position == len(self.boss_coordinates) + 1:  
                self.exit()
        else:
            sleep(1)

   
        # WILL CLEAN TRASH ON NEXT ROUTINE

    def on_after_exit(self): 
        self.is_inside = False
        self.inner_position = 1
        close_all_dialog() #CLOSE UNCLOSED DIALOG, LIKE PARTY DIALOG OR MAP BY ACCIDENTALLY STILL SHOWN
         
    def exit(self):
        set_afk(False)
        set_party(False)
        self.on_exit()
        wait_for_image([self.image_path("entrance"), MAP_REGION], timeout=MAP_TIMEOUT)
            
        self.on_after_exit()
        
    def prepare(self):
        
       

        print("loot config", self.loot_config)

        #PREPARE AFK SAFETY, AFK TIME, HO AND USE SOME USABLE TO PRESERVE MORE SPACE
        if self.loot_focus == "item": 
            click(697, 865, clicks=10)
            click(731, 865, clicks=8)
            click(768, 865, clicks=6)
            click(806, 865,clicks=1) #HO SHORTCUT
            
        sleep(0.5)
        set_loot_mode(**self.loot_config)
        self.is_prepared = True
        close_all_dialog() 

     #MAIN FLOW
    
            
    
    def init(self):
        self.running = True
        self.require_dk = self.activity_asset_directory in config.character.require_dk or self.require_dk

        run_thread(self.die_detector)
        try:
            self.activity_asset_directory = (self.__class__.__name__).replace("D", "")
            #FOR MAKESURE BAG IS EMPTY AT FIRST START OF ROUTINE
            print(self.activity_asset_directory, "starting")
            if self.done : return
            if not self.is_prepared:  self.prepare()
            if not self.is_inside:  
                if self.backpack_settling_attempt < 3:  self.settling_bag_position()
                self.provide_bag_space()
                    
            #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
            while not self.done and self.running and self.die_count < self.die_tolerance:   
                self.get_rid_blocking_notif()
                # print("detect_location")
                self.detect_location()

            if self.error is not None:
                raise self.error
            else:
                print(self.error)
                print(self.activity_asset_directory, "done")
        
        except CharacterDieException as de: 
            #DG 175 CASE. IF SOME PEEPS KILLING OUTSIDE DG 3 TIMES, HALT PROCESS
            if not self.is_inside: self.die_count += 1 
            if self.die_count == self.die_tolerance: 
                self.done = False
                self.running = False
                print("SOMEONE MIGHT HUNTING YOU, HALT THE SCRIPT")
            else:
                click(678, 475)
                time.sleep(2)
                wait_map_load()
                time.sleep(2)
                self.is_inside = False 
                self.inner_position = 1 
                press("esc") 
                self.init()

    

    #MAIN FLOW
    def detect_location(self):
        if not self.is_inside:
            if is_in_map(self.image_path(("entrance"))) :
                print("#1")
                self.is_inside = False
                if not  self.bag_already_empty_before : 
                    self.provide_bag_space()
                else: self.enter_instance()
          
            elif is_in_map(self.image_path("instance")):  
                print("#2")
                self.is_inside = True
            
            elif  is_in_map(MAIN_CITY) : 
                print("#3")
                self.is_inside = False
                if not self.bag_already_empty_before : #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
                    if(self.loot_focus == "equip") :   
                        selling_equip()
                    else: 
                        pass
                        # clean_bag(quick_clean=True, instance_obj=self) 
                    self.backpack_settling_attempt = 3
                    self.bag_already_empty_before = True
                self.go_to_entrance()
            
            elif not check_map_blank():  #IF IN SOME RANDOM MAP
                print("#4")
                print("blank")
                if self.faction_shortcut_unlocked: go_to_city_by_shortcut()
                
                # self.tp_usage += go_to_main_city()
                
        if is_in_map(self.image_path("instance")) :
            if not self.on_enter_triggered:  self.on_enter()
            elif self.is_inside:  self.kill_boss() #DG 355 FIX AFTER REVALIDATE POSITION // WHEN INSTACE MAP IS SAME AS ENTRANCE MAP

        
