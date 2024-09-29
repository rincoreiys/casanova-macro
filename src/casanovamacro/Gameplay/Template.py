from dataclasses import dataclass
from ..Macro import *
# import Helper.Global as _
from ..Core.ErrorHandler import run_thread
@dataclass
class Activity:
    #CHARACTER SETUP
    faction_shortcut_unlocked:bool = config.character.faction_shortcut_unlocked 
    loot_focus:str= "item"
    loot_quality:int = 2
    
    #ACTIVITY INFROMATION
    category:str = ""
    activity_asset_directory:str = ""
    is_prepared:bool = False
    is_inside:bool = False
    done:bool = False
    running:bool = False
    
    required_space:int = 18
    bag_already_empty_before:bool = False
    backpack_settling_attempt:int = 0
    
    timeout_detector_state:bool = False
    default_timeout:int = 900  # 15 min

    #BASIC EVENT
    on_enter_triggered:bool = False
    
    #ERROR 
    die_count:int = 0
    die_tolerance:int = 5
    in_error_calibration:bool = False
    error: Exception = None
    

    #FUNCTION SCAFFOLDING
    def image_path(self, file): 
        return f"{self.category}/{self.activity_asset_directory}/{file}"
    
    def invalid_map_handler(self):
        while not self.done and self.running:
            if check_image_existance(image_location=["exception/invalid_map", (570,441,105,42)]): 
                click(677, 517)
            sleep(5)

    
    def timeout_detector(self):
        duration = self.default_timeout
        while not self.done and self.running and self.timeout_detector_state:
            sleep(1)
            duration -= 1
            if duration <= 0:
                self.done = False
                self.running = False
                self.timeout_detector_state = False
                break
        print(f"Macro:{self.activity_asset_directory}:Timeout!!")

    def run_timeout_detector(self):
        if self.timeout_detector_state == False: #PREVENT DUPLICATE RUNNING THREAD
            print(f"Macro:{self.activity_asset_directory}:Timeout Detector Started")
            self.timeout_detector_state = True
            run_thread(self.timeout_detector)

    def stop_timeout_detector(self):
        self.timeout_detector_state = False
        print(f"Macro:{self.activity_asset_directory}:Timeout Detector Stopped")

    def settling_bag_position(self):
        while not is_bag_settled():
            if not is_in_map(MAIN_CITY):
                if self.faction_shortcut_unlocked: go_to_city_by_shortcut()
                else :self.go_to_main_city()
            elif is_in_map(MAIN_CITY):
                if check_image_existance(["dialog/sg_seller" , NPC_DIALOG_REGION]):
                    click_npc_option()
                    time.sleep(1)
                else:
                    talk_to_npc_by_map("npc link/sg_seller", npc_index=3)
                    wait_for_image(["dialog/sg_seller" , NPC_DIALOG_REGION])
        
        self.backpack_settling_attempt = 3


    def go_to_main_city(self):
        while not is_in_map(MAIN_CITY):
            if is_in_map(self.image_path("entrance")): 
                use_tp()
                wait_map_changed(self.image_path("entrance"))
                continue
            
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


    def provide_bag_space(self): 
        #THIS FUNCTION CANT RUN IF BAG NOT SETTLED
        if self.backpack_settling_attempt < 3:  self.settling_bag_position() # VALIDATION
        
        number_of_empty_space = 0
        if not is_bag_settled(): 
            press("B")
            time.sleep(1.5)
        
        if is_bag_settled():
            number_of_empty_space = check_last_page_slots()

            self.bag_already_empty_before = number_of_empty_space >= self.required_space
            if  not self.bag_already_empty_before and self.backpack_settling_attempt >= 3:    
                if config.character.focus == "item"  : clean_bag(self.loot_focus, True)
                elif config.character.focus == "equip" : selling_equip(False)
                number_of_empty_space = check_last_page_slots()

            press("B")
            print(f"Macro:{self.activity_asset_directory}:Available bag space =  {number_of_empty_space}")
            if not self.bag_already_empty_before and self.loot_focus == "equip" and  self.faction_shortcut_unlocked and not is_in_map(MAIN_CITY):
                go_to_city_by_shortcut()
        


        self.backpack_settling_attempt = 3
   
    # def get_rid_blocking_notif(self):
    #     if check_image_existance(["exception/require_party", BLOCKING_NOTIFICATION_REGION], grayscale=True) : click(675,513)
    #     if check_image_existance(["exception/require_exit_party", BLOCKING_NOTIFICATION_REGION] , grayscale=True) : click(652,576)
    #     if check_image_existance(["exception/require_unmount", BLOCKING_NOTIFICATION_REGION] , grayscale=True) : click(674,514)
        # if check_image_existance(["exception/"]) : click()
        # if check_image_existance(["exception/"]) : click()


            
   