import socket
import pickle

HEADERSIZE = 10
T_PORT = 1234
TCP_IP = '127.0.0.1'


k = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
k.connect((TCP_IP, T_PORT))

while True:

    full_msg = b""
    new_msg = True

    while True:
        msg = k.recv(16)
        if new_msg:
            print(f"New messge length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recieved")
            print(full_msg[HEADERSIZE:])
        
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            new_msg = True
            full_msg = b""

    print(full_msg)