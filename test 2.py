messages_array = []
messages_array.append("hello")
last_message = messages_array[(len(messages_array)-1)]
username = input(str("Please enter a username: "))


def check_unread_message(last_message):
    if last_message == messages_array[(len(messages_array)-1)]:
        print("There is no unread message")
    else:
        the_actual_last_message = messages_array[(len(messages_array)-1)]
        print(f"There is a unread message, {the_actual_last_message}")
        return the_actual_last_message
        

    
def send_message(username): #Adds a message to the messages array
    message = input(str(f"Please enter your message, {username} "))
    messages_array.append(message)

def print_all_messages(): #Prints all the messages in the array
    for message in messages_array:
        print(message)
    

while True:
    option = input(str(f"Hello, {username}. Do you want to: See messages (1), send a message (2), check for a new message (3) or exit (4)? "))
    if option == "1":
        print_all_messages()
    elif option == "2":
        send_message(username)
    elif option == "3":
        last_message = check_unread_message(last_message)
    elif option == "4":
        break

#user sends message
#message gets added to the messages array
#the most recent message is broadcast to all devices
#

