import socket

HEADERSIZE = 10

#this is for handling sockets which exceed the buffer, whilst keeping the stream open
#   this is done with a "header", tells the size of the data incoming
#   recieving end reads the buffer stream until the size is reached


T_PORT = 58352
TCP_IP = '127.0.0.1'
BUF_SIZE = 30

# create a socket object name 'k'
k = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
k.bind((TCP_IP, T_PORT))
k.listen(1) #"max_clients" or the capacity of the queue of clients


print("bound socket")

while True :
    client_socket, addr = k.accept() #returns the address of the client and the socket
    print(f"conncetion from {addr} has been established")
    
    msg = "Welcome to server"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    
    client_socket.send(bytes(msg, "utf-8")) #send via the socket
