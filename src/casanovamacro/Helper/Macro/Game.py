## SIMPLE GAME FUNCTION 
from ...Helper.Macro.Recognition import *


#UPDATED 20/5/24   WORKING ALPHA
def set_party(state=True): #UPDATED
    result = check_image_existance(PARTY_STATE_RECOGNITION_LOCATION) is not  state 
    if result :
        press("P")
        time.sleep(0.5)
        click( *((395, 632) if state else (395,646)))
        press("P")
    return result

#UPDATED 20/5/24   WORKING ALPHA
def set_peace_mode(): 
    click(93,9)
    time.sleep(0.5)
    click(144,27)

#UPDATED 20/5/24 WORKING ALPHA
def set_mounting(state = True):
    result = check_image_existance(MOUNTED_STATE_RECOGNITION_LOCATION) is not  state 
    if result :  press("Z")
    time.sleep(0.2)

#UPDATED 20/5/24 WORKING ALPHA
def set_afk(state = True, radius=None):
    result = False
    if check_image_existance(AFK_WINDOW_LOCATION):
        click_on_image(AFK_WINDOW_LOCATION, clicks=2) #GET RID AFK BUTTON HOVER GLOWING EFFECT
        if state and radius is not None: 
            click( 586 , 440, clicks=3) #RESET RADIUS
            # #INCREASING RADIUS
            if radius > 1 :
                click( 648 , 440, clicks=radius-1) 

        result = ( 
            click_on_image([f"state/{'afk_off' if state else 'afk_on'}", AFK_STATE_BUTTON_REGION]) 
            or click_on_image([f"state/{'afk_off_hover' if state else 'afk_on_hover'}", AFK_STATE_BUTTON_REGION]) 
            or check_image_existance([f"state/{'afk_off' if state else 'afk_on'}", AFK_STATE_BUTTON_REGION]) 
            or check_image_existance([f"state/{'afk_off_hover' if state else 'afk_on_hover'}", AFK_STATE_BUTTON_REGION])  
            ) #STRICT LOGIC
        
        #MAKE SURE ITS REALLY TURNED
        # if  state == False and result == False:  
        #     click_on_image(AFK_WINDOW_LOCATION) #GET RID AFK BUTTON HOVER GLOWING EFFECT
           
        #     result = ( 
        #         wait_for_image(["state/afk_on", AFK_STATE_BUTTON_REGION], False,  timeout=5)
        #         or wait_for_image(["state/afk_on_hover", AFK_STATE_BUTTON_REGION],  False,  timeout=5) == False
        #         )
        #     print("FINAL state", result)
                
        # if state == False:
        click(*AFK_ICON_LOCATION) #CLOSE AFK DIALOG
        sleep(1)
        close_all_dialog()
        # click(1200, 710) #CLICK SOME RANDOM POINT TO GET RID RANDOM POP UP
        return result
    else:
        click(*AFK_ICON_LOCATION)
        wait_for_image(AFK_WINDOW_LOCATION)
        #click(1200, 710) #CLICK SOME RANDOM POINT TO GET RID RANDOM POP UP
        return set_afk(state)

#UPDATED 20/5/24 WORKING ALPHA
def set_top_menu(state=True): # INIT MEAN  UNCOVER HIDE TOP MENU BUTTON FROM EQUIP DURABILITY INDICATOR
    # if is_in_map(imagePath=asset_path('Map/sg')):  walk_to_map_coordinate(810, 475, acknowledge=True, timeout=7) #PREVENT TELEPORT TO CRAGSTONE BY WALKING TO KALENDRA VENDOR
    #STABILIZE HIDE TOP MENU BUTTON
    if check_image_existance(TOP_MENU_OFF_STATE if state else TOP_MENU_ON_STATE, confidence=0.98):
        print(f"TOP MENU {state}")
        click(1126,46)
        sleep(0.5)
        return
    
    #PREVENT ERROR BECAUSE EQUIPMENT BROKEN INDICATOR COVERING THE ICON
    if(check_image_existance(TOP_MENU_ON_STATE) or  check_image_existance(TOP_MENU_OFF_STATE)) == False:
        # print(f"TOP MENU COVERED BY EQUIP")
        # click(887, 134) #OPEN FUND DIALOG FOR TEMPORARY
        # sleep(0.5)
        # click(887, 134) #OPEN FUND DIALOG FOR TEMPORARY
        # # sleep(1.5)
        click(1126,46)
        sleep(0.5)
       
        return set_top_menu(state)

