from dataclasses import dataclass

from ...Helper.Macro import *

from .GrindingBlueprint import GrindGold


@dataclass
class G340(GrindGold):
    afk_spot_map = "south_river"
    afk_coordinate = (820, 524)
    dg_index_number = 2
    dg_page_number = 4
    transit_maps = ["hot_rain_plain"]
    def walk_to_afk_spot(self):
        while is_in_map(self.image_path("south_river")) == False:
            if is_in_map(self.image_path("hot_rain_plain")):
                walk_to_map_by_link(self.image_path("south_river_link"), self.image_path("south_river"), sequence=[(482,622)] )
            elif is_in_map(MAIN_CITY): return #ANOMALLY

            
    
            


