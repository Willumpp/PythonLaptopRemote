import socket
from socket_commands import *

HEADERSIZE = 10

#this is for handling sockets which exceed the buffer, whilst keeping the stream open
#   this is done with a "header", tells the size of the data incoming
#   recieving end reads the buffer stream until the size is reached


T_PORT = 58352
TCP_IP = '192.168.0.40'
BUF_SIZE = 30

server_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, T_PORT))
server_socket.listen(1) #"max_clients" or the capacity of the queue of clients


print("bound socket")

while True :
    client_socket, addr = server_socket.accept() #returns the address of the client and the socket
    print(f"conncetion from {addr} has been established")

    send_message(client_socket, "Welcome to server", HEADERSIZE)

    full_msg = ""
    new_msg = True

