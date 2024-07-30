from .DungeonBlueprint import *
@dataclass
class D315(Dungeon):
    dg_index_number:int = 1
    dg_page_number:int = 4
    activity_asset_directory:str = "315"
    required_space:int = 30 if config.character.focus  == "equip" else 12
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 1
    }) # ALTER DEFAULT ITEM LOOT CONFIG
    boss_coordinates = {
        1: [998, 500]
    }