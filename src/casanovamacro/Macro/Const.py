#CONFIG
DEFAULT_CONFIDENCE = 0.98
MAP_TIMEOUT = 20
MAIN_CITY = "starglade"
TP_SHORTCUT_COORDINATE = (539, 867)
EXCLUSIVE_ROUTINES = ["Ladder", "ClaimFund", "ClaimDaily", "PurchaseTorch"]

#COORDINATE
AFK_ICON_LOCATION = (860,949) #UPDATED 20/5/24
SYNTH_BUTTON_LOCATION = (847, 466)
PROC_SYNTH_BUTTON_LOCATION = (663,760)
BAG_SORT_BUTTON_LOCATION = (855,365)
HIDE_PLAYER_BUTTON_LOCATION = (1303,180)
HIDE_EFFECT_BUTTON_LOCATION = (1274, 180)
BAG_PAGE_NUMBER_LOCATION = [
            (762,619), #PAGE 6
            (726,619),
            (694,619),
            (656,619),
            (621,619),
            (585,619),
        ] #START FROM THE LAST ONE #UPDATED 22/5/24


#NPC PAGE INDEX 
BATTLEMASTER_INDEX =  0
COUNTER_UP_BUTTON_LOCATION = (598, 754)


#REGION
MOB_AVATAR_REGION = (555, 0 ,310 , 50)
CHARACTER_STATUS_REGION =  (250, 0, 811,90 )
BAGPACK_REGION = (561, 369, 242, 242)  #UPDATED 20/5/24
MAP_REGION = (1172, 0, 176, 38) #UPDATED 20/5/24
MAP_LINK_REGION = (663, 430, 653, 413)
NPC_DIALOG_REGION = (447, 312, 457, 119) #UPDATED 20/5/24
NPC_CHOICES_REGION = (455, 430, 411, 512)
NOTIFICATION_CENTER_SCREEN_DIALOG_REGION = (455,447,440,166) #UPDATED 21/5/24
MAP_SCROLL_REGION = (720,223, 609, 556) #UPDATED 20/5/24
TOP_MENU_BUTTON_REGION = (1100, 20, 50, 50) #UPDATED 20/5/24
NPC_LIST_REGION =  (700,234, 566, 520) #UPDATED 20/5/24
AFK_STATE_BUTTON_REGION = (618,772,110,30) #UPDATED 20/5/24 
FACTION_FEATURE_REGION = ["iconbutton/faction", (797,166,59,55)] #UPDATED 20/5/24 
ONLINE_STATE_RECOGNITION_LOCATION = ["state/online", (208, 15, 43,43)] #UPDATED 20/5/24 
CLOSE_BUTTON_DIALOG_LOCATION = ["common/close_dialog_button", (208,20, 1100, 800)] #UPDATED 20/5/24 
MAP_SCROLL_LOCATION = lambda x : [f"common/scroll_{x}_button", MAP_SCROLL_REGION ] #UPDATED 20/5/24 
EMPTY_PAGE_LOCATION = ["state/empty_page", BAGPACK_REGION]
BLOCKING_NOTIFICATION_REGION = (347,229,761,534)
SYNTH_REQUIREMENT_REGION = (518, 425, 311, 64)
SYNTH_CATEGORY_OPTIONS_REGION = ()


#DIALOG
DUNGEON_TELEPORTER_DIALOG = ["dialog/dungeon_teleporter", NPC_DIALOG_REGION]
TELEPORTER_DIALOG = ["dialog/teleporter", NPC_DIALOG_REGION]



#WINDOW
AFK_WINDOW_LOCATION = ["window/afk", (487,737,93,25)] #UPDATED 20/5/24 
VENDOR_WINDOW_LOCATION = ["window/npc_vendor", (242, 295, 47 ,28)]  #UPDATED 20/5/24 
INVENTORY_WINDOW_LOCATION =  ["window/inventory" , (709, 320, 67, 28)]  #UPDATED 20/5/24 
PET_WINDOW_LOCATION = ["window/pet", (0,280, 97,27)]  #UPDATED 20/5/24 
MAP_WINDOW_LOCATION = ["window/map_on", (798,103,411, 223)] #UPDATED 20/5/24 
FACTION_WINDOW_LOCATION = ["window/faction",(507,420,53,161)]  #UPDATED 20/5/24 
SYNTH_WINDOW_LOCATION = ["window/synth", (546,193, 281, 62)] #UPDATED 20/5/24 
#STATE
NO_GOLD_RECOGNITION_LOCATION = ["state/no_gold", (662,534,19,18) ]
NO_PLATINUM_RECOGNITION_LOCATION = ["state/no_plat", (622, 534, 32, 19)]
FROST_STATE_RECOGNITION_LOCATION = ["state/frost", CHARACTER_STATUS_REGION] #UPDATED 20/5/24
PARTY_STATE_RECOGNITION_LOCATION = ["state/party", (0, 1, 26,23 )]   #UPDATED 20/5/24
INVENTORY_SETTLE_STATE_RECOGNITION_LOCATION = ["window/inventory", (708 , 323, 71, 21)] #WORKS
MOUNTED_STATE_RECOGNITION_LOCATION = ["state/mounted", (21,92,26,29)]  #UPDATED 20/5/24
AFK_STATE_RECOGNITION_LOCATION = ["state/afk", (623,175,50,18)]
IS_IT_LINE_ONE_STATE = ["state/line1", (1215, 38, 6, 10)] #UPDATED 26/5/24
TOP_MENU_ON_STATE = ["state/top_menu_on", TOP_MENU_BUTTON_REGION] #UPDATED 20/5/24
TOP_MENU_OFF_STATE = ["state/top_menu_off", TOP_MENU_BUTTON_REGION] #UPDATED 20/5/24
ONLINE_STATE_RECOGNITION_LOCATION = ["state/online", (205, 16, 47,39)]#UPDATED 26/5/24
MOB_STATE_RECOGNITION_LOCATION = ["state/mob", (661,26,36,10)]




