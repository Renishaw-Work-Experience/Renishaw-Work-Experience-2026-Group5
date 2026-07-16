import socket

messages_array = []
unread_array = []

def see_messages(messages_array): #Prints all the messages in messages_array
    number_of_all_messages = len(messages_array)
    print(f"There are {number_of_all_messages} previous messages")
    for message in messages_array:
        print(message)

def check_unread_messages(unread_array):
    if len(unread_array) > 0:
        amount_of_messages = len(unread_array)
        print(f"There are {amount_of_messages} unread messages")

        for message in unread_array:
            print(message)

        unread_array.clear()

    else:
        print("There are no unread messages")

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:

        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")

            data = conn.recv(1024)

            if not data:
                continue

            decoded_data = data.decode("utf-8")

            conn.sendall(data)

            if decoded_data.startswith("%"):
                message = decoded_data[1:]
                messages_array.append(message)
                unread_array.append(message)

            elif decoded_data == "seemessages":
                see_messages(messages_array)

            elif decoded_data == "checkforanewmessage":
                check_unread_messages(unread_array)