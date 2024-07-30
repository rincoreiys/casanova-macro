from .DungeonBlueprint import *
@dataclass
class D110(Dungeon):
    dg_page_number: int = 2
    def __post_init__(self):
        self.required_space = 24 if self.character_loot_focus == "equip" else  12
        self.boss_coordinates: set = [
            (464, 478),
            (897, 478),
            (654, 276),
            (686, 425),
        ]