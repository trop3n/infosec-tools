import socket
import sys
import threading


def hexdump(src, length=16):
    """Hex dump
    This function produces a classic 3-column hex dump of a string.
    The first column prints the offset in hexadecimal.
    The second column prints the hexadecimal byte values.
    The third column prints ASCII values or a dot (.) for non-printable characters.
    """
    result = []
    digits = 4  # offset width

    if isinstance(src, bytes):  # ensure we handle bytes properly
        for i in range(0, len(src), length):
            s = src[i : i + length]
            hexa = " ".join(f"{x:02X}" for x in s)  # hex representation
            text = "".join(
                chr(x) if 0x20 <= x < 0x7F else "." for x in s
            )  # ASCII values
            result.append(f"{i:04X} {hexa:<{length * 3}} {text}")

    print("\n".join(result))


def receive_from(connection):
    """Receive data from the socket.
    Reads data until no more is available or a timeout occurs.
    """
    buffer = b""
    connection.settimeout(2)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except socket.timeout:
        pass

    return buffer


def request_handler(buffer):
    """Modify requests before sending them to the remote host (if needed)."""
    return buffer


def response_handler(buffer):
    """Modify responses before sending them back to the client (if needed)."""
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """Handles communication between the client and the remote host."""

    # create a connection to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # if we need to receive data first from the remote host
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print("[<==] Received from remote:")
            hexdump(remote_buffer)

        # send data to response handler
        remote_buffer = response_handler(remote_buffer)

        # forward modified response to local client
        client_socket.send(remote_buffer)

    while True:
        # receive data from local client
        local_buffer = receive_from(client_socket)
        if local_buffer:
            print(f"[==>] Received {len(local_buffer)} bytes from local host")
            hexdump(local_buffer)

            # modify the request if needed
            local_buffer = request_handler(local_buffer)

            # forward the request to the remote server
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote")

        # receive resposne from the remote server
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            print(f"[<==] Received {len(remote_buffer)} bytes from remote")
            hexdump(remote_buffer)

            # modify the request if needed
            remote_buffer = response_handler(remote_buffer)

            # forward the response to the local client
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost")

        # close connections when no more data is received
        if not local_buffer or not remote_buffer:
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    """Creates a listening server that forwards traffic to a remote server"""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except socket.error as e:
        print(f"[-] Failed to bind to {local_host}:{local_port}")
        print("[-] Ensure no other processes are using the port.")
        print(f"Error: {e}")
        sys.exit(1)

    print(f"[*] Listening on {local_host}:{local_port}")

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print(f"[==>] Incoming connection from {addr[0]}:{addr[1]}")

        # create a new thread to handle the connection
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first),
        )
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first),
        )
        proxy_thread.start()


def main():
    """Main function to parse arguments and start the proxy server."""

    if len(sys.argv[1:]) != 5:
        print(
            "Usage: ./tcp-proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        )
        print("Example: ./tcp-proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(1)

    # assign command-line arguments
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # convert string "True" or "False" to boolean
    receive_first = sys.argv[5].lower() == "true"

    # start the server loop
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()
