import cv2 as cv
import numpy as np


def ConvertBGR2HSV(BGR):
    color=np.uint8([[BGR]])
    [[hsv_color]]=cv.cvtColor(color,cv.COLOR_BGR2HSV)
    return hsv_color

cap=cv.VideoCapture(0)

while(cap.isOpened()):
    _, img=cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cv.imshow("hsv",hsv)

    # cv.imshow("hsv",hsv)

    """
    # define range of blue color in HSV
    lower_red = ConvertBGR2HSV([0,0,128])
    print 'lower red = %s' % lower_red

    upper_red = ConvertBGR2HSV([0,0,255])
    print 'upper red = %s' % upper_red

    lower_red = np.array([160,100,100])
    upper_red = np.array([180,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv,lower_red,upper_red)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(img,img, mask= mask)
    cv.imshow('Original Image',img)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    """
    # Pressing ESC key will terminate the program.
    if cv.waitKey(10)%256==27:
      break

cap.release()
cv.destroyAllWindows()