import socket
import serial
import time

# Set the IP address and port to listen on
# IP_ADDRESS = "192.168.147.134"
PORT = 1025

# Set up the serial port
port = "/dev/ttyS0"
baud_rate = 115200
parity = 'N'
stop_bits = 1

ser = serial.Serial(port, baudrate=baud_rate, parity=parity, stopbits=stop_bits)

data = "M155\r\n"

# Create a socket object and bind it to the IP address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))

# Listen for incoming connections
server_socket.listen()

# Accept a connection and receive data
while True:
    client_socket, client_address = server_socket.accept()
    
    while True:
        received_data = client_socket.recv(1024).decode()
        
        if not received_data:
            # No more data received, break the inner loop
            break
        
        print("Received data:", received_data)

        # Send a response back to the client
        response = f"Hello from the Raspberry Pi! msg: {received_data}"
        client_socket.sendall(response.encode())

        # Serial write data to the MCU
        ser.write(received_data.encode())
        print("Sent data:", received_data)

    client_socket.close()
