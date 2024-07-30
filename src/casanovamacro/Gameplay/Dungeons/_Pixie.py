from .DungeonBlueprint import *
@dataclass
class DPixie(Dungeon):
    #MAPPING
    difficulty: int = 1
    npc_scroll_position=2
    required_space: int = 0
    def __post_init__(self):
        self.loot_config = {
            "item": True,
            "radius": 3
        }
        self.boss_coordinates = {
            1: (793, 463), #1 - 4 is MOB
            2: (720, 332),
            3: (617, 358),
            4: (636, 463),
            5: (679, 414), ##FINAL BOSS
        }     

    def on_done(self): 
        #CLICK LEAVE
        click_npc_option(3)
    
    def kill_boss(self):
        def fight_boss(): return check_image_existance(imagePath=self.imagePath("boss_status"), region=(731, 87, 21, 16 )) 
        # def fight_mob(): return check_image_existance(imagePath=self.imagePath("mob"), region=(624, 74, 134, 39 ))
        def afk_if_mob_exist(timeout=3):
            set_afk()
            verify = 0
            while verify < timeout:
                
                time.sleep(0.5)
                if fight_boss() and self.inner_position != 5: 
                    self.inner_position = 5
                    set_afk( False)
                    return True
                elif  check_mob_existance() : verify = 0    
                else:
                    pyautogui.press("`")
                    verify += 1

            if self.inner_position == 5:  time.sleep(self.loot_time)
            set_afk( False)
            return False
    
            
        set_afk( False)
        boss_coordinates = self.boss_coordinates[self.inner_position]
        arrive =   walk_to_map_coordinate( *boss_coordinates, acknowledge=True)
        if arrive:
            found_boss = afk_if_mob_exist()
            if not found_boss: self.inner_position += 1 #KEEP ITERATE UNTIL BOSS FOUND
            
            # self.on_move_to_other_position()
            if self.inner_position == len(self.boss_coordinates) + 1:  
                self.exit()
    
    def check_attempt_and_enter(self):
        
        theres_attempt =  check_image_existance(imagePath=self.imagePath("zero_attempt"), region=(510, 340, 350, 99)) == False
        
        if theres_attempt: 
            set_mounting(False) #UNMOUNT WHEN REACH NPC
            time.sleep(1)
            click_npc_option()
            self.is_inside = wait_for_image(imagePath=self.imagePath("instance") , region=MAP_REGION, timeout=MAP_TIMEOUT)
            return
        else: 
            self.done = True

    def on_done(self):
        while True:
            if check_image_existance(imagePath=asset_path("Dialog/npc_dialog") , region=NPC_DIALOG_REGION):       
                click_npc_option(2)
                time.sleep(1)   
                click_npc_option(1)  
                time.sleep(1)
                if check_image_existance(imagePath=self.imagePath("exchange_limit") , region=(583, 318, 199, 131)): 
                    click(682,411)
                    time.sleep(0.5)
                    if check_image_existance(imagePath=self.imagePath("exchange_limit") , region=(583, 318, 199, 131)): #DOUBLE CHECK
                        click(682,411)
                    break
            else:
                talk_to_npc_by_map(imagePath=self.imagePath("npc_link"), scroll_position=self.npc_scroll_position)
                wait_for_image(imagePath=asset_path("Dialog/npc_dialog") ,  region=NPC_DIALOG_REGION)