import cv2 as cv
import numpy as np
import imutils


def rescaleFrame(frame, scale):
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

            # Draw a rectangle around the contour
            cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    return frame


capture = cv.VideoCapture("balls.mp4")

# Set the color ranges for the ping pong balls
lower_ranges = {
    "yellow": np.array([20, 100, 100]),
    "green": np.array([60, 100, 50]),
    "blue": np.array([100, 100, 50]), 
    "red1": np.array([0, 100, 50]),
    "red2": np.array([170, 100, 50])
}

upper_ranges = {
    "yellow": np.array([40, 255, 255]),
    "green": np.array([100, 255, 255]),
    "blue": np.array([130, 255, 255]),
    "red1": np.array([10, 255, 255]),
    "red2": np.array([180, 255, 255])
}

colors = {
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "red1": (0, 0, 255),
    "red2": (0, 0, 255)
}

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break
    frame_resized = rescaleFrame(frame, 0.5)

    # Detect and draw balls of different colors
    for color in colors:
        frame_resized = detect_and_draw_balls(frame_resized, lower_ranges[color], upper_ranges[color], colors[color])

    # Show the modified frame
    cv.imshow("Frame", frame_resized)

    # Exit if the 'q' key is pressed
    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()
