import cv2 as cv
import numpy as np
import imutils

def rescaleFrame(frame,scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0]* scale)

    dimensions = (width,height)

    return cv.resize(frame,dimensions, interpolation = cv.INTER_AREA)


capture = cv.VideoCapture('photos/celine.MOV')

lower_white = np.array([140,126,100])
upper_white = np.array([238,164,142])

while True:
    isTrue, frame = capture.read()
    frame_resized = rescaleFrame(frame, 0.5)

    hsv = cv.cvtColor(frame_resized, cv.COLOR_BGR2HSV)

    mask = cv.cvtColor(cv.inRange(hsv, lower_white, upper_white), cv.COLOR_GRAY2BGR)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    
    contours = cv.findContours(cv.cvtColor(mask, cv.COLOR_BGR2GRAY), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for c in contours:
        # Calculate the area of the contour
        area = cv.contourArea(c)
        
        # Ignore small contours
        if area > 500:
            # Get the bounding box of the contoura
            (x, y, w, h) = cv.boundingRect(c)
            
            # Draw a rectangle around the contour
            cv.rectangle(mask, (x, y), (x+w, y+h), (0, 255, 0), 2)



    cv.imshow('Celine_shirt', mask)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()
