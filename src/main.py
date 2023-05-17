import cv2 as cv
import numpy as np
from ball_detection import rescale_frame, detect_and_draw_balls
from cart_detection import cart_detection


# Store the HSV color values in another file to minimize clogging up the main script
from hsvcolordata import lower_ranges, upper_ranges, colors



def main():
    capture = cv.VideoCapture(0, cv.CAP_DSHOW)
    
    while True:
        is_true, frame = capture.read()
        if is_true:
            frame_resized = rescale_frame(frame, 1)

            # Detect and draw balls of different colors
            for color in colors:
                frame_resized = detect_and_draw_balls(frame_resized, lower_ranges[color], upper_ranges[color], colors[color])

            # Perform cart detection and label rotation angle
            frame_resized = cart_detection(frame_resized)

            # Show the modified frame
            cv.imshow("Frame", frame_resized)

            # Exit if the 'q' key is pressed
            if cv.waitKey(20) & 0xFF == ord('d'):
                break

    capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
