from .Blueprint import *
DAILY_BONUS_WINDOW = ["window/daily_bonus", (595, 262, 163, 36)]

class ClaimDailyBonus(Daily):
    def init(self):
        print(f"Macro:{self.__class__.__name__}:Starting")
        while not self.done:
            if not check_image_existance(DAILY_BONUS_WINDOW):
                click(1179, 62)
                sleep(1)
            else:
                #LOG IN TAB
                sleep(1)
                click(504,313, clicks=2)
                sleep(.5)
                click(812,390, clicks=2)
                sleep(1)

                #COUPON TAB
                click( 571,313, clicks=2)
                sleep(.5)
                click(824,372, clicks=2)
                sleep(.5)
                self.done = True
        close_all_dialog()
        print(f"Macro:{self.__class__.__name__}:Done")


