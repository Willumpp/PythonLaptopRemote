from pynput.keyboard import Key, Listener, Controller
keyboard = Controller()

def on_press(key):
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

keyboard.press("a")