#UPDATED 20/5/24 WORKING ALPHA
def set_loot_mode(item = False, item_quality=2, equip=False, all=False, equip_quality=0, radius=1): #UPDATED
    #MAKE SURE OPEN AFK DIALOG
    
    if check_image_existance(AFK_WINDOW_LOCATION):
        time.sleep(2) #LET DIALOG FULLY OPENED
        
        # if equip is item : item = not equip #PREVENT BOTH TRUE NEED TOGGLER
        
        #CHECKLIST FIRST WORKING WITH TOGGLE CASE FOR EFFICIENCY
        if  check_image_existance(['state/checked',(420, 644, 24, 24 )]) is not all:
            click(432, 656)
            time.sleep(0.2)
        if  check_image_existance(['State/checked', (420, 668, 24, 24 )]) is not equip:
            click(432, 679)
            time.sleep(0.2)
        if  check_image_existance(['State/checked', (420, 688, 24, 24 )]) is not item:
            click(432, 699)
            time.sleep(0.2)

        #DETERMINE QUALITY
        #EQUIP

        if equip:
            click(603, 679)
            time.sleep(0.2)
            click(603, 700 + (20*equip_quality))
            time.sleep(0.6)

        if item:
            click(603,699)
            time.sleep(0.2)
            click(603, 722 + (20*item_quality))
            time.sleep(0.6)

        #SET RADIUS
        #RESET FIRST
        click( 586 , 440, clicks=3) #DECRESE RADIUS
        
        # #INCREASING RADIUS
        if radius > 1 :
            click( 648 , 440, clicks=radius-1) 

        sleep(0.5)
        click(*AFK_ICON_LOCATION)
        time.sleep(1)
        
    elif not check_image_existance(AFK_WINDOW_LOCATION): 
        click(*AFK_ICON_LOCATION)
        time.sleep(2)
        return set_loot_mode(item, item_quality, equip, all, equip_quality, radius)

    # #MAKE SURE CLOSE AFK DIALOG
   
#UPDATED 20/5/24 WORKING ALPHA
def set_frost(state=True): #UPDATED
    result = check_image_existance(FROST_STATE_RECOGNITION_LOCATION) is not  state 
    if result : press("S")


#UPDATED 20/5/24 WORKING ALPHA
def set_map_display(state = True): #UPDATED    
    if check_image_existance(MAP_WINDOW_LOCATION) is not state and check_map_blank() == False: #DONT SPAM OPEN MAP IF MAP LOADER STILL RUNNING
        print("map opened")
        press("M")
        # time.sleep(0.5)
        wait_for_image(MAP_WINDOW_LOCATION, state)
    print("MAP IS ", check_image_existance(MAP_WINDOW_LOCATION) )
    return check_image_existance(MAP_WINDOW_LOCATION) == state
   
