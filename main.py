import cv2 as cv
import numpy as np
from collections import deque

frameWidth = 640
frameHeight = 480

def test(val):
    pass

#create trackbars
trackbar = "HSV FILTER"
cv.namedWindow(trackbar, cv.WINDOW_NORMAL)
cv.resizeWindow(trackbar,640,240)
cv.createTrackbar("Hue Min", trackbar, 0, 179, test)
cv.createTrackbar("Hue Max", trackbar, 20, 179, test)
cv.createTrackbar("Sat Min", trackbar, 20, 255, test)
cv.createTrackbar("Sat Max", trackbar, 255, 255, test)
cv.createTrackbar("val Min", trackbar, 70, 255, test)
cv.createTrackbar("val Max", trackbar, 255, 255, test)

#initialize video capturing
vid = cv.VideoCapture(0)
vid.set(3,frameWidth)
vid.set(4,frameHeight)
kernel = np.ones((5,5), np.uint8)

#point deques for different colors
bpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = 0
red_index = 0
green_index = 0
yellow_index = 0

#color index and colors
colors = [(255,255,0),(0,255,0),(0,0,255),(0,255,255)]
colorIndex = 0

#white canvas
paintWindow = np.zeros((480,640,3))+255
paintWindow = cv.rectangle(paintWindow,(40,1),(140,65),(0,0,0),2)
paintWindow = cv.rectangle(paintWindow,(165,1),(255,65),colors[0],-1)
paintWindow = cv.rectangle(paintWindow,(275,1),(370,65),colors[1],-1)
paintWindow = cv.rectangle(paintWindow,(390,1),(465,65),colors[2],-1)
paintWindow = cv.rectangle(paintWindow,(505,1),(600,65),colors[3],-1)

cv.putText(paintWindow, "CLEAR", (62,33), cv.FONT_HERSHEY_DUPLEX, 0.5, (0,0,0), 2, cv.LINE_AA)
cv.putText(paintWindow, "BLUE", (185,33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
cv.putText(paintWindow, "GREEN", (298,33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
cv.putText(paintWindow, "RED", (420,33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
cv.putText(paintWindow, "YELLOW", (520,33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
cv.namedWindow("AIR DOODLE")
cv.resizeWindow("AIR DOODLE", frameWidth, frameHeight)

while True:
    ret,frame = vid.read() #ret is a boolean indicating if the frame was successfully captured
    if not ret:
        break

    frame = cv.flip(frame,1) #1 is horizontal flip
    hsvImg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    frame = cv.rectangle(frame, (40,1),(140,65),(0,0,0),2)
    frame = cv.rectangle(frame, (160, 1), (255, 65), colors[0], 2)
    frame = cv.rectangle(frame, (275, 1), (370, 65), colors[1], 2)
    frame = cv.rectangle(frame, (390, 1), (485, 65), colors[2], 2)
    frame = cv.rectangle(frame, (505, 1), (600, 65), colors[3], 2)
    cv.putText(frame, "CLEAR", (62,33), cv.FONT_HERSHEY_DUPLEX, 0.5, (0,0,0), 2, cv.LINE_AA)
    cv.putText(frame, "BLUE", (185, 33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
    cv.putText(frame, "GREEN", (298, 33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
    cv.putText(frame, "RED", (420, 33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)
    cv.putText(frame, "YELLOW", (520, 33), cv.FONT_ITALIC, 0.5, (0,0,0), 2, cv.LINE_AA)

    h_min = cv.getTrackbarPos("Hue Min", trackbar)
    h_max = cv.getTrackbarPos("Hue Max", trackbar)
    s_min = cv.getTrackbarPos("Sat Min", trackbar)
    s_max = cv.getTrackbarPos("Sat Max", trackbar)
    v_min = cv.getTrackbarPos("val Min", trackbar)
    v_max = cv.getTrackbarPos("val Max", trackbar)

    lower_hsv = np.array([h_min,s_min,v_min])
    upper_hsv = np.array([h_max,s_max,v_max])
    mask = cv.inRange(hsvImg, lower_hsv, upper_hsv)
    mask = cv.GaussianBlur(mask, (5, 5), 0)
    mask = cv.medianBlur(mask, 5)
    mask = cv.erode(mask, kernel, iterations=1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.dilate(mask, kernel, iterations=1)

    #findcontourpointer
    cnts,_ = cv.findContours(mask.copy(),cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    center = None
    #if contour formed
    if len(cnts)>0:
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)[0]
        #largestcontour = max(cnts,key=cv.contourArea())
        if cv.contourArea(cnts)>500:
           ((x,y),radius) = cv.minEnclosingCircle(cnts)
           cv.circle(frame, (int(x),int(y)), int(radius), (0,255,255), 2)
           M=cv.moments(cnts)
           if M['m00'] != 0:
              center = (int(M['m10']/M['m00'])), int(M['m01']/M['m00'])
           if center:
            if colorIndex==0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex==1:
                gpoints[green_index].appendleft(center)
            elif colorIndex==2:
                rpoints[red_index].appendleft(center)
            elif colorIndex==3:
                ypoints[yellow_index].appendleft(center)

    else:
        bpoints.append(deque(maxlen=512))
        blue_index+=1
        gpoints.append(deque(maxlen=512))
        green_index+=1
        rpoints.append(deque(maxlen=512))
        red_index+=1
        ypoints.append(deque(maxlen=512))
        yellow_index+=1

    key = cv.waitKey(1) & 0xFF
    if key == ord('b'):
        colorIndex = 0
    elif key == ord('g'):
        colorIndex = 1
    elif key == ord('r'):
        colorIndex = 2
    elif key == ord('y'):
        colorIndex = 3
    elif key == ord('c'):
        bpoints = [deque(maxlen=1024)]
        gpoints = [deque(maxlen=1024)]
        rpoints = [deque(maxlen=1024)]
        ypoints = [deque(maxlen=1024)]
        blue_index = 0
        green_index = 0
        red_index = 0
        yellow_index = 0

        paintWindow[66:, :, :] = 255
    elif key == ord('q'):
        break


    points = [bpoints,gpoints,rpoints,ypoints]
    for i in range (len(points)):
        for j in range (len(points[i])):
            for k in range (len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv.line(frame, points[i][j][k-1], points[i][j][k], colors[i], 2)
                cv.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i],2)

    cv.imshow('LIVE FEED', frame)
    cv.imshow('Mask', mask)
    cv.imshow('AIR DOODLE', paintWindow)


vid.release()
cv.destroyAllWindows()