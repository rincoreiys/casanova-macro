
from .DungeonBlueprint import *

#UPDATED 20/5/24
@dataclass
class D175(Dungeon):
    dg_page_number:int = 2
    dg_index_number: int = 4
    loot_focus:str = "equip"
    required_space:int = 32
    activity_asset_directory = "175"
    faction_shortcut_unlocked = True
    require_dk:bool = True
    #MAPPING
    def __post_init__(self):
        self.boss_coordinates = {
            1: (441, 495),
            2: (674, 617),
            3: (555, 436),
            4: (789, 554),
            5: (673, 378),
            6: (902, 497),
            7: (892, 391), 
        }     
        self.loot_time = 10
        
    def prepare(self):
        #MUST BE TRULLY EMPTY FROM LEFTOVER EQUIP FROM ANOTHER DG
        self.bag_already_empty_before = False
        return super().prepare()
    
    def before_go_to_last_boss(self):
        self.loot_focus = "item"
        self.required_space = 4
        if self.provide_bag_space():
            self.loot_time = 15
            return True
        else: 
            self.exit()
            return False
        
    def exit(self):    
        self.required_space = 30
        self.loot_focus = "equip"
        self.loot_time = 10
        self.bag_already_empty_before = False
        go_to_city_by_shortcut()
        if not wait_for_image([self.image_path("instance"), MAP_REGION], False): self.exit()
        self.on_after_exit()