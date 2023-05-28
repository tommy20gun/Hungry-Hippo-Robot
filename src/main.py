import cv2 as cv
import numpy as np
from ball_detection import rescale_frame, detect_and_draw_balls
#from cart_detection import cart_detection
from cart_detection import plot_axes_on_frame
from Ball import Ball
from Cart import Cart
from PIDcalculator import getdutycycledata
import socket
from simple_pid import PID
import time


# Store the HSV color values in another file to minimize clogging up the main script
from hsvcolordata import lower_ranges, upper_ranges, colors



def main():
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    rescalefactor = 1

    #initialize ball and cart list
    cart = None
    balls = None

    #initializes Socket object to send serial data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP_ADDRESS = "169.254.80.57"
    PORT = 1025
    s.connect((IP_ADDRESS, PORT)) 

    #initialize PID object
    pid = PID(.5,.1,.01, setpoint= 1)

    #initialize framedetection counter
    framedetectioncounter = 0
    desiredframes = 2

    while True:
        #read the frames of the video as a while loop to make it "look" like a video
        thereisaframe, frame = capture.read()
        if thereisaframe:

            frame = rescale_frame(frame, rescalefactor)

            #resets ball and cart
            balls = []
            cart = None

            # Detect and draw balls of different colors
            for color in colors:
                frame,ball_x, ball_y = detect_and_draw_balls(frame, lower_ranges[color], upper_ranges[color], colors[color])
                if ball_x is not None:
                    #adds balls to the list of balls
                    balls.append(Ball(color,ball_x,ball_y))
                    #print(balls)

            # Plot axes and angle on the frame
            frame, cart_x, cart_y, angle = plot_axes_on_frame(frame)

            # Check if an object is detected
            if cart_x is not None and cart_y is not None and angle is not None:
                framedetectioncounter +=1
                if framedetectioncounter >= desiredframes:
                    #assign variable values to cart
                    cart = Cart(angle,cart_x,cart_y)
                    print(cart.x,cart.y)
            else:
                framedetectioncounter = 0
                #print("QR code rotation angle:", cart.angle)
                #print("QR code center: ({}, {})".format(cart.x, cart.y))


            # Display the frame
            cv.imshow('Frame', frame)

            #send the data through serial to the MCU and echo it in terminal
            data = getdutycycledata(balls, cart, pid)
            if data:    
                s.sendall(data.encode())
                received_data = s.recv(1024)
                print(received_data)

        # Exit if the 'q' key is pressed
        if cv.waitKey(20) & 0xFF == ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()
    #s.close()


if __name__ == '__main__':
    main()
