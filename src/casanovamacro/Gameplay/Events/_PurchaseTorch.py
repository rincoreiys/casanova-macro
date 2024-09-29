from .EventBlueprint import *

class PurchaseTorch(Event):
    #MAIN FLOW
    lucky_pack_claimed:bool = False
    torch_purchase_done:bool = False

    def detect_location(self):
        if  is_in_map(MAIN_CITY) : 
            if check_image_existance(["dialog/mysterious_man", NPC_DIALOG_REGION]):
                if check_image_existance(["options/mysterious_gifts", NPC_CHOICES_REGION]):
                    click_npc_option()                    
                    sleep(1)
                    if self.lucky_pack_claimed == False:
                        if check_image_existance([self.image_path("lucky_pack_claimed"), NPC_CHOICES_REGION]) :
                            self.lucky_pack_claimed = True
                        else:
                            click_npc_option()
                            return

                    if self.torch_purchase_done == False:
                        if check_image_existance([self.image_path("require_gold"), BLOCKING_NOTIFICATION_REGION]):
                            self.torch_purchase_done =  True
                            click(674, 516)

                        if check_image_existance([self.image_path("torch_zero_purchase_attempt"), NPC_CHOICES_REGION]):
                            self.torch_purchase_done = True   
                        else:
                            click_npc_option(2)
                            return 
                    self.done = self.torch_purchase_done and self.lucky_pack_claimed   
                else:
                    self.done =True

                if self.done: self.on_done()
            else:
                talk_to_npc_by_map("mysterious_man", npc_index=1)

        elif not check_map_blank():  #IF IN SOME RANDOM MAP
            if config.character.faction_shortcut_unlocked: go_to_city_by_shortcut()
            


