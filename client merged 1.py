import socket

HOST = "192.168.26.16"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def send_message(username): #Adds a message to the messages array
    #message = input(str(f"Please enter your message, {username} "))

    #the user enters a message and will be sent to the host

    #these two methods should happen on the host computer once the
    #message is recieved. the methods are on the host computer
    #messages_array.append(message)
    #unread_array.append(message)


while True:
    option = input(str(f"Hello, {username}. Do you want to: See messages (1), send a message (2), check for a new message (3) or exit (4)? "))
    if option == "1":
        #sends a request for this to happen on the host computer, and will return an output to the client
        #print_previous_messages(messages_array)
    elif option == "2":
        #happens locally
        #send_message(username)
    elif option == "3":
        #sends a request for this to happen on the host computer, and will return an output to the client
        #unread_array = check_unread_messages(unread_array)
    elif option == "4":
        break





with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello Matthew and Aarvin")
    data = s.recv(1024)

print(f"Received {data!r}")
