import socket
messages_array = []
username = input(str("Please enter a username: "))
unread_array = []
HOST = "213.120.89.10"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on 



def recieve_message()
    #code goes here

def check_unread_messages(unread_array):
    if len(unread_array)>0:
        amount_of_messages = len(unread_array)
        print(f"There are {amount_of_messages} unread messages")
        for message in unread_array:
            print(message)
        unread_array.clear()
        return unread_array
    else:
        print("There are no new messages")
        return unread_array

def print_previous_messages(messages_array): #Prints all the messages in messages_array
    number_of_all_messages = len(messages_array)
    print(f"There are {number_of_all_messages} previous messages")
    for message in messages_array:
        print(message)


#while true
    #recieve messages
        
    #message could include a request to check_unread_message() etc.
    #depending on the information recieved, a subroutine will be called
    #e.g. if the recieved message is to check unread messages then the check unread messages subroutine will be called
        
with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
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


