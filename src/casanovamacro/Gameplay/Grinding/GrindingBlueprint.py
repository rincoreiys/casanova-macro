
from ...Gameplay.Template import *
from dataclasses import dataclass


@dataclass
class GrindGold(Activity):
    #GRIND SETUP
    dg_page_number = 1 # IN DG TELEPORT CLASSING
    dg_index_number = 1 # IN DG TELEPORT DG NUMBERING
    afk_spot_map = None
    afk_coordinate = (0,0)
    transit_maps = []
    category:str = "Grind Gold"
    bag_already_empty_before:bool = False
    loot_focus:str= "equip"
    required_space:int = 6

    #GRINDING FLOW
    def teleport(self):  
        
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
        set_peace_mode()
        set_frost()
        close_all_dialog() 

    def init(self):
        self.running = True
        print(self.dg_index_number, self.dg_page_number)
        
        run_thread(self.die_detector)
        run_thread(self.invalid_map_handler)
        try:
            self.activity_asset_directory = (self.__class__.__name__).replace("G", "")
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
        
        if is_in_map(self.image_path(self.afk_spot_map)):
            
            if   self.bag_already_empty_before  == False:    self.provide_bag_space()
            else:
                if  walk_to_map_coordinate(*self.afk_coordinate, acknowledge=True):
                    set_afk()
                    sleep(10)
                    set_afk() #DOUBLE CHECK
                    close_all_dialog()
                    sleep(0.2)
                    if is_bag_settled() == False and self.backpack_settling_attempt >= 3: press("B") #MONITOR BAG
                    sleep(1)
                    check_last_page_slots(False) 
                    for x in range(3): #HANDLE IMAGE MISSMATCHING RECOGNITION
                        self.bag_already_empty_before = read_empty_space(True) >  0 #DOUBLE CHECK
                        while self.bag_already_empty_before:
                            self.bag_already_empty_before = read_empty_space(True) >  0
                            sleep(0.5)
                    set_afk(False)
                    go_to_city_by_shortcut()
                            
        elif  is_in_map(MAIN_CITY) : 
            if not self.bag_already_empty_before : #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
                selling_equip(need_synth_artefact=False)
                self.backpack_settling_attempt = 3
                self.bag_already_empty_before = True
            self.teleport()
            self.walk_to_afk_spot()
            
        
        elif not check_map_blank():  #IF IN SOME RANDOM MAP
            at_one_of_transit_maps = False
            for m in self.transit_maps:
                if is_in_map(self.image_path(m)): 
                    at_one_of_transit_maps = True
                break
            
            if at_one_of_transit_maps == False: 
                go_to_city_by_shortcut()
            else:
                self.walk_to_afk_spot()
     
        
