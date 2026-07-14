messages_array = []
username = input(str("Please enter a username: "))
unread_array = []

class message:
  def __init__(msg, text, author):
    msg.text = text
    msg.author = author


def check_unread_messages(unread_array):
    if len(unread_array)>0:
        amount_of_messages = len(unread_array)
        print(f"There are {amount_of_messages} unread messages")
        for index, message in enumerate(unread_array, start=1):
            print(f"{index}: {message}")
        unread_array.clear()
        return unread_array
    else:
        print("There are no new messages")
        return unread_array
    
def send_message(username): #Adds a message to the messages array
    message1 = message(input(str(f"Please enter your message, {username} ")), username)
    messages_array.append(message1)
    unread_array.append(message1)

def print_previous_messages(messages_array, unread_messages): #Prints all the messages in messages_array
    number_of_all_messages = len(messages_array)
    print(f"There are {number_of_all_messages} previous messages")
    for index, message in enumerate(messages_array, start=1):
        print(f"{index}: {message.text}")
        unread_array.clear()
                            
def print_user_messages(messages_array, username):
    for message in messages_array:
        if message.author == username
            print(message.text)
    
while True:
    option = input(str(f"Hello, {username}. Do you want to: See messages (1), send a message (2), check for a new message (3) or exit (4)? "))
    if option == "1":
        print_previous_messages(messages_array, unread_array)
        while True:
            option2 = input(str(f"Hello, {username}, do you want to delete any messages (1), display main panel (2) or print messages by user (3) "))
            if option2 == "1":
               deleted_message = int(input(f"Please enter the message you wish to delete, {username} "))
               messages_array.pop((deleted_message)-1)
            elif option2 == "2":
                break
            elif option2 == "3":
                print_user_messages(messages_array, username)
    elif option == "2":
        send_message(username)
    elif option == "3":
        unread_array = check_unread_messages(unread_array)
    elif option == "4":
        break
exit()
