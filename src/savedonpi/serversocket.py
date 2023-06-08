#code guide provided by https://realpython.com/python-sockets/
#double while-loop inspired by chatGPT. I got stuck on looping the signal sent into the server to have it continuously send data.
import socket
import serial
import time
import RPi.GPIO as GPIO

# initial conditions
# IP_ADDRESS = "192.168.147.134"
PORT = 1025

# serial port configurations
port = "/dev/ttyS0"
baud_rate = 115200
parity = 'N'
stop_bits = 1

ser = serial.Serial(port, baudrate=baud_rate, parity=parity, stopbits=stop_bits)

#Raspberry pi GPIO setup

GPIO.setmode(GPIO.BCM)
gpio_pin = 17
gpio_pin2 = 27
GPIO.setup(gpio_pin, GPIO.OUT)
GPIO.setup(gpio_pin2, GPIO.OUT)
#initially set up the gpio pin to low
GPIO.output(gpio_pin,GPIO.LOW)
GPIO.output(gpio_pin,GPIO.LOW)


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

        # serial write data to the MCU, except for pause string.
        
        if received_data == "pause":
            GPIO.output(gpio_pin, not GPIO.input(gpio_pin))
            pin_state = GPIO.input(gpio_pin)
            print(f"Toggled {gpio_pin} to: {pin_state}")
        elif received_data == "state3":
            GPIO.output(gpio_pin2, not GPIO.input(gpio_pin2))
            pin_state = GPIO.input(gpio_pin2)
            print(f"Toggled {gpio_pin2} to: {pin_state}")
        else:
            ser.write(received_data.encode())
            print("Sent data:", received_data)

    client_socket.close()
