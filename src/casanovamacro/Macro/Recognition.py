from .Base import *

check_map_blank = lambda: not check_image_existance(ONLINE_STATE_RECOGNITION_LOCATION) #UPDATED
still_talking_with_vendor =  lambda: check_image_existance(VENDOR_WINDOW_LOCATION)
is_bag_settled = lambda: check_image_existance(INVENTORY_SETTLE_STATE_RECOGNITION_LOCATION)
is_synth_window_opened = lambda: check_image_existance( ["window/synth", (580, 205, 190, 45)])
wait_map_load = lambda:  wait_for_image(ONLINE_STATE_RECOGNITION_LOCATION, True, timeout=MAP_TIMEOUT) #UPDATED
is_in_map = lambda image_path :  find_image([f"map/{image_path}" if len(str(image_path).split("/")) == 1 else image_path , MAP_REGION], confidence=0.95) is not None #UPDATED
is_insufficent_gold = lambda:  check_image_existance(NO_GOLD_RECOGNITION_LOCATION) and check_image_existance(NO_PLATINUM_RECOGNITION_LOCATION)
look_inventory_state = lambda: check_image_existance(image_path=asset_path("State/inventory_indicator"), region=(322,186, 589,240)) 
check_mob_existance = lambda: check_image_existance(["state/mob",(659, 15, 61, 30)], grayscale=False) #UPDATED 20/5/24
