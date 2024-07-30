## MORE COMPLEX GAME FUNCTION 
from ...Helper.Macro.Game import * 
from ...Helper.Global import * 

#UPDATED 20/5/24 WORKING ALPHA
def open_synth_window():
    if check_image_existance(SYNTH_WINDOW_LOCATION) == False:
        click(*SYNTH_BUTTON_LOCATION)
        sleep(0.5)
        click_on_image(SYNTH_WINDOW_LOCATION)
        return wait_for_image(SYNTH_WINDOW_LOCATION, timeout=3)
    else:
        return True

#UPDATED 20/5/24 WORKING ALPHA
def synthesis_aterfact():         
    #UPDATED
    ARTEFACT_CATEGORY_OPTION = ["options/artefact_category", (557,546,99,26)]
    FOCUSED_ARTEFACT_CATEGORY_OPTION = ["options/artefact_category_focused", (557,546,99,26)]
    ARTEFACT_ESSENCE_IMAGE = ["props/artefact_essence", (517,283,313,212)]

    def select_category():
        click(682,258)
        sleep(0.5) #SELECT CATEGORY
        click(804, 553, clicks=4, step=0.1) #SCROLL TILL BUTTOM

        if wait_for_image(ARTEFACT_CATEGORY_OPTION) or wait_for_image(FOCUSED_ARTEFACT_CATEGORY_OPTION): 
            if click_on_image(ARTEFACT_CATEGORY_OPTION) or click_on_image(FOCUSED_ARTEFACT_CATEGORY_OPTION):
                click(671, 237) # GET RID ITEM DESCRIPTION POPUP
                return True
        return False
    

    def refresh():
        if  check_image_existance(["options/artefact_category_selected", (559, 247, 80, 25)]) == False:  
            select_category()
        else:
            click(675,279)
            sleep(0.3)
            click(675, 340)
            sleep(0.3)
            click(675, 279)
            sleep(0.3)
            click(675, 299)
        sleep(1.5)
    
    while True: 
        open_synth_window()
        if check_image_existance(ARTEFACT_ESSENCE_IMAGE):
            print("ESSENCE FOUND")
            click(548, 308, clicks=2)
            sleep(0.3)
            click(*COUNTER_UP_BUTTON_LOCATION) #COUNTER UP PRESS 
            sleep(0.3)
            click(*PROC_SYNTH_BUTTON_LOCATION)
            sleep(2) #WAIT FOR SYNTH PROCESS
            refresh()
        else:
            refresh()
            if not check_image_existance(ARTEFACT_ESSENCE_IMAGE): break

            print("Nothing to synthetized")
            
    click(754, 762) #CLOSE THE SYTNH DIALOG, SOMETIME ACCIDENTALLY PRESSING D HOTKEY
    return True
        
def check_has_money():
    pass
    # return check_image_existance()
    

def synthesis_gems():
    GEMS_CATEGORY_OPTION = ["options/gems_category", (559,267,252,308)]#-
    GEMS_CATEGORY_SELECTED = ["options/gems_category_selected", (559,246,227,24)] #-
    FOCUSED_GEMS_CATEGORY_OPTION = ["options/gems_category_focused", (557,546,99,26)] #-
    GEMS_INDEX = ["ruby", "topaz", "amber", "saphire", "jade", "emerald"]
    GEMS_GRADE_POSITION = [(545,310),(685,310), (545,350), (685, 350)] #FLAWED, SCRATCHED, NORMAL, SHINING
    
    def select_gems_category():
        while check_image_existance(GEMS_CATEGORY_SELECTED) == False: 
            click(685, 260)
            sleep(0.8)
            #RESET SCROLLBAR FIRST
            click(804, 284, clicks=5)
            sleep(0.8)

            click_on_image(GEMS_CATEGORY_OPTION)
            
            

    def select_gems_subcategory(subcategory_index=0):
        while check_image_existance([f"state/gems/selected_sub_{GEMS_INDEX[subcategory_index]}", (557, 269, 256,22)]) == False:
            if is_synth_window_opened()  :
                click(600, 280)
                sleep(0.3)
                click(600, 320 + (20*subcategory_index))
                sleep(0.3)
            else:
                return False
        return True

    def synth_gems_proc():
        pc_empty = False
        for i in range(2): #DOUBLE CHECK
            for gems_index in range(len(GEMS_INDEX) ):
                if select_gems_subcategory(gems_index) == False:  return False #HANDLE IF SOMETHING WRONG HAPPENED, EG WINDOW MOVED OR CLOSED
                for grade in range(len(GEMS_GRADE_POSITION)):
                    print("grade is ", grade)
                    if  pc_empty and grade == 3: continue #SKIP SYNTH SHINING GEMS  IF PC EMPTY
                    
                    if is_synth_window_opened() == False: return False
                    click(*GEMS_GRADE_POSITION[grade])
                    sleep(1)
                    click(*COUNTER_UP_BUTTON_LOCATION, clicks=3)
                    sleep(0.3)
                    click(*PROC_SYNTH_BUTTON_LOCATION)
                    sleep(0.5)
                    if grade == 3 :
                        pc_empty = check_image_existance(["state/gems/empty_pc",  (536,440, 287, 45)])  #CHECKING PC
                        if pc_empty: continue
                   
                    while (
                        check_image_existance([f"state/gems/empty_{GEMS_INDEX[gems_index]}", (536,440, 287, 45)]) == False
                        and check_image_existance(["state/gems/empty_pc",  (536,440, 287, 45)]) == False 
                        and is_synth_window_opened()
                        ):  #HANDLE IF SOMETHING WRONG HAPPENED, EG WINDOW MOVED OR CLOSED
                        # if grade == 3:
                       
                        print("pc empty: ", pc_empty, " grade: ", grade )
                        click(*COUNTER_UP_BUTTON_LOCATION, clicks=2)
                        sleep(1)

        return True

    while True:
        if is_synth_window_opened():
            select_gems_category()
            if synth_gems_proc(): return True
        else:
            if is_bag_settled():
                if check_has_money() == False: return False
                else:
                    open_synth_window()
            else:
                press("B")
                sleep(1)
                if is_bag_settled(): continue
                else:
                    press("B")
                    settling_bag_position()

   
