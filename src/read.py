import cv2 as cv
import numpy as np


# img = cv.imread('photos/wtf.jpg')
# cv.imshow('oatmeal',img)



# cv.waitKey(0)

def rescaleFrame(frame,scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0]* scale)

    dimensions = (width,height)

    return cv.resize(frame,dimensions, interpolation = cv.INTER_AREA)

def changeRes(width,height):
    # only works for videos
    capture.set(3,width)
    capture.set(3,height)



capture = cv.VideoCapture('photos/celine.MOV')

while True:
    isTrue, frame = capture.read()
    frame_resized = rescaleFrame(frame, 0.2)
    gray = cv.cvtColor(frame_resized, cv.COLOR_BGR2GRAY)
    lap = cv.Laplacian(gray,cv.CV_64F)
    lap = np.uint8(np.absolute(lap))
    cv.imshow('celine',lap)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()
