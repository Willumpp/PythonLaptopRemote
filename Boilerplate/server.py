import threading
import socket

host = "192.168.0.40"
port = 58352

#AF_INET = internet type socket, SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() #this is for enabling the server to accept connections

clients = [] #list of client sockets
nicknames = [] #custom name client chooses

#.recv stops the current code execution until a packet is recieved
#this is why threading is needed


#sends message to every clients
#   input must already be decoded
def broadcast(message):
    for client in clients:
        client.send(message)


#This function is called for for each individual client connected
#   each client waits until they recieve a packet from themself
#"client" represents the client's socket,
#   each socket is waiting for their coresponding client to send a packet to the server
#   each socket is waiting for a request from their client
#compared to gamemaker, idk if this is better or not
#"handle()" = handle each socket
def handle(client):
    while True:
        try:
            message = client.recv(1024) #wait until a message is recieved by a client
            broadcast(message)
        except:
            #listening for socket failed...
            print("error recieving message and/or client disconnected")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat".encode("ascii"))
            break


#This is for clients connecting the server
def receive():
    while True:
        #client = the client's socket
        client, address = server.accept() #wait until a new client connects to the server
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii")) #"NICK" is the msgid representing nickname
        nickname = client.recv(1024).decode("ascii") #recieves the nickname after the request
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))

        client.send("connected to the server".encode("ascii"))

        #creates a thread for listening to the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()

#I am now going to try and convert this infastructure to something similar to my previous