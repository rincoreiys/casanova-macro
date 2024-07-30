
from .DungeonBlueprint import *
@dataclass
class D255(Dungeon): 
    dg_page_number:int = 3
    dg_index_number:int = 1
    required_space:int = 18
    activity_asset_directory:str = "255"
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 2
    }) # ALTER DEFAULT ITEM LOOT CONFIG
  
    def kill_boss(self):
        walk_to_map_coordinate(693, 505, acknowledge=True)
        set_afk()
        sleep(340) #5 MIIN 40 SEC
        set_afk(False)
        self.exit()
    
    