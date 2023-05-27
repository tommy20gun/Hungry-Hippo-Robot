#code guide provided by https://realpython.com/python-sockets/
#double while-loop inspired by chatGPT. I got stuck on looping the signal sent into the server to have it continuously send data.
import socket
import serial
import time

# initial conditions
# IP_ADDRESS = "192.168.147.134"
PORT = 1025

# serial port configurations
port = "/dev/ttyS0"
baud_rate = 115200
parity = 'N'
stop_bits = 1

ser = serial.Serial(port, baudrate=baud_rate, parity=parity, stopbits=stop_bits)

data = "M155\r\n"

# create a socket object, bind a port to the socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))
server_socket.listen()

while True:
    client_socket, client_address = server_socket.accept()
    
    while True:
        received_data = client_socket.recv(1024).decode()
        
        #if no data received, code will close the socket and reaccept
        if not received_data:
            break
        
        print("Received data:", received_data)

        # allow the raspberrypi to echo response back to the client
        response = f"Hello from the Raspberry Pi! msg: {received_data}"
        client_socket.sendall(response.encode())

        # serial write data to the MCU
        ser.write(received_data.encode())
        print("Sent data:", received_data)

    client_socket.close()
