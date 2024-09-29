from .Blueprint import *
BOUNTY_CLAIM_BUTTON = ["common/bounty_claim_button", (625, 426, 112, 27)]
BOUNTY_WINDOW = ["window/bounty", (613, 203, 114, 40)]
BOUNTY_ICON = ["iconbutton/bounty", (1031, 863, 35, 40)]

class ClaimBounty(Daily):
    def init(self):
        print(f"Macro:{self.__class__.__name__}:Starting")
        while not self.done:
            if not check_image_existance(BOUNTY_WINDOW):
                click_on_image(BOUNTY_ICON)
                sleep(1)
            else:
                click(707,439, clicks=2)
                sleep(1)
                self.done = True
        close_all_dialog()
        print(f"Macro:{self.__class__.__name__}:Done")


