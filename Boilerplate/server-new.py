import threading
import socket
import pickle #This is used for encoding data sctructures and sending them accross network

host = "192.168.0.40"
port = 58352

#AF_INET = internet type socket, SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() #this is for enabling the server to accept connections

clients = [] #list of client sockets
nicknames = [] #custom name client chooses



def broadcast_raw(message):
    for client in clients:
        client.send(message)

def client_send_raw(client, message):
    client.send(message)


def broadcast(msgid, *args):
    message = pickle.dumps((msgid, args))
    broadcast_raw(message)


def client_send(client, msgid, *args):
    message = pickle.dumps((msgid, args))
    client_send_raw(client, message)





def handle(client):
    while True:
        try:
            message = client.recv(1024) #wait until a message is recieved by a client
            broadcast_raw(message)
        except:
            #listening for socket failed...
            print("error recieving message and/or client disconnected")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)

            broadcast("MSG", f"{nickname} left the chat")
            break





#This is for clients connecting the server
def receive():
    while True:
        #client = the client's socket
        client, address = server.accept() #wait until a new client connects to the server
        print(f"Connected with {str(address)}")

        client_send(client, "NICK")
        nickname = client.recv(1024).decode("ascii") #recieves the nickname after the request
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of client {nickname}")

        broadcast("MSG", f"{nickname} joined the chat")
        client_send(client, "MSG", "connected to the server")

        #creates a thread for listening to the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
