
import ctypes
import pyautogui, time, os, win32api, win32gui, win32con, win32ui
from ctypes import windll, wintypes
from time import sleep

import casanovamacro
from ...Helper.Global import *
from ...Helper.Macro.Const import *
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
class ImageStorage:
    image:Image = None
    state:bool = False

image_storage = ImageStorage()

def asset_path(path):  return  os.path.join(*casanovamacro.__path__, f"Assets/img/{path}")
pyautogui.FAILSAFE = False
def click( x=0, y=0, clicks=1, step=0.01): #UPDATED
    for click in range(clicks):
        lParam = win32api.MAKELONG(x, y)
        config.flash.SendMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.01)
        config.flash.SendMessage(win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
        time.sleep(step)

def right_click( x=0, y=0, clicks=1, step=0.01): #UPDATED
    for click in range(clicks):
        lParam = win32api.MAKELONG(x, y)
        config.flash.SendMessage(win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
        time.sleep(0.01)
        config.flash.SendMessage(win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, lParam)
        time.sleep(step)
        
def drag(start=(0,0), end=(0,0)): #UPDATED
        startlParam = win32api.MAKELONG(*start)
        endlParam = win32api.MAKELONG(*end)
        config.flash.SendMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, startlParam)
        time.sleep(0.4)
        config.flash.SendMessage(win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, endlParam)
            
    
def press(key = None, mode="char"):  #UPDATED
    key = key if mode != "char" else ord(key)
    config.flash.SendMessage( win32con.WM_KEYDOWN, key, 0)
    config.flash.SendMessage( win32con.WM_KEYUP, key, 0)



class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]
    

def screenshot(show=False): #UPDATED
    # restore_flash()
    # minimize_flash()
    try:
        image_storage.state = False
        hwnd:int =  config.flash_hwnd
        # restore_flash()
        # sleep(0.2)
        
        rect = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        # left, top, right, bot = rect
        
        w = rect.right - rect.left
        h = rect.bottom - rect.top
        # print("rct",  w, h)
        
        hwndDC = user32.GetWindowDC(hwnd)
        mfcDC  =  win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC = gdi32.CreateCompatibleDC(hwndDC)

        # print("mfdc", mfcDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        sleep(0.3)
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        gdi32.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        user32.ReleaseDC(hwnd, hwndDC)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        # # im.show()
      
        image_storage.image = im
        if raw_find_image(["exception/blank_screenshot",( 0, 0 , 1364,64)]):
            print("FAILED")
            raise Exception()
        
        image_storage.state =  True
        # # if SCREENSHOT_STATE: minimize_flash()
        # # return SCREENSHOT_IMAGE
        if show: 
            Thread(target=im.show).start()
            sleep(1)
            
        
            # image.save(os.path.join(*casanovamacro.__path__, "Temp", f"{config.flash_hwnd}{time.time()}.png") )
        
    except Exception as ex:
        print("Grab image failure", ex)
        
    # print("ppp", os.path.join(*casanovamacro.__path__))
  
   
def find_image(image_location, confidence=DEFAULT_CONFIDENCE, grayscale=False) -> pyautogui.Point : #UPDATED 
  
    while not image_storage.state: 
        # print("screnshot state from find_image", image_storage.state)
        sleep(0.1)
    try:
        if(image_storage.image is None):     screenshot()
        result = pyautogui.locate(needleImage=f"{asset_path(image_location[0])}.png", 
                                  haystackImage=image_storage.image , 
                                  confidence=confidence, 
                                  region=image_location[1],
                                  grayscale=grayscale)
        return result
    except pyautogui.ImageNotFoundException:
        print(f'Image not Found {image_location[0]}')
        return None
    except  Exception as ex:
        print("IMG Find Image Failure", ex)
    

def raw_find_image(image_location, confidence=1, grayscale=False) -> pyautogui.Point :
    try:
        return pyautogui.locate(needleImage=f"{asset_path(image_location[0])}.png", 
                                    haystackImage=image_storage.image , 
                                    confidence=confidence, 
                                    region=image_location[1],
                                        grayscale=grayscale)
    except pyautogui.ImageNotFoundException:
        return None

def check_image_existance(image_location, confidence=DEFAULT_CONFIDENCE, grayscale=False) : #UPDATED
    result = find_image(image_location, confidence=confidence, grayscale=grayscale) 
    print(image_location[0], result, confidence, DEFAULT_CONFIDENCE)
    return result is not None

def minimize_flash():  config.flash.SendMessage(win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE) #UPDATED
def restore_flash(): config.flash.SendMessage(win32con.WM_SYSCOMMAND, win32con.SC_RESTORE) #UPDATED
    
def wait_for_image(image_location, state = True, timeout=2, confidence=DEFAULT_CONFIDENCE, step = 0.5): #UPDATED
   
    while True:
        # print(F"WAITING IMAGE {image_location[0]}")
      
        if check_image_existance(image_location, confidence) is not state :
            
            timeout -= step
            if timeout <= 0: 
                return False
        else:
            print(F" IMAGE FOUND {image_location[0]}")
            return True
        sleep(step)#in second unit



def wait_for_condition(condition, ret_value=True,timeout=5, step=0.5):  #UPDATED
    while timeout > 0:
        if condition() is ret_value: return True
        timeout -= step
        time.sleep(step)
    return False

def click_on_image(image_location, clicks = 1, confidence=DEFAULT_CONFIDENCE, timeout=None) : #UPDATED
    image =  find_image(image_location, confidence)
    print(" click img", image_location, image)
    if image is not None:
        x, y, w, h = image
        click(x+ int(w/2), y + int(h/2), clicks)
        return True
    return False
