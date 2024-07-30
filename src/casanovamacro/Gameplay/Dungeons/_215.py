from dataclasses import field
from .DungeonBlueprint import *

@dataclass
class D215(Dungeon):
    dg_index_number: int = 6
    dg_page_number:int = 2
    activity_asset_directory = "215"
    require_dk:bool =True
    loot_quality:int = 3
    done_color:list  = field(default_factory=lambda: [])
    loot_time:int = 5
    color:str = None
    boss_coordinates = {
        "yellow": (857, 551),
        "blue": (784, 391),
        "purple": (490, 462)
    }
    required_space:int = 10
    require_dk:bool = True
    default_timeout:int  = 300 #5 MIN IF NOT CLEAR ATEEMPT THEN HALT
    target_boss:int = 1
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 1 
    }) # ALTER DEFAULT ITEM LOOT CONFIG
    desired_color = ["yellow", "blue", "purple"]
    color_detector_state = False

    def color_detector(self):
        pass

    def get_buff(self, attack_duration = 5): 
        if walk_to_map_coordinate(638, 538, acknowledge=True):
            #TARGETTING STONE
            while not check_image_existance([self.image_path("stone") ,MOB_AVATAR_REGION]):
                press(192, mode="unicode") 
                sleep(0.8)

            while not check_image_existance([self.image_path("green_buff") ,CHARACTER_STATUS_REGION]) :
                press("1") #LAUNCH ATTACK TO GET BUFF
            
            sleep(1)
            while not check_image_existance([self.image_path("green_buff") ,CHARACTER_STATUS_REGION]) : #DOUBLE CHECK BUFF
                press("1") #LAUNCH ATTACK TO GET BUFF

            for i in range(attack_duration):  #MAKE SURE BUFF IS RE-GAINED
                press("1") #LAUNCH ATTACK TO GET BUFF
                sleep(1) # SET SOME DELAY WHEN RE-TAKE THE BUFF 
            
            # RELEASE TARGET
            for i in range(5): 
                press(win32con.VK_ESCAPE, mode="unicode") 
                sleep(0.1)

        else: 
            self.get_buff()

    def color_detector(self):
        while self.color == None:
            for c in self.desired_color:
                if check_image_existance([self.image_path(c) ,CHARACTER_STATUS_REGION]) and c not in self.done_color:
                    # RELEASE TARGET
                    for i in range(3): 
                        press(win32con.VK_ESCAPE, mode="unicode") 
                        sleep(0.1)

                    self.color = c
                    # MAKE SURE THE COLOR IS NOT RED
                    sleep(2)
                    if check_image_existance([self.image_path(c) ,CHARACTER_STATUS_REGION]): 
                        if self.verify_color() : 
                            self.color = c
                            break
                    else:
                        self.color = None
                        self.color_detector_state = False

    def verify_color(self):
        for c in self.desired_color:
            if check_image_existance([self.image_path(c) ,CHARACTER_STATUS_REGION])  and c not in self.done_color: return True
        return False

    def get_color(self): 
        if walk_to_map_coordinate(715, 501, acknowledge=True):
            if self.color_detector_state == False: 
                self.color_detector_state  = True
                run_thread(self.color_detector)

            #TARGETTING STONE
            while not check_image_existance([self.image_path("stone") ,MOB_AVATAR_REGION]):
                press(192, mode="unicode") 
                sleep(0.8)

            while self.color == None:   press("1")
            
            if self.verify_color(): press(win32con.VK_ESCAPE, mode="unicode") 
            else: self.get_color()
        else:
            self.get_color()
    
            
    def kill_boss(self):
        self.run_timeout_detector()
        if  len(self.done_color) == self.target_boss: 
            self.stop_timeout_detector()
            self.exit()
            self.done_color.clear()             
            self.color = None
            self.color_detector_state = False
        else:
            if len(self.done_color) == 0: self.get_buff(0)
            self.get_color()
            self.get_buff(10)
            try:
                boss_cordinate = self.boss_coordinates[self.color]
                if walk_to_map_coordinate(*boss_cordinate, True):
                    afk_if_mob_exist(loot_time=self.loot_time)
                    self.done_color.append(self.color)
                    
                if len(self.done_color) < self.target_boss : self.get_buff()
            except:
                print("Color is None, Repeat Process")
                
