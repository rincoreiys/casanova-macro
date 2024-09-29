from ...Core.Thread import run_thread
from .Blueprint import *
@dataclass
class Ladder(Daily):
    activity_asset_directory:str = "Ladder"
    required_space:int = 10

    def die_detector(self):      
        print(f"Macro:{self.__class__.__name__}:Die Detector Started")
        while not self.done and self.running:
            if check_image_existance(["exception/die", (503,377, 341, 237)]):
                self.in_error_calibration = True
                click(673, 597)
                sleep(2)
                self.is_inside = False
                self.in_error_calibration = False
                break
            sleep(2)

        print(f"Macro:{self.__class__.__name__}:Die Detector Stopped")

    def go_to_entrance(self):
        if check_image_existance(TELEPORTER_DIALOG) :
            click_npc_option(3)
            wait_map(self.image_path("entrance"))
        else:
            talk_to_npc_by_map("teleporter" , npc_index=4)
            wait_for_image(TELEPORTER_DIALOG)

    def on_done(self):
        if self.faction_shortcut_unlocked and len([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ]) > 0: 
            while not is_in_map(MAIN_CITY):
                go_to_city_by_shortcut()
           
    def enter_instance(self):
        set_party()
        if check_image_existance([self.image_path("entrance_dialog"), NPC_DIALOG_REGION]):

            #CLAIM UNCLAIMED REWARD
            if(click_on_image([self.image_path('collect'), NPC_CHOICES_REGION])):
                sleep(1)
                return self.enter_instance() #DO RECURSIVE
            
            set_mounting(False)
            time.sleep(0.2)
            click_on_image([self.image_path(config.character.ladder_checkpoint), NPC_CHOICES_REGION])
            time.sleep(1)

            #CHECK ATTEMPT
            if check_image_existance([self.image_path("zero_attempt"), NPC_CHOICES_REGION]) == False:
                click_npc_option()
                if wait_map(self.image_path(f"instance{config.character.ladder_checkpoint}")): 
                    self.is_inside = True
            else:
                click_npc_option(3)
                self.done = True

        else:
            talk_to_npc_by_map(self.image_path("entrance_link"))
            wait_for_image([self.image_path("entrance_dialog"), NPC_DIALOG_REGION])

            
    def claim(self): 
        claimed = False
        claim_option_clicked = False
        while not claimed:
            if check_image_existance([self.image_path("entrance_dialog"), NPC_DIALOG_REGION]):
                #TO MAKE SURE ITS CLAIMED
                time.sleep(1)
                if check_image_existance([self.image_path('collect'), NPC_CHOICES_REGION]):
                    if click_on_image([self.image_path('collect'), NPC_CHOICES_REGION]): claim_option_clicked = True
                elif claim_option_clicked and check_image_existance([self.image_path('collect'), NPC_CHOICES_REGION]) == False :
                    claimed = True
            else:
                talk_to_npc_by_map(self.image_path("entrance_link"))
                wait_for_image([self.image_path("entrance_dialog"), NPC_DIALOG_REGION])


    def detect_location(self):
        if self.in_error_calibration: 
            sleep(5)
            return
        # self.get_rid_blocking_notif()
        if not self.is_inside:
            if is_in_map(self.image_path(("entrance"))) :
                self.enter_instance()
          
            elif is_in_map(self.image_path(f"instance{config.character.ladder_checkpoint}")):  
                print(f"Macro:Ladder:Character at {config.character.ladder_checkpoint} floor")
                self.is_inside = True
            
            elif  is_in_map(MAIN_CITY) : 
                if not self.bag_already_empty_before : #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
                    self.backpack_settling_attempt = 3
                    self.bag_already_empty_before = True
                self.go_to_entrance()
            
            elif not check_map_blank():  #IF IN SOME RANDOM MAP
                if self.faction_shortcut_unlocked: go_to_city_by_shortcut()
                
        if self.is_inside:
            self.exit()


    def init(self): 
        self.running = True
        run_thread(self.die_detector)
        try:
            #FOR MAKESURE BAG IS EMPTY AT FIRST START OF ROUTINE
            print(f"Macro:{self.__class__.__name__}:Starting")
            if self.done : return

            #IF ITS ONLY LEADDER AUTOMATION NO NEED TO SETTLE 
            if not self.is_inside and len([routine for routine in config.character.routines if routine not in EXCLUSIVE_ROUTINES ]) > 1:  
                if self.backpack_settling_attempt < 3:  self.settling_bag_position()
                self.provide_bag_space()

            
            #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
            while not self.done and self.running :   
                self.detect_location()

            sleep(2)
            print(f"Macro:Ladder:Done")
        
        except CharacterDieException as de: 
            click(678, 475)
            time.sleep(2)
            wait_map_load()
            time.sleep(2)
            self.is_inside = False 
            self.inner_position = 1 
            press("esc") 
            self.init()

    def exit(self):
        set_party(False)
        wait_for_image([self.image_path("entrance"), MAP_REGION], timeout=MAP_TIMEOUT)
        #CLAIM REWARD
        
        self.claim()
        self.done = True
        self.on_done()
        