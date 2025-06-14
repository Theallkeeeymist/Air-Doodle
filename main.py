import cv2 as cv
import numpy as np
from collections import deque

frameWidth = 640
frameHeight = 480


def test():
    pass


trackbars = "HSV FILTER"
cv.namedWindow(trackbars)
cv.resizeWindow(trackbars, 640, 240)
cv.createTrackbar("Hue Min", trackbars, 106, 179, test)
cv.createTrackbar("Hue Max", trackbars, 179, 179, test)
cv.createTrackbar("Sat Min", trackbars, 55, 255, test)
cv.createTrackbar("Sat Max", trackbars, 255, 255, test)
cv.createTrackbar("Val Min", trackbars, 0, 255, test)
cv.createTrackbar("Val Max", trackbars, 255, 255, test)

vid = cv.VideoCapture(0)
vid.set(3, frameWidth)
vid.set(4, frameHeight)
kernel = np.ones((5, 5), np.uint8)

bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# assigning index values
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

colors = [(255, 255, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# starting the painting window setup
paintWindow = np.zeros((480, 640, 3)) + 255
paintWindow = cv.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
paintWindow = cv.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
paintWindow = cv.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
paintWindow = cv.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
paintWindow = cv.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)

cv.putText(paintWindow, "CLEAR", (62, 33), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(paintWindow, "BLUE", (185, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(paintWindow, "GREEN", (298, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(paintWindow, "RED", (420, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(paintWindow, "YELLOW", (520, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.namedWindow("AIR DOODLE")
cv.resizeWindow("AIR DOODLE", frameWidth, frameHeight)

while True:
    ret, frame = vid.read()
    # Flipping the frame to see same side of yours
    frame = cv.flip(frame, 1)

    hsvImg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Adding the colour buttons to the live frame for colour access
    frame = cv.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
    frame = cv.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
    frame = cv.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
    frame = cv.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
    frame = cv.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
    cv.putText(frame, "CLEAR", (62, 33), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(frame, "BLUE", (185, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(frame, "GREEN", (298, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(frame, "RED", (420, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(frame, "YELLOW", (520, 33), cv.FONT_ITALIC, 0.5, (0, 0, 0), 2, cv.LINE_AA)

    h_min = cv.getTrackbarPos("Hue Min", trackbars)
    h_max = cv.getTrackbarPos("Hue Max", trackbars)
    s_min = cv.getTrackbarPos("Sat Min", trackbars)
    s_max = cv.getTrackbarPos("Sat Max", trackbars)
    v_min = cv.getTrackbarPos("Val Min", trackbars)
    v_max = cv.getTrackbarPos("Val Max", trackbars)

    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])
    mask = cv.inRange(hsvImg, lower_hsv, upper_hsv)
    mask = cv.erode(mask, kernel, iterations=1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.dilate(mask, kernel, iterations=1)

    # Find contours for the pointer after idetifying it
    cnts, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    center = None

    # Ifthe contours are formed
    if len(cnts) > 0:
        # sorting the contours to find biggest
        cnt = sorted(cnts, key=cv.contourArea, reverse=True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Calculating the center of the detected contour
        M = cv.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # Now checking if the user wants to click on any button above the screen
        if center[1] <= 65:
            if 40 <= center[0] <= 140:  # Clear Button
                bpoints = [deque(maxlen=1024)]
                gpoints = [deque(maxlen=1024)]
                rpoints = [deque(maxlen=1024)]
                ypoints = [deque(maxlen=1024)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[66:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 1  # Green
            elif 390 <= center[0] <= 485:
                colorIndex = 2  # Red
            elif 505 <= center[0] <= 600:
                colorIndex = 3  # Yellow
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

    # Append the next deques when nothing is detected to avois messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    cv.imshow('LIVE FEED', frame)
    cv.imshow('Mask', mask)
    cv.imshow('AIR DOODLE', paintWindow)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()