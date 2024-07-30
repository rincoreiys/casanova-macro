
from .DungeonBlueprint import *
@dataclass
class D195(Dungeon):
    dg_page_number:int = 2
    dg_index_number: int = 5
    required_space: int = 18
    loot_time: int = 3
    #MAPPING
  
    def __post_init__(self):
        self.loot_config =  DEFAULT_EQUIP_LOOT_CONFIG
        self.boss_coordinates = {
            1: (465, 494),
            2: (667, 376),
            3: (847, 307),
        }  
    
    
    def on_enter(self):
        super().on_enter()
        
        while  not check_image_existance(imagePath=asset_path("Dialog/npc_dialog"), region=NPC_DIALOG_REGION): 
            press("m")
            for i in range(260, 245 + (13*11), 13):
                click(1020, i)
                time.sleep(0.02)
            press("m") 
            time.sleep(0.5) 
            if check_image_existance(imagePath=asset_path("Dialog/npc_dialog"), region=NPC_DIALOG_REGION):
                time.sleep(2)
                if check_image_existance(imagePath=asset_path("Dialog/npc_dialog"), region=NPC_DIALOG_REGION):
                    break
        
        click_npc_option()

    def on_after_exit(self):
        walk_to_map_coordinate(461,484)