from .DungeonBlueprint import *

@dataclass
class D75(Dungeon):
    required_space:int = 10
    dg_index_number: int = 6
    in_chamber: bool = False
    require_dk:bool = True
    chamber_entrance = {
        1: { 
            "map_point" : (828,514),
            "npc_position": (442,188),
        },
        2: {
            "map_point" : (772,456),
            "npc_position": (426,326),
        },
        3:  {
            "map_point" : (624,484),
            "npc_position": (367,373),
        },
        4: {
            "map_point" : (582,553),
            "npc_position": (372,377),
        } ,
        5:  {
            "map_point" :(582,662),
            "npc_position": (388,365),
        },
    }
    boss_coordinates = {
            1: (888, 439), #
            2: (799, 362), #
            3: (545, 409), #
            4: (453, 548), #
            5: (462, 671), #
        }

    
    def on_move_to_other_position(self): 
        #FOR DYNAMIC LOOT TIME
        self.loot_time = self.loot_time + (self.inner_position * 1.8)
        
    def exit_chamber(self):
        while  self.in_chamber:
            if check_image_existance([self.image_path("entrance_chamber_dialog"),  NPC_DIALOG_REGION]):
                click_npc_option()
                time.sleep(2) #PREVENT DIALOG GLITCH
                if check_image_existance([self.image_path("entrance_chamber_dialog"),  NPC_DIALOG_REGION]):
                    click_npc_option()
                    time.sleep(0.1)
                    #PREVENT OVERLAPPING DIALOG
                    click_npc_option(2)
                    self.in_chamber = False

            else:
                #RETURN IF INNER BOSS ALL KILLED
                map_state = set_map_display()
                if map_state:     
                    for i in range(328, 328 + (17*9), 17):
                        click(1040, i)
                        time.sleep(0.05)

                set_map_display(False)
                time.sleep(0.5)

    def kill_boss(self):
        boss_coordinates = self.boss_coordinates[self.inner_position]
        entrance_coordinate = self.chamber_entrance[self.inner_position]
       
        if  self.in_chamber and self.is_inside : 
            afk_if_mob_exist(loot_time=self.loot_time, timeout=4)
            if  self.inner_position == len(self.boss_coordinates):
                self.in_chamber = False
                #reset dynamic time loot
                self.loot_time = 8
                self.exit()
                
                return 
            else: 
                self.exit_chamber()
                self.inner_position += 1
        elif self.is_inside:
            retry_talk = 0 
            self.run_timeout_detector()
            while not self.in_chamber and self.running:
                if check_image_existance([self.image_path("entrance_chamber_dialog"), NPC_DIALOG_REGION]):
                    click_npc_option()
                    time.sleep(2) #PREVENT DIALOG GLITCH
                    if check_image_existance([self.image_path("entrance_chamber_dialog"), NPC_DIALOG_REGION]):
                        click_npc_option()
                        time.sleep(1)
                        self.in_chamber = True
                        walk_to_map_coordinate(*boss_coordinates, acknowledge=True)
                        time.sleep(2 + (self.inner_position / 4 ))
                else: 
                    arrive_to_chamber_entrance = walk_to_map_coordinate( *entrance_coordinate['map_point'], acknowledge=True, timeout=6) #HANDLE FOR SLOW MOVEMENT SPEED
                    set_mounting(False)
                    if arrive_to_chamber_entrance:
                        time.sleep(1) #FIX CHARACTER POSITION GLITCH
                        click( *entrance_coordinate['npc_position'])
                        wait_for_image([self.image_path("entrance_chamber_dialog"), NPC_DIALOG_REGION], timeout=1.5)
                    else:
                        retry_talk += 1
                        #STUCK INSIDE CASE WHEN LAG SO BAD NEED SOME HANDLER
                        if retry_talk == 5: 
                            self.in_chamber = True
                            self.exit_chamber()

            self.stop_timeout_detector()               
    