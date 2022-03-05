import socket
import threading

nickname = input("input nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.0.40", 58352))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii") #recieving from the server
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)

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