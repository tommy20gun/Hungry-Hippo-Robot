import cv2 as cv
import numpy as np
from ball_detection import rescale_frame, detect_and_draw_balls
#from cart_detection import cart_detection
from run_qr import plot_axes_on_frame
from Ball import Ball
from Cart import Cart


# Store the HSV color values in another file to minimize clogging up the main script
from hsvcolordata import lower_ranges, upper_ranges, colors



def main():
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)

    #initialize ball and cart list
    cart = None
    balls = None
    
    while True:
        #resets ball to be extended
        balls = []
        is_true, frame = capture.read()
        if is_true:
            frame = rescale_frame(frame, 1)

            # Detect and draw balls of different colors
            for color in colors:
                frame,ball_x, ball_y = detect_and_draw_balls(frame, lower_ranges[color], upper_ranges[color], colors[color])
                if ball_x is not None:
                    #adds balls to the list of balls
                    balls.append(Ball(color,ball_x,ball_y))
                    print(f"{balls.color} ball at ({balls.x},{balls.y})")

        # Plot axes and angle on the frame
        frame, cart_x, cart_y, angle = plot_axes_on_frame(frame)

        # Check if an object is detected
        if cart_x is not None and cart_y is not None and angle is not None:
            
            #assign variable values to cart[]
            cart = Cart(angle,cart_x,cart_y)

            print("QR code rotation angle:", cart.angle)
            print("QR code center: ({}, {})".format(cart.x, cart.y))


        # Display the frame
        cv.imshow('Frame', frame)
            #sendserialdata(frame_resized)

            # Exit if the 'q' key is pressed
        if cv.waitKey(20) & 0xFF == ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
