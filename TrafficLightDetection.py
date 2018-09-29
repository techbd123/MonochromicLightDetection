import cv2
import numpy as np


mainImage = None

font = cv2.FONT_HERSHEY_SIMPLEX

colors = {"red":(0,0,255), "green":(0,255,0), "yellow":(0, 255, 217)}

#HSV Color Space
lower = {"red":(166, 84, 141), "green":(66, 122, 129), "yellow":(23, 59, 119)} 
upper = {"red":(186,255,255), "green":(86,255,255), "yellow":(54,255,255)}

def ConvertBGR2HSV(BGR):
    color = np.uint8([[BGR]])
    [[hsv_color]] = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
    return hsv_color

def DetectFilledCircle(image,lower_color,upper_color,text,text_color):
    mask = cv2.inRange(image,lower_color,upper_color)
    kernel = np.ones((10,10),np.uint8)
    #Removing spots outside
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #Removing spots inside
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("mask",mask)
    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,200,param1=50, param2=15, minRadius=5, maxRadius=100)
    if circles is not None:
      circles=np.round(circles[0, :]).astype("int")
      for (x, y, r) in circles:
          # draw the circle in the original image
          cv2.circle(mainImage,(x,y),r,text_color,2)
          cv2.circle(mask,(x,y),r,(255,255,255),2)
          cv2.putText(mainImage,text,(x-r,y-r),font,0.5,text_color,2,cv2.LINE_AA)
    return

cap=cv2.VideoCapture(0)


while(cap.isOpened()):
    _, mainImage=cap.read()
            
    hsv = cv2.cvtColor(mainImage,cv2.COLOR_BGR2HSV)

    DetectFilledCircle(hsv,lower["red"],upper["red"],"RED SIGNAL",colors["red"])
    DetectFilledCircle(hsv,lower["green"],upper["green"],"GREEN SIGNAL",colors["green"])
    DetectFilledCircle(hsv,lower["yellow"],upper["yellow"],"YELLOW SIGNAL",colors["yellow"])

    cv2.imshow("Color Tracking",mainImage)

    #Pressing 'ESC' key will terminate the program.
    if cv2.waitKey(10)%256==27:
           break

cap.release()
cv2.destroyAllWindows()