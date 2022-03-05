import socket
import threading
import pickle
from pynput.keyboard import Key, Listener, Controller

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.40", 58352))

type = input("Recieve or send (r/s): ")
keyboard = Controller()

def idNick(*args):
    client.send(nickname.encode("ascii"))

def idMSG(*args):
    message = args[0] #Message
    print(message)

def idHoldKey(*args):
    key = args[0]
    print(f"Key held:{key}")
    keyboard.press(key)

def idReleaseKey(*args):
    key = args[0]
    print(f"Key released:{key}")
    keyboard.release(key)

client_funcs = {
    "NICK": idNick,
    "MSG": idMSG,
    "HOLDKEY":idHoldKey,
    "RELEASEKEY":idReleaseKey,
}


def client_send(msgid, *args):
    message = pickle.dumps((msgid, args))

    client.send(message)


#This is for the client recieving packets from the server
def receive():
    while True:
        try:
            msgid, args = pickle.loads(client.recv(1024)) #recieving bytes from the server
            client_funcs[msgid](*args)

        except:
            print("Error with recieving message")
            client.close()
            break

def on_press(key):
    client_send("HOLDKEY", key)

def on_release(key):
    client_send("RELEASEKEY", key)

def write():
    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

if type == "s":
    write_thread = threading.Thread(target=write)
    write_thread.start()