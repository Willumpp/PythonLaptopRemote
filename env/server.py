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

def broadcast_raw(message, exclient=""):
    for client in clients:
        if client != exclient:
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
            broadcast_raw(message, exclient=client)
        except:
            #listening for socket failed...
            print("error recieving message and/or client disconnected")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break





#This is for clients connecting the server
def receive():
    while True:
        #client = the client's socket
        client, address = server.accept() #wait until a new client connects to the server
        print(f"Connected with {str(address)}")
        clients.append(client)

        client_send(client, "MSG", "connected to the server")

        #creates a thread for listening to the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
