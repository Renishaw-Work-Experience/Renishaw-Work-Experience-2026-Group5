import socket
messages_array = []
unread_array = []

def see_messages(messages_array): #Prints all the messages in messages_array
    number_of_all_messages = len(messages_array)
    print(f"There are {number_of_all_messages} previous messages")
    for message in messages_array:
        print(message)

def check_unread_messages(unread_array):
    if len(unread_array)>0:
        amount_of_messages = len(unread_array)
        print(f"There are {amount_of_messages} unread messages")
        for message in unread_array:
            print(message)
            unread_array.clear()
    else:
        print("There are no unread messages")

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            if data.decode("utf-8")[0] == "%":
                message = data.decode("utf-8")[1:]
                messages_array.append(message)
                unread_array.append(message)
            elif data.decode("utf-8") == "seemessages":
                see_messages(messages_array)
            elif data.decode("utf-8") == "checkforanewmessage":
                check_unread_messages(unread_array)
