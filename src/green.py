import cv2 as cv
import numpy as np

deeznuts = np.zeros((500,500,3), dtype = 'uint8')

deeznuts[200:300, 200:300] = 0,255,0



cv.rectangle(deeznuts, (0,0), (250,250), (0,255,0), thickness = 2)
cv.imshow('Green', deeznuts)


cv.waitKey(0)
