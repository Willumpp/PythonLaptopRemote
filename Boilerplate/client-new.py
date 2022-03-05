import socket
import threading
import pickle #This is used for encoding data sctructures and sending them accross network


nickname = input("input nickname: ")

#AF_INET = internet type socket, SOCK_STREAM = TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.40", 58352))



def idNick(client, *args):
    client.send(nickname.encode("ascii"))

def idMSG(client, *args):
    message = args[0] #Message
    print(message)


client_funcs = {
    "NICK": idNick,
    "MSG": idMSG
}


def client_send(client, msgid, *args):
    message = pickle.dumps((msgid, args))

    client.send(message)


#This is for the client recieving packets from the server
def receive():
    while True:
        try:
            msgid, args = pickle.loads(client.recv(1024)) #recieving bytes from the server
            client_funcs[msgid](client, *args)

        except:
            print("Error with recieving message")
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client_send(client, "MSG", message)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()