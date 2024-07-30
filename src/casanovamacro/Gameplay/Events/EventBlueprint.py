from ..Template import *

@dataclass
class Event(Activity):
    category:str = "Event"
    
    def detect_location(self):pass

    def on_done(self):
        self.running = False
        
    def init(self):
        print("cat", self.category)
        self.activity_asset_directory = (self.__class__.__name__)
        self.running = True
        while not self.done and self.running:   
            self.get_rid_blocking_notif()
            self.detect_location()

            