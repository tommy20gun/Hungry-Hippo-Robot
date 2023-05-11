import socket

# Set the IP address and port of the Raspberry Pi server
IP_ADDRESS = "169.254.80.57"
PORT = 1025

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

# Send data to the server
data = "Hello, Raspberry Pi!"
client_socket.sendall(data.encode())

# Receive data from the server
received_data = client_socket.recv(1024).decode()
print("Received data: ", received_data)

# Close the connection
client_socket.close()
