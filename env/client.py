import socket
import threading
import pickle
from pynput.keyboard import Key, Listener, Controller
import pynput.mouse
import pyautogui
import string

move_mouse = False

keymap = {
    "Key.space":Key.space,
    "Key.enter":Key.enter,
    "Key.backspace":Key.backspace,
}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.40", 58352))

type = input("Recieve or send (r/s): ")
keyboard = Controller()
mouse = pynput.mouse.Controller()

def idNick(*args):
    client.send(nickname.encode("ascii"))

def idMSG(*args):
    message = args[0] #Message
    print(message)

def idHoldKey(*args):
    key = args[0]
    print(f"Key held:{key}")

    #this is because the key is recieved like 'a'
    key = key.replace("'","")
    key = key.replace("'","")

    if key in string.ascii_letters:
        keyboard.press(key)
    elif key in keymap:
        keyboard.press(keymap[key])

def idReleaseKey(*args):
    key = args[0]
    print(f"Key released:{key}")
    key = key.replace("'","")
    key = key.replace("'","")

    if key in string.ascii_letters:
        keyboard.release(key)

def idMoveMouse(*args):
    x, y = args
    pyautogui.moveTo(x * pyautogui.size()[0], y * pyautogui.size()[1])

def idMouseClick(*args):
    pyautogui.click()

client_funcs = {
    "NICK": idNick,
    "MSG": idMSG,
    "HOLDKEY":idHoldKey,
    "RELEASEKEY":idReleaseKey,
    "MVMOUSE":idMoveMouse,
    "MOUSECLICK":idMouseClick
}

def client_send(msgid, *args):
    print((msgid, args))
    message = pickle.dumps((msgid, args))

    client.send(message)


#This is for the client recieving packets from the server
def receive():
    while True:
        #try:
        msgid, args = pickle.loads(client.recv(1024)) #recieving bytes from the server
        client_funcs[msgid](*args)

        #except:
        #    print("Error with recieving message")
        #    client.close()
        #    break

def on_press(key):
    if key != Key.esc:
        client_send("HOLDKEY", "{0}".format(key))

def on_release(key):
    global move_mouse

    if key != Key.esc:
        client_send("RELEASEKEY", "{0}".format(key))
    else:
        move_mouse = not move_mouse

    if key == Key.alt:
        client_send("MOUSECLICK")

def on_move(x, y):
    global move_mouse
    if move_mouse:
        client_send("MVMOUSE", round(x / pyautogui.size()[0], 3), round(y / pyautogui.size()[1], 3))

def write_keyboard():
    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release, on_move=on_move) as listener:
        listener.join()

def write_mouse():
    # Collect events until released
    with pynput.mouse.Listener(on_move=on_move) as listener:
        listener.join()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

if type == "s":
    write_thread = threading.Thread(target=write_keyboard)
    write_thread.start()
    write_thread = threading.Thread(target=write_mouse)
    write_thread.start()