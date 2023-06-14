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
from CameraBufferCleaner import CameraBufferCleanerThread

# Store the HSV color values in another file to minimize clogging up the main script
from hsvcolordata import lower_ranges, upper_ranges, colors



def main():
    #capture = cv.imread('Screenshot.png')
    capture = cv.VideoCapture(1, cv.CAP_DSHOW)#'rtsp://192.168.84.58:8080/h264.sdp') #, cv.CAP_DSHOW)#2, cv.CAP_DSHOW)
    cam_cleaner = CameraBufferCleanerThread(capture)
    rescalefactor = .7

    #initialize ball and cart list
    cart = None
    balls = None
    corralstation = None

    #initializes Socket object to send serial data
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #IP_ADDRESS = "169.254.80.57"
    IP_ADDRESS = "192.168.84.134"
    PORT = 1025
    s.connect((IP_ADDRESS, PORT))

    #initialize PID object
    pid = PID(.2,3,.01, setpoint= 0)

    #initialize framedetection counter
    cartframedetectioncounter = 0
    ballframedetectioncounter = 0
    desiredframes = 2
    previousdata = ""

    pause = False
   

    while True:
        #read the frames of the video as a while loop to make it "look" like a video

        #thereisaframe, frame = capture.read()

        #thereisaframe = True
        #if thereisaframe and not pause:
        if cam_cleaner.last_frame is not None:
            #frame = cv.imread('Screenshot.png')
            #frame = rescale_frame(frame, rescalefactor)
            frame = rescale_frame(cam_cleaner.last_frame, rescalefactor)
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
                cartframedetectioncounter +=1
                if cartframedetectioncounter >= desiredframes:
                    #assign variable values to cart
                    cart = Cart(angle,cart_x,cart_y)
                    #print(cart.x,cart.y)
            else:
                cartframedetectioncounter = 0
                #print("QR code rotation angle:", cart.angle)
                #print("QR code center: ({}, {})".format(cart.x, cart.y))

            #chekcs if there are no balls for a long time, at 20 frames of no balls, the program exits
            if balls == []:
                ballframedetectioncounter += 1
                if ballframedetectioncounter >= 20:
                    #print("no more balls")
                    #corralstation = Ball("yellow", 500, 500)
                    pass

            else: 
                ballframedetectioncounter = 0

            # Display the frame
            cv.imshow('Frame', frame)

            #send the data through serial to the MCU and echo it in terminal
            
            """if corralstation is not None:
                data = getdutycycledata(corralstation, cart, pid)
                #if the cart is close to the corral station
                if (cart.x - corralstation.x) <= 30 and (cart.y - corralstation.y) <= 30:
                    #s.sendall("state3".encode())
                    #received_data = s.recv(1024)
                    #print(received_data)
                    print("State3")
            else:"""

            data = getdutycycledata(balls, cart, pid)

            if data:
                #this fixes the random noise of rotation
                if not (data[8:10] == "D0" and previousdata[8:10] != "D0"):    
                    s.sendall(data.encode())
                    received_data = s.recv(1024)
                    print(received_data)
                    #print(data)
                previousdata= data

        key = cv.waitKey(20)
        #state 3 with d
        if key == ord('d'):
            s.sendall("state3".encode())
            received_data = s.recv(1024)
            print(received_data)

        #emergency kill button with space bar
        elif key == ord(' '):
            pause = not pause
            s.sendall("pause".encode())
            received_data = s.recv(1024)
            print(received_data)
        # Exit if the 'q' key is pressed
        elif key == ord('q'):
            break
            

    capture.release()
    cv.destroyAllWindows()
    #s.close()


if __name__ == '__main__':
    main()
