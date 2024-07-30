
from .DungeonBlueprint import *
@dataclass
class D165(Dungeon):
    dg_page_number: int = 2
    dg_index_number: int = 3
    required_space: int = 18
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 1
    }) # ALTER DEFAULT ITEM LOOT CONFIG
  
    boss_coordinates = {
        1: (799, 392),
        2: (550, 392)
    }

    def on_enter(self):
        #TAKE BUFF
        super().on_enter()
        while not check_image_existance([self.image_path("inside_npc_dialog") , NPC_DIALOG_REGION]):
            talk_to_npc_by_map(self.image_path("inside_npc_link"))
            time.sleep(0.5)
        click_npc_option()
    
    def exit(self):
        while not check_image_existance([self.image_path("inside_npc_dialog"), NPC_DIALOG_REGION]):
            talk_to_npc_by_map(self.image_path("inside_npc_link"))
            time.sleep(0.5)
        
        click_npc_option(3)
        if wait_for_image([self.image_path("entrance"), MAP_REGION], timeout=MAP_TIMEOUT): 
            self.is_inside = False
        self.on_exit()