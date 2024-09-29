from dataclasses import dataclass
from ...Macro import *
from .GrindingBlueprint import GrindGold

@dataclass
class G320(GrindGold):
    afk_spot_map = "north_river"
    afk_coordinate = (474, 477)
    dg_index_number = 1
    dg_page_number = 4
    transit_maps = ["lava_purgatory"]
    def walk_to_afk_spot(self):
        while is_in_map(self.image_path(self.afk_spot_map)) == False and self.running:
            if is_in_map(self.image_path("lava_purgatory")):
                walk_to_map_by_link(self.image_path("north_river_link"), self.image_path(self.afk_spot_map), sequence=[(684,456)] )
            elif is_in_map(MAIN_CITY): return #ANOMALLY

            
    
            


