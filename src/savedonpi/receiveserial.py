import socket
import serial
import time

# Set the IP address and port to listen on
IP_ADDRESS = "169.254.80.57"
PORT = 1025

#set up the serial port
port = "/dev/ttyS0"
baud_rate = 115200
parity = 'N'
stop_bits = 1

ser= serial.Serial(port,baudrate = baud_rate,parity = parity,stopbits = stop_bits )

data = "Hello world!"
while True:

    ser.write(data.encode())
    time.sleep(1)

ser.close()

# Create a socket object and bind it to the IP address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
server_socket.listen()

# Accept a connection and receive data
while True:
    client_socket, client_address = server_socket.accept()
    received_data = client_socket.recv(1024).decode()
    print("Received data: ", received_data)

    # Send a response back to the client
    response = "Hello from the Raspberry Pi!"
    client_socket.sendall(response.encode())

    # Close the client socket
    client_socket.close()



