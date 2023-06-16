#code guide provided by https://realpython.com/python-sockets/
import socket
import time

# initial conditions of ip and port. We are using port 1025 because 1-1024 needs admin approval.
IP_ADDRESS = "169.254.80.57"
PORT = 1025

# create a socket object and connect to it
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

while True:
    time.sleep(.5)
    
    # send data to the server
    #print("input data here: ")
    data = "M122\r\n"
    client_socket.sendall(data.encode())

    # echo the data
    received_data = client_socket.recv(1024).decode()
    print("Received data: ", received_data)

    if data == "break":
        break

# this is not needed, but its there to close the connection if I break
client_socket.close()
