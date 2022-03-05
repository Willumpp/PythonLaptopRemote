import threading
import socket

host = "192.168.0.40"
port = 58352

#AF_INET = internet type socket, SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            print("error recieving message and/or client disconnected")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat".encode("ascii"))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))

        client.send("connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()