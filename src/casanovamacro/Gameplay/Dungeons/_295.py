
from .DungeonBlueprint import *
@dataclass
class D295(Dungeon):
    dg_page_number:int = 3
    dg_index_number: int = 3
    required_space: int = 24

    def __post_init__(self):
        self.loot_config =  DEFAULT_EQUIP_LOOT_CONFIG
        self.boss_coordinates = {
            1: (594, 441),
            2: (550, 364),
            3: (646, 325),
            4: (867, 402),
            5: (700, 495),
            6: (654, 412)
        }
    