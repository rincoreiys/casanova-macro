from dataclasses import dataclass
from ...Macro import *
from .GrindingBlueprint import GrindGold

@dataclass
class G310(GrindGold):
    afk_spot_map = "volcano_world"
    afk_coordinate = (597, 591)
    dg_index_number = 1
    dg_page_number = 4
    transit_maps = ["lava_purgatory", "lava_world"]
    def walk_to_afk_spot(self):
        while is_in_map(self.image_path(self.afk_spot_map)) == False and self.running:
            if is_in_map(self.image_path("lava_purgatory")):
                walk_to_map_by_link(self.image_path("lava_world_link"), self.image_path("lava_world"), sequence=[(965,355)] )
            elif is_in_map(self.image_path("lava_world")):
                walk_to_map_by_link(self.image_path("volcano_world_link"), self.image_path("volcano_world"), sequence=[(868,441)] )
            elif is_in_map(MAIN_CITY): return #ANOMALLY

            
    
            