#UPDATED 30/5/24 
def read_empty_space( sorted=False): #UPDATED
    
    last_page_coordinate = (763,617)
    click(594, 365) #CLICK ALL TAB FIRST
    sleep(1)
   
    click(*last_page_coordinate, clicks=3 ) #CLICK PAGE 6
    if not sorted:  click(853,368)  # CLICK SORT BUTTON FIRST
    time.sleep(5)
    
    try:
        from ...Helper.Macro.Base import image_storage
        number_of_empty_space =  len(list(pyautogui.locateAll(needleImage=asset_path("state/empty_slot.png"), haystackImage=image_storage.image,  confidence=DEFAULT_CONFIDENCE, region=BAGPACK_REGION)))
        print("THERE IS ENOUGH SPACE")
        return number_of_empty_space
    except Exception: 
        return 0

def repair_equip():
    if still_talking_with_vendor():
        click(151, 539)
        time.sleep(1)
        # if wait_for_image(imagePath=asset_path("Dialog/repair_equip"), region=(617, 312, 141, 30),  timeout=5):
        click(724, 458 )
        time.sleep(2)
        click(785, 330 ) #CLOSE UNCLOSED REPAIR DIALOG
        print("Repair Done")
        return

    elif check_image_existance(imagePath=asset_path("Dialog/npc_dialog"), region=NPC_DIALOG_REGION):
        click(845, 282)
        time.sleep(0.5)
        click(545,355) 
        
        time.sleep(2)
        return
        
        # #print("ee", still_talking_with_vendor(), is_bag_settled())
    else:
        talk_to_npc_by_map(imagePath=asset_path("NPC Link/sg_seller"), scroll_position=4)
        wait_for_image(imagePath=asset_path("Dialog/npc_dialog"), region=NPC_DIALOG_REGION)
   
    repair_equip()

def drop_junk(quick_clean=False):
    #print(quick_clean, "qc")
    
    path_of_the_directory= asset_path("Quick Junk" if quick_clean else "Junk")
    files = list(filter(lambda filename : os.path.isfile(os.path.join(path_of_the_directory,filename)) ,  os.listdir(path_of_the_directory)))
    print(files)
    click_confirm()   #CLICK UNCLOSED CONFIRM DIALOG
    time.sleep(1)
        
    result = None
    def get_junk_coordinates():
       
        junks = []
        for file in files:
            from ...Helper.Macro.Base import image_storage
            f = os.path.join(path_of_the_directory,file)
            print("f is", f)
            
            try:
                result  = list(pyautogui.locateAll(needleImage=f, haystackImage=image_storage.image,  confidence=DEFAULT_CONFIDENCE, region=BAGPACK_REGION, grayscale=False))
                def idt(c):
                    x, y ,w , h = c
                    return x+round(w/2), y+round(h/2)
                junks += map(idt ,result)
            except Exception as e: pass
        return junks

    print("reading junk ",  result)
    
    for i in range(2): #DOUBLE CHECKING JUNK
        junk_coordinates =  get_junk_coordinates()
        for c in junk_coordinates:
            click_confirm()  #CLICK UNCLOSED CONFIRM DIALOG
            if is_bag_settled(): 
                drag(start=c, end=(1172,533))
                sleep(1)
                click_confirm()

        print("JUNK COORDINATES", junk_coordinates)
 
def check_last_page_slots(loot_focus):
    if is_bag_settled():
        click(*BAG_SORT_BUTTON_LOCATION) #CLICK SORT BUTTON
        sleep(3)
        click(*BAG_PAGE_NUMBER_LOCATION[0], clicks=2) #CLICK LAST PAGE ON BAGPACK
        sleep(1)
        return read_empty_space(loot_focus)
    else:
        print("PAGE UNEXPECTEDLY CLOSED")
        return 0

