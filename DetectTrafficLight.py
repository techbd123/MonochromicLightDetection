import cv2
import numpy as np

cap=cv2.VideoCapture(0)

while(cap.isOpened()):
    _, img=cap.read()
            
    font = cv2.FONT_HERSHEY_SIMPLEX
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #defining the range of color
    #lower_red1 = np.array([0,100,100],np.uint8)
    #upper_red1 = np.array([10,255,255],np.uint8)

    lower_red = np.array([160,100,100])
    upper_red = np.array([180,255,255])

    lower_green = np.array([40,50,50])
    upper_green = np.array([90,255,255])
    # lower_yellow = np.array([15,100,100])
    # upper_yellow = np.array([35,255,255])
    lower_yellow = np.array([15,150,150])
    upper_yellow = np.array([35,255,255])

    #finding the range of red,green and yellow in the image
    red=cv2.inRange(img, lower_red, upper_red)
    green=cv2.inRange(img, lower_green, upper_green)
    yellow=cv2.inRange(img, lower_yellow, upper_yellow)

    maskr = cv2.inRange(hsv, lower_red, upper_red)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)

    size = img.shape
    # print size

    # hough circle detect
    r_circles = cv2.HoughCircles(maskr,cv2.HOUGH_GRADIENT, 1, 80,param1=50, param2=15, minRadius=10, maxRadius=30)

    g_circles = cv2.HoughCircles(maskg,cv2.HOUGH_GRADIENT, 1, 80,param1=50, param2=15, minRadius=10, maxRadius=30)

    y_circles = cv2.HoughCircles(masky,cv2.HOUGH_GRADIENT, 1, 80,param1=50, param2=15, minRadius=10, maxRadius=30)
    #traffic light detect
    r = 5
    bound = 4.0 / 10
    if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))

        #print r_circles

        for i in r_circles[0, :]:
          
            if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += maskr[i[1]+m, i[0]+n]
                    s += 1
            if h / s > 50:
                cv2.circle(img, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv2.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv2.putText(img,'RED SIGNAL',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

    elif g_circles is not None:
          g_circles = np.uint16(np.around(g_circles))

          for i in g_circles[0, :]:
              if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                  continue

              h, s = 0.0, 0.0
              for m in range(-r, r):
                  for n in range(-r, r):
                    
                      if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                          continue
                      h += maskg[i[1]+m, i[0]+n]
                      s += 1
              if h / s > 100:
                   cv2.circle(img, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                   cv2.circle(maskg, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                   cv2.putText(img,'GREEN SIGNAL',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

    else:
        if y_circles is not None:
           y_circles = np.uint16(np.around(y_circles))

           for i in y_circles[0, :]:
               if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                   continue

               h, s = 0.0, 0.0
               for m in range(-r, r):
                   for n in range(-r, r):

                       if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                           continue
                       h += masky[i[1]+m, i[0]+n]
                       s += 1
               if h / s > 50:
                    cv2.circle(img, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                    cv2.circle(masky, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                    cv2.putText(img,'YELLOW SIGNAL',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

    cv2.imshow("color tracking",img)

    #cv2.imshow("maskred",maskr)
    #cv2.imshow("maskgreen",maskg)
    #cv2.imshow("maskyellow",masky)

    #Pressing 'q' key will terminate the program.
    if cv2.waitKey(10)%256==ord("q"):
           break

cap.release()
cv2.destroyAllWindows()