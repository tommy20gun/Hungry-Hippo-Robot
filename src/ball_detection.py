import cv2 as cv
import numpy as np
import imutils


def rescale_frame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def detect_and_draw_balls(frame, lower_range, upper_range, color):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Detect balls
    mask = cv.inRange(hsv, lower_range, upper_range)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Draw rectangles around balls
    for c in contours:
        # Calculate the area and circularity of the contour
        area = cv.contourArea(c)
        perimeter = cv.arcLength(c, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        # Ignore small or non-circular contours
        if area > 500 and circularity > 0.8:
            # Get the bounding box of the contour
            (x, y, w, h) = cv.boundingRect(c)

            # Calculate the center of the ball
            center_x = x + w // 2
            center_y = y + h // 2

            # Draw a rectangle around the contour
            cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            # Display the coordinates of the center
            text = f"({center_x}, {center_y})"
            cv.putText(frame, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame
