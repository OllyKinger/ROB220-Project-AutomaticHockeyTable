import time
import serial
import numpy as np
import cv2 as cv
import glob
import cvzone 
import matplotlib.pyplot as plt
from cvzone.ColorModule import ColorFinder


#myColourFinder = ColorFinder(True)
arduinoData = serial.Serial('COM4', 115200)
cap = cv.VideoCapture(0)
cmd = ''
intersection_y = 0
ActualTarget = 0
CameraMatrix = np.array([[3.57113146e+03, 0.00000000e+00, 9.31680315e+02],
 [0.00000000e+00, 3.54737534e+03, 5.39541294e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

DistCoefficient = np.array([[-2.46317455e+00,  1.24411849e+01, -7.86637954e-02,  6.35301326e-02, -7.68346211e+01]])
#These 2 are for the camera on my laptop and wont work anyway, just a placeholder at the moment

y1 = 1500
cap.set(3,800)
cap.set(4,500)
CurrentPosition = 900
DistanceToMove = 0

posListX, posListY = [], []
xList =[item for item in range(0, 1300)]#I have no possible idea what this does

while True: 
    ret, frame = cap.read()
    flipped = cv.flip(frame, 1)

   # cv.imshow('frame', flipped)
    

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

    #circle = cv.circle(flipped, (x,y), 5, (0,0,255), 2)
    cv.imshow('mask', mask)
    #cv.imshow('contours',contours)
    #cv.imshow('result', result)
    #This is where the trajectory prediction will go

    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])
        #M = cv.moments(int(contours[0])['cnt'])
        #cnt = contours[0]['cnt']
        #M = cv.moments(cnt)
        #posListX.append(int(M['m10']/M['m00']))
        #posListY.append(int(M['m01']/M['m00']))
    

      

    if posListX:
        A, B = np.polyfit(posListX, posListY, 1)

    
        ''' for i, (posX, posY) in enumerate(zip(posListX, posListY)):
            pos = (posX, posY)
            cv.circle( imgContours, pos, 5, (0, 255, 0), cv.FILLED)
            if i == 0: 
                cv.line( imgContours, pos, pos, (0, 255, 0), 2)
                cv.line( flipped, (posListX[i-1], posListY[i-1]), (255, 0, 0), 2)
            else: 
                print("Eeeeeeeeee")
                cv.line( imgContours, (posListX[i-1], posListY[i-1]), pos, (255, 0, 0), 2)'''
        # This section can be uncommented for troubleshooting
        
                

        x_coords = list(xList)
        y_coords = [int((A*x + B)) for x in x_coords]
        #cv.line( imgContours, (x_coords[0], y_coords[0]), (x_coords[-1], y_coords[-1]), (0, 255, 0), 2)
        #cv.line( imgContours, (posListX[-1], posListY[-1]), (x_coords[0], y_coords[0]), (0, 255, 0), 2) 

        #ADD NEW CODE HERE: 
        # if len(posListX) >= 2:
        #    cv.line(flipped, (posListX[-2], posListY[-2]), (posListX[-1], posListY[-1]), (0, 255, 0), 2)
        '''if len(posListX) >= 2:
            x = posListX[-1] - posListX[-2] + 100
            y = posListY[-1] - posListY[-2] + 100
        if x == 0 and y == 0:
            pass
        x = posListX[-1] + x
        y = posListY[-1] + y
        while 0 <= x < flipped.shape[1] and 0 <= y < flipped.shape[0]:
            x_coords = [posListX[-1], x]
            y_coords = [posListY[-1], y]
            cv.line(flipped, (x_coords[0], y_coords[0]), (x_coords[-2], y_coords[-2]), (0, 255, 0), 2)
            x += x
            y += y
        pass'''

        #this drawws a line in the direction the contour is moving 
        #cv.line( flipped, (posListX[-1], posListY[-1]), (posListX[-1] + 100, posListY[-1] + 100), (0, 255, 0), 2) 

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
                    #print("this is x:", x ,"this is y:", y)

                    if x == 105: 
                        intersection_y = y
                        cv.circle(imgContours, (x, y), 5, (0, 255, 0), 2)
                        break
                    #print("this is x:", x ,"this is y:", y) 
                    #detects if the lines intersect and if they do it will draw a circle at the intersection
                '''if len(contours) > 0:
                        if cv.pointPolygonTest(contours[0]['cnt'], (x, y), False) >= 0:
                            intersection_y = y
                            cv.circle(imgContours, (x, y), 5, (0, 255, 0), 2) 
                            #print("this is x:", x ,"this is y:", y)'''
                        
                        

                 
                
                

        pass


            




            

    # draw a line that is vertical 100 pixels from the right side of the screen 
    #cv.line( flipped, (flipped.shape[1] - 100, 0), (flipped.shape[1] - 100, flipped.shape[0]), (0, 255, 0), 2)
        #cv.line( flipped, (x_coords[0], y_coords[0]),(posListX[-1], posListY[-1] ), (0, 255, 0), 2)
       
       # cv.line( imgContours, (posListX[0], posListY[0]), (posListX[-1], posListY[-1]), (0, 255, 0), 2) 
    #imgContours = cv.undistort(frame, CameraMatrix, DistCoefficient, None, CameraMatrix)
    #this draws a vertical line in the middle of the screen imgContours 
    img = cv.line(imgContours,(105,0),(105,700),(0,255,0),2)
   # cv.resize(imgContours, (0, 0), None, 0.3, 0.3)
   # cv.resizeWindow(imgContours, 1280,720)
    #fart = cv.getWindowImageRect(imgContours)
    #print(fart)
    imgContours = cv.flip(imgContours, 1)
    cv.imshow("ImageColor", imgContours)
    
   # cv.imshow("Image", flipped)

  
    
    TargetPosition = intersection_y

    #Pixel to mm conversion will happen here
    #pixel2mm= 1.0
    #ActualTarget = TargetPosition * pixel2mm

    #this is where I will keep track of the position of the blocker
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

   
    #DistanceToMove = ActualTarget - CurrentPosition
    #print(ActualTarget)
    intTargetPosition = int(TargetPosition)
    Command = intTargetPosition * 10
    y = y * 10
    y1 = y1 * 10
    
    sDistanceToMove = str(DistanceToMove)
    #print(DistanceToMove)
    #CurrentPosition = ActualTarget
    sCommand = str(Command)
    Sy = str(y)
    sY1 = str(y1)
    
   # time.sleep(0.1)
    cmd = sCommand + '\n' # need to change Actual target to a different variable
    print(sCommand)
    arduinoData.write(cmd.encode())
    #CurrentPosition = ActualTarget
    #time.sleep(0.1)
    

    


    if cv.waitKey(1) == ord('q'): 
        break