#UPDATED 20/5/24 WORKING ALPHA
def walk_to_map_coordinate(x=0,y=0, acknowledge=False, allow_afk=False, sequence=None, timeout=5, let_dialog_opened = False): #UPDATED
    CHARACTER_POINTER_ON_MAP_LOCATION  = ["common/character_on_map", (x-15, y-15, 30, 30)]
    result = False
    if allow_afk == False: 
        if check_image_existance(AFK_STATE_RECOGNITION_LOCATION): 
            press("n") # n = .
            sleep(1)
    if set_map_display(): 
        if sequence is not None:
            for x, y in sequence:
                print("x", x)
                print("y", y)
                click(x, y, clicks=(10 if allow_afk  else 1))
                if acknowledge:
                    result = wait_for_image(CHARACTER_POINTER_ON_MAP_LOCATION, timeout=timeout)
                time.sleep(0.2)
        else:   
            click(x, y, clicks=(10 if allow_afk  else 1))
            if acknowledge:
                while not check_image_existance(CHARACTER_POINTER_ON_MAP_LOCATION) and timeout >= 0:
                    click(x, y)
                    sleep(0.5)
                    timeout -= .5
                result =  timeout > 0
                # if not result: result = walk_to_map_coordinate(x, y, ac)
                

        print("walk_to_map_coordinate", result)
        time.sleep(0.2)

    set_map_display(let_dialog_opened)
        
    return result   

def walk_to_map_by_link(destinaton_map_link, map_destination, sequence=[], acknowledge=False, timeout=5):
    #SEQUENCE USEFULL TO HANDLE STUCK ON PORTAL
    while not is_in_map(map_destination):
        if set_map_display():
            for x, y in sequence:
                CHARACTER_POINTER_ON_MAP_LOCATION  = ["common/character_on_map", (x-15, y-15, 30, 30)]
                if acknowledge:
                    while not check_image_existance(CHARACTER_POINTER_ON_MAP_LOCATION) and timeout >= 0:
                        click(x, y)
                        sleep(0.5)
                        timeout -= .5
                else:
                    click(x, y)
                    sleep(2)

            
                timeout = 5
            click_on_image([destinaton_map_link, MAP_LINK_REGION])
            if is_in_map(map_destination): pass
        

#UPDATED 20/5/24 WORKING ALPHA
def scroll_npc_list_on_map(index=0):
    click_on_image(MAP_SCROLL_LOCATION("up"), clicks=13*5+5)
    print("aaa", index)
    if index > 0 :
        print("aaa")
        click_on_image(MAP_SCROLL_LOCATION("down"), clicks=13*index)

#UPDATED 20/5/24 WORKING ALPHA
def talk_to_npc_by_map(npc_name, npc_index=0, allow_afk=False): 
    print("FROM talk_to_npc_by_map")
    result = False

    #RELATIVE OR ABSOLUTE PATH
    npc_link = [(f"npc link/{npc_name}") if len(npc_name.split("/")) == 1 else npc_name, NPC_LIST_REGION]
    print("npc_link", npc_link)
    if allow_afk == False: 
        if check_image_existance(AFK_STATE_RECOGNITION_LOCATION): press("n") # n = .
    if set_map_display():
        sleep(0.8)
        print("CHECKING IMG", check_image_existance(npc_link))
        if  check_image_existance(npc_link) == False:  
            scroll_npc_list_on_map(npc_index)
            sleep(1)
        result = click_on_image(npc_link, confidence=0.99)
        sleep(1)
        
    set_map_display(False)
    return result

#UPDATED 20/5/24 WORKING ALPHA
def close_all_dialog(): 
    check_attempt = 2
    while True: 
        if click_on_image(CLOSE_BUTTON_DIALOG_LOCATION): sleep(0.5)
        else: 
            check_attempt -= 1
            sleep(1)
            if(check_attempt <= 0): break

    print("ALL DIALOG CLOSED")
        
#UPDATED 20/5/24 WORKING ALPHA       
def click_npc_option(option=1): #UPDATED
    print(485, 434 + ((25 * (option-1)) + 13))
    click(485, 434 + ((25 * (option-1)) + 13))


#UPDATED 20/5/24 WORKING ALPHA   
def wait_map(image_path,timeout=MAP_TIMEOUT ): #UPDATED
    if  wait_for_image([image_path, MAP_REGION], timeout=timeout, confidence=0.95 ):
        time.sleep(2) #SOLVE MAP RENDER GLITCH
        if is_in_map(image_path):   return True
    return False

