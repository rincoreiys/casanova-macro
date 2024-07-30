from .DungeonBlueprint import *
@dataclass
class D355(Dungeon):
    dg_index_number:int = 3
    dg_page_number:int = 4
    activity_asset_directory:str = "355"
    required_space:int = 35 if config.character.focus  == "equip" else 12
    loot_config:dict =  field(default_factory=lambda: {
        f"item": True,
        f"item_quality": 3,
        "radius": 1
    }) # ALTER DEFAULT ITEM LOOT CONFIG
    boss_coordinates = {
        1: (564 ,565),
        2: (611 ,406),
        3: (946 ,589),
        4: (883 ,416),
    }
    verify_attempt:int = 3
    def verify_inside(self):
        if check_image_existance([self.image_path("verify_inside"), NPC_DIALOG_REGION]):
            self.is_inside = True
            return True
        elif  check_image_existance([self.image_path("entrance_dialog"), NPC_DIALOG_REGION]):
            self.is_inside = False
            return False
        else:
            talk_to_npc_by_map(self.image_path("entrance_link"))
            sleep(2)
            if self.verify_attempt > 0 :
                self.verify_attempt -= 1
                return self.verify_inside()
            else:
                return False

    def on_enter(self):
        if self.verify_inside():  super().on_enter()

    def on_exit(self):
        super().on_exit()
        self.verify_attempt = 3
        

    