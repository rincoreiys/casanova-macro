from .DungeonBlueprint import *
@dataclass
class D85(Dungeon):
    dg_index_number: int = 7
    difficulty: int = 1
    required_space:int = 10
    require_dk:bool = True #DEFAULT VALUE
    mob_safe_coordinate = (338,326)
    
    boss_coordinates = {
            1: (945, 469),
            2: (781, 548),
            3: (607, 636),
            4: (417, 498),
            5: (641, 478),
            6: (684, 365),
            7: (507, 409)
    }
    