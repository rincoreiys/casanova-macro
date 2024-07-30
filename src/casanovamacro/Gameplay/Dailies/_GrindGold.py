from .Blueprint import *

@dataclass
class GrindGold335(Activity):
    dg_index_number:int = 2
    dg_page_number:int = 4
    def go_to_afk_spot(self): pass
       

    def check_space(self):
        pass

    def detect_location(self):
        if is_in_map("starglade"):
            if not self.bag_already_empty_before : #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
                if(self.loot_focus == "equip") :   
                    selling_equip()
            if check_image_existance(DUNGEON_TELEPORTER_DIALOG):
                click_npc_option(self.dg_page_number)
                sleep(1) #FIX WRONG TELEPORTED BECAUSE FPS ISSUE
                click_npc_option(self.dg_index_number )
                wait_map(self.image_path("entrance"), timeout=MAP_TIMEOUT)
            else:
                talk_to_npc_by_map("dungeon_teleporter" ,npc_index=2)
                wait_for_image(DUNGEON_TELEPORTER_DIALOG)
        elif is_in_map("hot_rain_plain"):
            walk_to_map_coordinate(942, 402, True)
            set_map_display()
            click_on_image([ "boundless_fire" , (207,120, 1050,565)])
            set_map_display(False)


    def init(self):
        self.running = True
        while self.running:
            self.detect_location()


@dataclass
class GrindGold315(Activity):
    def __init__(self):
        pass

    def go_to_afk_spot(self):
        #TELEPORT TO DG 355
        pass

    def check_space(self):
        pass

    def detect_location(self):
        if is_in_map("starglade"):
            if not self.bag_already_empty_before : #PRIORITY, HAVE SOME SPACE BEFORE RUNNING DUNGEON
                if(self.loot_focus == "equip") :   
                    selling_equip()
            self.go_to_afk_spot()
        elif is_in_map(""): pass

    def init(self):
        self.running = True
        while self.running:
            self.detect_location()


