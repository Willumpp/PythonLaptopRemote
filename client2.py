import socket
from socket_commands import *

HEADERSIZE = 10
T_PORT = 58352
TCP_IP = '192.168.0.40'


client_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((TCP_IP, T_PORT))

sent_thing =  True

while True:

    full_msg = ""
    new_msg = True

    while True:
        msg = client_socket.recv(16)
        if new_msg:
            print(f"New messge length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recieved")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ""