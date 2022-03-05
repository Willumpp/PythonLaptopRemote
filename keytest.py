from pynput.keyboard import Key, Listener, Controller
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

# Collect events until released
#with Listener(on_press=on_press, on_release=on_release) as listener:
#    listener.join()
#print(Key.__dict__["_member_map_"])
#inv_map = {v: k for k, v in Key._member_map_.items()}
#print(inv_map[Key.space])
keyboard.press('a')