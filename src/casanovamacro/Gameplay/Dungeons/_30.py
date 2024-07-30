from .DungeonBlueprint import *

@dataclass
class D30(Dungeon):
    dg_index_number: int = 2
    activity_asset_directory:str = "30"
    loot_radius:int = 2
    def __post_init__(self):
        self.boss_coordinates = {
            1: (387, 495),
            2: (858, 357),
            3: (931, 594)
        }

