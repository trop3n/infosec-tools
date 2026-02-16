import socket
import threading

# bind IP and port
bind_ip = "0.0.0.0"  # listen on all available interfaces
bind_port = 9999  # port to listen on

# create TCP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the server to the IP and port
server.bind((bind_ip, bind_port))

# start listening with a backlog of 5 connections
server.listen(5)

print(f"[*] Listening on {bind_ip}:{bind_port}")

# client handling thread


def handle_client(client_socket):
    """Handles communication with the connected client."""
    request = client_socket.recv(1024)  # receive data from the client

    print(f"[*] Received: {request.decode('utf-8')}")

    # send back an acknowledgement
    client_socket.send(b"ACK!")

    print(f"[*] Sent ACK to {client_socket.getpeername()}")

    client_socket.close()


# main loop to accept incoming connections
while True:
    client, addr = server.accept()
    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

    # spin up a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
