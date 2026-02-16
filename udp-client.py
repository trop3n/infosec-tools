import socket

# define the target host and port
target_host = "127.0.0.1"  # Localhost (own machine)
target_port = 80  # port number

# create a socket object
# AF_INET specifies IPv4 addressing, and SOCK_DGRAM specifies UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data to the server
# the sendTo() method sends the message "AAABBBCCC" to the specified (host, port)
client.sendto(b"AAABBBCCC", (target_host, target_port))

# receive data from the server
# the recvfrom() method reads up to 4096 bytes of data and also returns the sender's address
data, addr = client.recvfrom(4096)

# close the socket
client.close()

# print the received data
print(data)
