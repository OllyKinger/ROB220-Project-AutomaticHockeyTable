import time
import serial
import numpy as np
import cv2 as cv
import glob
import cvzone 
import matplotlib.pyplot as plt
from cvzone.ColorModule import ColorFinder



arduinoData = serial.Serial('COM4', 115200)
cap = cv.VideoCapture(0)
cmd = ''
intersection_y = 0
ActualTarget = 0
CameraMatrix = np.array([[3.57113146e+03, 0.00000000e+00, 9.31680315e+02],
 [0.00000000e+00, 3.54737534e+03, 5.39541294e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

DistCoefficient = np.array([[-2.46317455e+00,  1.24411849e+01, -7.86637954e-02,  6.35301326e-02, -7.68346211e+01]])


y1 = 1500
cap.set(3,800)
cap.set(4,500)
CurrentPosition = 900
DistanceToMove = 0

posListX, posListY = [], []
xList =[item for item in range(0, 1300)]

while True: 
    ret, frame = cap.read()
    flipped = cv.flip(frame, 1)


    

    #dst = cv.undistort(frame, CameraMatrix, DistCoefficient, None, CameraMatrix)
    #cv.imshow('dst', dst)
    #The commented code here is for the camera calibration, It will be uncalibrated when the camera matrix and distortion coefficient are found 
    
    hsv = cv.cvtColor(flipped, cv.COLOR_BGR2HSV)

    lower_bound = np.array([56, 44, 72]) 
    upper_bound = np.array([69, 217, 188])

    mask = cv.inRange(hsv, lower_bound, upper_bound)
    imgContours, contours = cvzone.findContours(flipped, mask, minArea=200)
    result = cv.bitwise_and(flipped, flipped, mask=mask)

    coord =cv.findNonZero(mask)
    x = coord[0][0][0]
    y = coord[0][0][1]


    cv.imshow('mask', mask)


    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])

    

      

    if posListX:
        A, B = np.polyfit(posListX, posListY, 1)

    

        
                

        x_coords = list(xList)
        y_coords = [int((A*x + B)) for x in x_coords]

        if len(posListX) >= 2:
            dx = posListX[-1] - posListX[-2]
            dy = posListY[-1] - posListY[-2]
            y1 = posListY[-1]
    
            if dx != 0 or dy != 0:
                x = posListX[-1]
                y = posListY[-1]

                while 0 <= x < flipped.shape[1] and 0 <= y < flipped.shape[0]:
                    x_coords = [posListX[-1], x]
                    y_coords = [posListY[-1], y]
                    cv.line(imgContours, (x_coords[0], y_coords[0]), (x_coords[1], y_coords[1]), (0, 0, 255), 2)
                    x += dx
                    y += dy
                    

                    if x == 105: 
                        intersection_y = y
                        cv.circle(imgContours, (x, y), 5, (0, 255, 0), 2)
                        break            

        pass


            




            
    img = cv.line(imgContours,(105,0),(105,700),(0,255,0),2)
    imgContours = cv.flip(imgContours, 1)
    cv.imshow("ImageColor", imgContours)
    
   # cv.imshow("Image", flipped)

  
    
    TargetPosition = intersection_y

    if TargetPosition > 250:    
        TargetPosition = 250            
    elif TargetPosition < 10:      
        TargetPosition = 10

    if y > 250:    
        y = 250            
    elif y < 10:      
        y = 10

    #y1 = posListY[-1]

         

    if y1 > 250:
        y1 = 250
    elif y1 < 10:
        y1 = 10
    #on)
    Decimal = (TargetPosition - 10) / 290
    #print(TargetPosition)

    if Decimal == 0 : 
        pass
    else:
        ActualTarget = ((Decimal * 290)+10)

   

    intTargetPosition = int(TargetPosition)
    Command = intTargetPosition * 10
    y = y * 10
    y1 = y1 * 10
    
    sDistanceToMove = str(DistanceToMove)
    sCommand = str(Command)
    Sy = str(y)
    sY1 = str(y1)
    
 
    cmd = sCommand + '\n' 
    print(sCommand)
    arduinoData.write(cmd.encode())
    
    

    


    if cv.waitKey(1) == ord('q'): 
        break

