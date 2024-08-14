
from dataclasses import dataclass

@dataclass
class Character:
    require_dk:list[str]
    needs:list[str]
    corruption_limit:int
    dungeon_loot_quality:int 
    corruption_loot_quality:int
    need_corruption_loot:bool
    need_corruption_mob_attempt:bool
    focus:str
    routines:list[str]
    done:list[str]
    ladder_checkpoint:int
    nickname:str
    faction_shortcut_unlocked:bool
    character_index: int
    needs:list[str]
    exclude_junk:list[str]