#UPDATED 20/5/24 WORKING ALPHA   
def afk_if_mob_exist(loot_time=3, timeout=5,  loot_focus="item", radius=None):
    set_afk(radius=radius)
    verify = 0
    step = 1
    while verify <= timeout:
        sleep(step)
        if  check_mob_existance() : verify = 0
        else:
            # pyautogui.press("`")
            verify += 1

     #LOOT PURIFIED CRYSTAL IF POSSIBLE
    while loot_time > 0 :
        if loot_focus == "equip":
            click_on_image([ "other/pc_on_ground", (33,33, 1282, 700)])
            sleep(0.05)
            click_on_image([ "other/pc_on_ground_text", (33,33, 1282, 700)])
        sleep(step)
        loot_time -= step

    set_afk(False)

#UPDATED 20/5/24 WORKING ALPHA   
def click_teleport_scroll(current_map=None):
    click(541,867) 
    time.sleep(5) #CAST TELEPORT TIMEo

    #WAIT UNTIL MAP CHANGED
    if current_map is not None: wait_for_image(image_location=current_map, state=False, timeout=MAP_TIMEOUT  )
    time.sleep(2)
    while check_map_blank(): time.sleep(1) #WAIT UNTIL MAP LOADED
    return 1

#UPDATED 20/5/24 WORKING ALPHA   
def click_confirm():
    CONFIRM_BUTTON_LOCATION = ["common/confirm",(57, 31,1166,648)]
    if click_on_image(CONFIRM_BUTTON_LOCATION):
        time.sleep(0.2)

#UPDATED 20/5/24 WORKING ALPHA   
def set_pixie(state:bool):
    if not check_image_existance(PET_WINDOW_LOCATION): press("X")
    #MAKE SURE OPEN
    if not wait_for_image(PET_WINDOW_LOCATION):   press("X")
    click(158, 2925)
    time.sleep(1)
    click(26, 332, clicks=2)
    # time.sleep(3)
    click((44 if state else 102), 483, clicks=2)
    press("x")
    if not wait_for_image(PET_WINDOW_LOCATION, state=False):   press("X")
    return state


def wait_map_changed(previous_image):
    sleep(1)
    wait_map_load()
    return  wait_for_image([ previous_image, MAP_REGION ] , False)

#ALWAYS RUN THIS EVERY LOGED IN
def claim_coupon():
    if wait_for_image(["window/daily_bonus", (616, 264, 114,34)]):
        click(574, 312) # ONLINE TAB
        sleep(0.6)
        click(827, 373) #CLICK CLAIM
        sleep(0.1)
        click(1180, 62) # CLOSE DAILY BONUS WINDOW
    else:
        click(1180, 62) # OPEN DAILY BONUS WINDOW
        sleep(0.5)
        return claim_coupon()
    
def purchase_tp_from_fate_shop():
    if not wait_for_image(["window/fate_shop", (540, 211, 82,77)]):
        click(1176, 162) #OPEN FATE SHOP
        sleep(1)
        return purchase_tp_from_fate_shop()
    
    if not check_image_existance(["state/selected_coupon_tab", (424, 284, 64, 46)]) :
        click(457, 306) # CLICK COUPON TAB
        sleep(1)
        return purchase_tp_from_fate_shop()
    else:
        click(881,388)
        sleep(0.5)
        click(844, 406)

        sleep(0.5)
        click(1176, 162) #CLOSE FATE SHOP

def use_tp():
    if(check_image_existance(["state/empty_tp", (520,844, 43,43)])):
        ###PURCHASE TP USING COUPON###
        purchase_tp_from_fate_shop()
        
    click(*TP_SHORTCUT_COORDINATE)
    sleep(5)

def change_line():
    if(check_image_existance(["state/line_one", (1216,38, 6,10)])):
        click(1216,38)
        sleep(0.5)
        click(1126,61)

        #WAIT TILL MAP REFRESHED
        wait_for_condition(check_map_blank,timeout=3)
        wait_for_condition(check_map_blank, False)


def claim_fund(): pass
