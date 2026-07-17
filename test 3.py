messages_array = []
username = input(str("Please enter a username: "))
unread_array = []

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
    
def send_message(username): #Adds a message to the messages array
    message = input(str(f"Please enter your message, {username} "))
    messages_array.append(message)
    unread_array.append(message)

def print_previous_messages(messages_array): #Prints all the messages in messages_array
    number_of_all_messages = len(messages_array)
    print(f"There are {number_of_all_messages} previous messages")
    for message in messages_array:
        print(message)

while True:
    option = input(str(f"Hello, {username}. Do you want to: See messages (1), send a message (2), check for a new message (3) or exit (4)? "))
    if option == "1":
        print_previous_messages(messages_array)
    elif option == "2":
        send_message(username)
    elif option == "3":
        unread_array = check_unread_messages(unread_array)
    elif option == "4":
        break

