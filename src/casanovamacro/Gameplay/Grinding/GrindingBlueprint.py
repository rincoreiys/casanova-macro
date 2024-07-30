
from Gameplay.Template import *
from dataclasses import dataclass
from Helper.ErrorHandler import run_thread
import Helper.Global as _

@dataclass
class Grinding(Activity):
    #GRIND SETUP
    dg_page_number = 1 # IN DG TELEPORT CLASSING
    dg_index_number = 1 # IN DG TELEPORT DG NUMBERING
    afk_coordinate = None
    category = "Grinding"
    loot_focus = _.character_focus
 
    #INSIDE DUNGEON STATE
    loot_focus = "equip"
    afk_spot_map = None
    ## BASE EVENT HANDLING
   
    #GRINDING FLOW
    def teleport(self):  
        DUNGEON_TELEPORTER_DIALOG = ["dialog/dungeon_teleporter", (462,182, 170,35)]
        if check_image_existance(DUNGEON_TELEPORTER_DIALOG):
            click_npc_option(self.dg_page_number)
            sleep(1) #FIX WRONG TELEPORTED BECAUSE FPS ISSUE
            click_npc_option(self.dg_index_number )
            wait_for_image( ["map/starglade", MAP_REGION], False,timeout=MAP_TIMEOUT)
        else:
            talk_to_npc_by_map("dungeon_teleporter" ,npc_index=2)
            wait_for_image(DUNGEON_TELEPORTER_DIALOG)

    def walk_to_afk_spot(self): pass

    def prepare(self):
        set_loot_mode(equip=True, equip_quality=0, radius=3)
        self.is_prepared = True
        close_all_dialog() 

     #MAIN FLOW
    def provide_bag_space(self): 
        number_of_empty_space = 0
        press("B")
        time.sleep(2)
        # #print( is_bag_settled(), self.backpack_settling_attempt)
        if self.backpack_settling_attempt < 3: 
            if is_bag_settled():
                self.backpack_settling_attempt = 3
                print("bag settled")
                
        if self.backpack_settling_attempt >= 3 :
            number_of_empty_space = preserve_one_slot(self.loot_focus)
            
        press("B")
        print("AVAILABLE SPACE = ", number_of_empty_space)

        self.bag_already_empty_before = number_of_empty_space >= self.required_space
        # #print("bag empty status",  self.bag_already_empty_before)
        if not self.bag_already_empty_before or  self.backpack_settling_attempt < 3: 
            if self.faction_shortcut_unlocked and not is_in_map(MAIN_CITY):
                go_to_city_by_shortcut()

    def init(self):
        self.running = True
        run_thread(self.die_detector)
        try:
            self.activity_asset_directory = (self.__class__.__name__).replace("D", "")
            #FOR MAKESURE BAG IS EMPTY AT FIRST START OF ROUTINE
            print(self.activity_asset_directory, "starting")
            if not self.is_prepared:  self.prepare()
            self.provide_bag_space()
                    
            #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
            while self.running and self.die_count < self.die_tolerance:   
                print("detect_location")
                self.detect_location()
        
        except CharacterDieException as de: 
            self.die_count += 1
            if self.die_count == self.die_tolerance: 
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
        if is_in_map(self.afk_spot_map):
            if not  self.bag_already_empty_before and self.required_space > 0 : 
                self.provide_bag_space()
            else:
                set_afk()
                close_all_dialog()
                sleep(0.2)
                
                while self.provide_bag_space():

            
        elif  is_in_map(MAIN_CITY) : 
            if not self.bag_already_empty_before : #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
                selling_equip()
                self.backpack_settling_attempt = 3
                self.bag_already_empty_before = True
            self.teleport()
            self.walk_to_afk_spot()
            
        elif not check_map_blank():  #IF IN SOME RANDOM MAP
            go_to_city_by_shortcut()
     
        
