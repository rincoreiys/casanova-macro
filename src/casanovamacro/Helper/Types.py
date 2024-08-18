
from dataclasses import dataclass
import dataclasses

@dataclass
class Character:
    require_dk:list[str] = dataclasses.field(default_factory=list)
    needs:list[str] = dataclasses.field(default_factory=list)
    corruption_limit:int = 0
    dungeon_loot_quality:int = 0
    corruption_loot_quality:int = 0
    need_corruption_loot:bool = 0
    need_corruption_mob_attempt:bool = 0
    focus:str = 'item'
    routines:list[str] = dataclasses.field(default_factory=list)
    done:list[str] = dataclasses.field(default_factory=list)
    ladder_checkpoint:int = 0
    nickname:str  = ''
    faction_shortcut_unlocked:bool = False
    needs:list[str] = dataclasses.field(default_factory=list)
    exclude_junk:list[str] = dataclasses.field(default_factory=list)
    character_index:int = 0

