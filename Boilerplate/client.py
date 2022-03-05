import socket
import threading

nickname = input("input nickname: ")

#AF_INET = internet type socket, SOCK_STREAM = TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.40", 58352))

#This is for the client recieving packets from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii") #recieving from the server
            #if the msgid is "NICK"
            if message == "NICK":
                client.send(nickname.encode("ascii")) #send your nickname back to the server
            else:
                print(message) #otherwise print the message

        except:
            print("Error with recieving message")
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("ascii"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()