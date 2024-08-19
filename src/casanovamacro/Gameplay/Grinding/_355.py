from dataclasses import dataclass
from ...Helper.Macro import *
from .GrindingBlueprint import GrindGold

@dataclass
class G340(GrindGold):
    afk_spot_map = "south_river"
    afk_coordinate = (1348, 1000)
    dg_index_number = 3
    dg_page_number = 4
            
    
            


