
from .DungeonBlueprint import *
@dataclass
class D275(Dungeon):
    dg_page_number:int = 3
    dg_index_number: int = 2
    required_space: int = 30
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 1 
    }) # ALTER DEFAULT ITEM LOOT CONFIG
    boss_coordinates = {
        1: (833, 368),
        2: (749, 402),
        3: (548, 411),
        4: (592, 301),
        5: (676, 354),
        6: (785, 284),
    }
    

    
    def before_go_to_last_boss(self):
        self.loot_time = 13

    def on_last_boss(self):
        walk_to_map_coordinate(765, 284)
        set_afk()
        for x in range(16):
            time.sleep(0.5)
            walk_to_map_coordinate(765-20, 284)
            time.sleep(0.5)
            walk_to_map_coordinate(765+20, 284)
        self.loot_time = 0
