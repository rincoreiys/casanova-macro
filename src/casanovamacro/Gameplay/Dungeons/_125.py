from .DungeonBlueprint import *
@dataclass
class D125(Dungeon):
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 1
    }) # ALTER DEFAULT ITEM LOOT CONFIG
    phase:str = ""
    battle_setup_state:int = False
    timer_activated:bool = False
    activity_asset_directory:str = "125"

    
    def on_enter(self):
        super().on_enter()
        self.phase = "enter_stone_zone"
        while self.battle_setup_state == False:
            if check_image_existance(AFK_WINDOW_LOCATION):
                
                if click_on_image(["common/mob_checklist", (425,311,24,24)]) : 
                    self.battle_setup_state = True
                
                #DOUBLE CHECK
                if check_image_existance(["common/mob_checklist", (425,311,24,24)]) == False:
                    self.battle_setup_state = True           
                set_loot_mode(radius=1)
                sleep(1)
                close_all_dialog()
            else:
                click(*AFK_ICON_LOCATION)
                wait_for_image(AFK_WINDOW_LOCATION)
        

    def on_after_exit(self):
        self.battle_setup_state = False
        super().on_after_exit()
    
    def enter_instance(self):
        set_party(True)
        if check_image_existance([self.image_path("entrance_dialog") , NPC_DIALOG_REGION]):
            def check_attempt( option=1): #NEED REVISION
                click_npc_option(option)
                time.sleep(1)
                theres_attempt =  check_image_existance([self.image_path("zero_attempt"), (463,427 , 422, 83) ]) == False
                if theres_attempt: click_npc_option()
                else: click_npc_option(2) 
                
                return theres_attempt 
            
            set_mounting(False)
            self.is_2x_dungeon =  check_image_existance(["options/2x_dungeon", NPC_CHOICES_REGION])
            
            #PREFERABLE CHOOSE 2x attempt FIRST
            if not self.dg2x_attempt_done and self.is_2x_dungeon: 
                if not check_attempt(2) :  
                    self.dg2x_attempt_done = True
                else: 
                    self.is_inside = wait_for_image([self.image_path("instance"), MAP_REGION], timeout=4)
                    return
                
            if not self.free_attempt_done: 
                if not check_attempt() : 
                    self.free_attempt_done = True
                else: 
                    self.is_inside = wait_for_image([self.image_path("instance"), MAP_REGION], timeout=4)
                    return

            self.done = True
            # if self.done :
            print(f"Macro:{self.activity_asset_directory}:Done")
            self.on_done()  #BACK TO CITY BY DEFAULT
            return
        else:
            talk_to_npc_by_map(self.image_path("entrance_link"), npc_index=2)
            wait_for_image([self.image_path("entrance_dialog") , NPC_DIALOG_REGION], timeout=2)


    def detect_location(self):
        if not self.is_inside:
            if is_in_map(self.image_path(("entrance"))) :
                self.is_inside = False
                if not  self.bag_already_empty_before : 
                    self.provide_bag_space()
                else: self.enter_instance()
          
            elif is_in_map(self.image_path("instance")):  
                self.is_inside = True
       
            
            elif not check_map_blank():  #IF IN SOME RANDOM MAP
                if self.faction_shortcut_unlocked: go_to_city_by_shortcut()
                
                # self.tp_usage += go_to_main_city()
                
        elif is_in_map(self.image_path("instance")) :
            if not self.on_enter_triggered:  self.on_enter()
            match self.phase:
                case "enter_stone_zone":
                    if check_image_existance([self.image_path("stone_npc_dialog"), NPC_DIALOG_REGION]) and self.timer_activated == False:
                        sleep(2)
                        if check_image_existance([self.image_path("stone_npc_dialog"), NPC_DIALOG_REGION]):
                            click_npc_option()
                            click_npc_option()
                            click_npc_option()
                            self.timer_activated = True
                    elif check_image_existance([self.image_path("stone_npc_dialog"), NPC_DIALOG_REGION]) and self.timer_activated == True:
                        sleep(2)
                        if check_image_existance([self.image_path("stone_npc_dialog"), NPC_DIALOG_REGION]):
                            click_npc_option()                                
                            self.phase = "kill_stone"
                    else:
                        map_state = set_map_display()
                        if map_state:     
                            for i in range(344, 344 + (17*8), 17):
                                click(1040, i)
                                time.sleep(0.05)

                        set_map_display(False)
                case "kill_stone":
                    afk_if_mob_exist(loot_time=0, radius=1)
                    self.phase = "teleport_to_guardian_area"
                case "teleport_to_guardian_area":
                    if check_image_existance([self.image_path("chronosphere_dialog"), NPC_DIALOG_REGION]) :
                        sleep(2)
                        if check_image_existance([self.image_path("chronosphere_dialog"), NPC_DIALOG_REGION]) :
                            click_npc_option()
                            self.phase = "kill_guardian_one"
                    else:
                        if walk_to_map_coordinate(819,623, acknowledge=True):
                            sleep(1)
                            click(425, 398)
                case "kill_guardian_one":
                    if walk_to_map_coordinate(658, 553, acknowledge=True): 
                        afk_if_mob_exist(radius=3)
                        self.phase = "kill_guardian_two"
                case "kill_guardian_two":
                    
                        if walk_to_map_coordinate(480, 491, acknowledge=True): 
                            afk_if_mob_exist(radius=3)
                            self.phase = "talk_to_black_hole"
                case "talk_to_black_hole": 
                    if check_image_existance([self.image_path("evil_land_teleport_dialog.png") , NPC_DIALOG_REGION]):
                        click_npc_option(2)
                    else:
                        talk_to_npc_by_map(self.image_path("evil_land_teleport"))
                case "kill_boss":
                    if walk_to_map_coordinate(877, 511, acknowledge=True):
                        afk_if_mob_exist()
                        self.exit()


                        
                    

                
                    
                    

        