def clean_bag(loot_focus, quick_clean:bool = False):
    
    def clean_junk(): 
        #CLICK PAGE 6 FIRST
        for page_number in BAG_PAGE_NUMBER_LOCATION:
            if is_bag_settled():
                click(*page_number, clicks=2 ) #CLICK ON PAGE NUMBER
                time.sleep(2)
                if not check_image_existance(EMPTY_PAGE_LOCATION):
                    # pass
                    print("PAGE ", page_number, "JUNKS", )
                    drop_junk(quick_clean)
            
            else: return False
        
    if is_bag_settled():
        if  clean_junk() == False: return False
        check_last_page_slots(loot_focus)
        if   not quick_clean :  synthesis_gems()
        return True
    else:
        press("B")
        sleep(1)
        clean_bag(loot_focus, quick_clean)

def settling_bag_position():
    while not is_bag_settled():
        if is_in_map(MAIN_CITY):
            if check_image_existance(["dialog/sg_seller" , NPC_DIALOG_REGION]):
                click_npc_option()
                time.sleep(1)
            else:
                talk_to_npc_by_map("npc link/sg_seller", npc_index=3)
                wait_for_image(["dialog/sg_seller" , NPC_DIALOG_REGION])
        elif config.character.faction_shortcut_unlocked:
            go_to_city_by_shortcut()

 #UPDATED 20/5/24 WORKING ALPHA
def selling_proc(brief_selling=False):
    timeout = 50 
    result = False
    click(686, 365, clicks=3 ) #CLICK EQUIP TAB FIRST
    sleep(0.5)
    
    while True:
        if not still_talking_with_vendor(): return False
        click(417, 680) #CLICK SELL BUTTON
        for ii in [
            (590,390),
            (626,390),
            (664,390),
            (702,390),
            (738,390),
            (778,390),
            (590,438),

        ]:
            click(*ii)
            sleep(0.1)
            click(746,334) # CLICK INVENTORY TITLE TO GET RID POPUP
            sleep(0.1)
            click_confirm()

      
        try:
            timeout -= 1
            from ...Helper.Macro.Base import image_storage
            number_of_empty_slot = len(list(pyautogui.locateAll(needleImage=asset_path("state/empty_slot.png"), haystackImage=image_storage.image,  confidence=DEFAULT_CONFIDENCE, region=BAGPACK_REGION)))
            result = number_of_empty_slot > 30 or timeout <= 0 
            print("number_of_empty_slot", number_of_empty_slot  )
        except Exception: pass
        finally: 
            sleep(1)
            click_confirm() #CLOSE UNCLOSED CONFIRMATION DIALOG
            click_on_image(INVENTORY_SETTLE_STATE_RECOGNITION_LOCATION) #GET RID EQUIP DESCRIPTION POPUP
            if result or brief_selling: return True


 #UPDATED 20/5/24 WORKING ALPHA
def selling_equip():   
    extract_artefact_result = False     
    while True:  #REPEAT THE PROCCESS UNTIL SELLING DONE
        if still_talking_with_vendor() and is_bag_settled():
            selling_proc(True)
            if not extract_artefact_result:
                extract_artefact_result = synthesis_aterfact()
            time.sleep(0.5)
            if not selling_proc(): selling_equip() #IF PROCESS WHEN SELLING IS INTRUPTED OR DIALOG CLOSE UNINTENTIONALLY, RUN THE PROCESS FROM THE START
            print("SELLING EQUIP DONE")
            press(win32con.VK_ESCAPE, mode="unicode") # CLOSE ALL NPC SHOP WINDOW
            sleep(0.1)
            press(win32con.VK_ESCAPE, mode="unicode") # CLOSE BAG
            return True

        elif check_image_existance(["dialog/sg_seller" , NPC_DIALOG_REGION]):
            click_npc_option()
            time.sleep(2)
        else:
            talk_to_npc_by_map("npc link/sg_seller", npc_index=3)
            wait_for_image(["dialog/sg_seller" , NPC_DIALOG_REGION])


#UPDATED 20/5/24 WORKING ALPHA
def go_to_city_by_shortcut():
    if not is_in_map(MAIN_CITY):
        set_top_menu()
        sleep(1.5)
        if click_on_image(FACTION_FEATURE_REGION):
            sleep(1.5)
            if check_image_existance(FACTION_WINDOW_LOCATION):
                click(570, 639)
                sleep(1)
                wait_map("map/starglade")
                time.sleep(1)
        set_top_menu(False)
        close_all_dialog()


def check_routine_by_event_tab(): #UPDATED

    
    undone_routine = [item for item in config.character.routines if item not in config.character.done]
    # print(undone_routine[0])
    #CLOSE THE EVENT TAB
    close_all_dialog()
    return undone_routine

def use_energy_particle():
    drag(start=(804, 942), end=(876, 301))