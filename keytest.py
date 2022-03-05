from pynput.keyboard import Key, Listener, Controller
import pynput.mouse
import pyautogui
import threading

import string
keyboard = Controller()
def on_press(key):
 
    if '{0}'.format(key) in string.ascii_letters:
        print('{0}'.format(
            key))
   
def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def on_move(x, y):
#    print(x, y)
    pass

def keylistener():
        
    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def mouselistener():

#print(Key.__dict__["_member_map_"])
#inv_map = {v: k for k, v in Key._member_map_.items()}
#print(inv_map[Key.space])

    with pynput.mouse.Listener(on_move=on_move) as listener:
            listener.join()

threading.Thread(target=keylistener).start()
threading.Thread(target=mouselistener).start()

mouse = pynput.mouse.Controller()
#print(mouse.positiion)
mouse.positiion = (0, 0)

pyautogui.moveTo(10,50)
pyautogui.click()