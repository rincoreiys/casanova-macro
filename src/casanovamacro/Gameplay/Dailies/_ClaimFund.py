from .Blueprint import *
from ...Helper.Socket import emit
DELUXE_CLAIM_BUTTON = ["common/claim_button", (791, 576, 123, 41)]
REGULAR_CLAIM_BUTTON = ["common/claim_button", (460, 576, 123, 41)]
REGULAR_CLAIMED_BUTTON = ["common/claimed_button", (460, 576, 123, 41)]
DELUXE_CLAIMED_BUTTON = ["common/claimed_button", (791, 576, 123, 41)]
PURCHASE_REGULAR_BUTTON = ["common/purchase_button", (460, 576, 123, 41)]
PURCHASE_DELUXE_BUTTON = ["common/purchase_button", (791, 576, 123, 41)]
FUND_ICON_BUTTON = ["iconbutton/fund", (864, 123, 48,48)]
FUND_WINDOW_REGION = ["window/fund", (514, 255, 316, 68)]

class ClaimFund(Daily):
    activity_asset_directory:str = "ClaimFund"
    def init(self):
        regular_claimed = False
        deluxe_claimed = False
        regular_fund_empty = False
        deluxe_fund_empty = False
        while True:
            if not check_image_existance(FUND_WINDOW_REGION):
                if not check_image_existance(FUND_ICON_BUTTON):
                    set_top_menu()
                else:
                    click_on_image(FUND_ICON_BUTTON)
                    sleep(1)
            else:
                click(800, 326 , clicks=2)
                sleep(2)
                if check_image_existance(PURCHASE_REGULAR_BUTTON):
                    regular_fund_empty = True
                elif check_image_existance(REGULAR_CLAIMED_BUTTON):
                    regular_claimed = True
                elif regular_claimed == False:
                    regular_claimed = click_on_image(REGULAR_CLAIM_BUTTON)
                    sleep(0.5)

                if check_image_existance(PURCHASE_DELUXE_BUTTON):
                    deluxe_fund_empty= True
                elif check_image_existance(DELUXE_CLAIMED_BUTTON):
                    deluxe_claimed = True
                elif deluxe_claimed == False:
                    deluxe_claimed = click_on_image(DELUXE_CLAIM_BUTTON)
                    sleep(0.5)
                break

        self.done = True
        emit("update_character_fields", {
            "deluxe_fund_claimed": deluxe_claimed,
            "regular_fund_claimed": regular_claimed,
            "regular_fund_empty": regular_fund_empty,
            "deluxe_fund_empty" : deluxe_fund_empty
        })
        close_all_dialog()
        set_top_menu(False)


