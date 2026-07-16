import socket
import threading

# Server configuration
HOST = '127.0.0.1'  
PORT = 5000       

# Store connected clients
clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    """Send message to all clients except the sender."""
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.sendall(message)
                except (BrokenPipeError, ConnectionResetError):
                    # Remove disconnected clients
                    clients.remove(client)

def handle_client(client_socket, address):
    """Handle messages from a single client."""
    print(f"[+] New connection from {address}")
    with clients_lock:
        clients.append(client_socket)

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # Client disconnected
            print(f"[{address}] {data.decode(errors='ignore')}")
            broadcast(data, client_socket)

    except ConnectionResetError:
        pass
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()
        print(f"[-] Connection closed from {address}")

def start_server():
    """Start the TCP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[*] Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, address), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
