import socket

HEADERSIZE = 10
T_PORT = 58352
TCP_IP = '127.0.0.1'


k = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
k.connect((TCP_IP, T_PORT))

while True:

    full_msg = ""
    new_msg = True

    while True:
        msg = k.recv(16)
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

    print(full_msg)