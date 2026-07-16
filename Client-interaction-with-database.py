import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

username = input(str("Please enter a username: "))

def send_message(username): #Adds a message to the messages array
    message = input(str(f"Please enter your message, {username} "))
    identifier = "%"
    message = identifier + message
    #messages_array.append(message)
    #unread_array.append(message)
    bytes_message = message.encode("utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes_message)
        data = s.recv(1024)
        print(f"Received {data!r}")


def send_function(option):
    if option == 1:
        function = "seemessages"
        bytes_function = function.encode("utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes_function)
            data = s.recv(1024)
            print(f"Received {data!r}")
    elif option == 2:
        function = "checkforanewmessage"
        bytes_function = function.encode("utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes_function)
            data = s.recv(1024)
            print(f"Received {data!r}")

while True:
    option = int(input(f"Hello, {username}. Do you want to: See messages (1), check for a new message (2), exit (3) or send a new message (4)? "))
    if (option > 0) and (option < 3):
        send_function(option)
    elif option == 3:
        print("Goodbye")
        break
    elif option == 4:
        send_message(username)
    
exit()
