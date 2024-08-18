from threading import Thread
from time import sleep
import socketio

from .Macro.Const import SERVER_ADDRESS
from .Global import config

class MacroNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print("CONNECTED")

    def on_disconnect(self):
        print(f"DISCONNECTED")

class Socket:
    namespace:str = f"/macro"
    sio = socketio.Client()
    
    def __init__(self) -> None:
        if config.workspace_mode != None :
            print(config.workspace_mode)
            self.sio.register_namespace(MacroNamespace(self.namespace))

    def connect(self) -> None:
        self.sio.connect(f"{SERVER_ADDRESS}?workspace_mode={config.workspace_mode}&workspace_hwnd={config.workspace_hwnd}&nickname={config.character.nickname}", namespaces=[self.namespace])
        Thread(target=self.sio.wait, daemon=True).start()

    def emit(self, event, data=None):
        print("emiiting", event, self.namespace, data)
        try:
            print("sio state: ", self.sio.connected)
            if self.sio.connected == False: 
                self.connect()
                sleep(2)
            else:
                self.sio.emit(event, data, namespace=self.namespace)
                sleep(2) # WAIT TILL REQUEST REACH THE SERVER
        except Exception as ex:
            print("Socket EX:", ex)

socket = Socket()

from .Global import config
if config.only_screenshot == False :
    print("config.only_screenshot from socket", config.only_screenshot, config.__dict__)
    socket.connect()
emit = socket.emit


