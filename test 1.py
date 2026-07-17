def setup():
    username = input(str("Enter a Username: "))
    return username

name = setup()

def send_message(name):
    message = input(str(f"Enter a message, {name} : "))
    return message

while True:
    print(send_message(name))
