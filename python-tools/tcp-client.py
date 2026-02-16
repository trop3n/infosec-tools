import socket  # import socket module to enable network communication

# define target server and port
target_host = "127.0.0.1"  # IP address or website to connect to
target_port = 80  # HTTP port for web traffic

# create a socket object using:
# AF_INET -> IPv4
# SOCK_STREAM -> TCP (Transmission Control Protocol)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client to the target server and port
client.connect((target_host, target_port))

# send an HTTP GET request to fetch the homepage
client.send(b"GET /HTTP/1.1\r\nHost: " + target_host.encode() + b"\r\n\r\n")

# receive and print the response from the server
response = client.recv(4096)
print(response.decode)
