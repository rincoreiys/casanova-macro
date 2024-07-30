from .DungeonBlueprint import *
@dataclass
class D55(Dungeon):
    dg_index_number: int = 4
    required_space: int = 8
    def __post_init__(self):
        self.boss_coordinates = {
            1: (907, 520),
            2: (443, 618),
            3:  (936, 627),
        }