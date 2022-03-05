
def send_message(sock, message, HEADERSIZE):
    msg = message

    #this is for sending the length of the string in the packet
    #   for padding the message with a gap
    msg = f"{len(msg):<{HEADERSIZE}}" + msg 
    
    sock.send(bytes(msg, "utf-8")) #send to the socket