from buildhat import Motor
import cv2
from module import findnameoflandmark,findpostion,speak
import math

#Use CV2 Functionality to create a Video stream and add some values + variables
cap = cv2.VideoCapture(0)
tip=[8,12,16,20,4]
tipname=[8,12,16,20,4]
fingers=[]
old_fingers = []
finger=[]
thumb = 1
old_thumb = 1

thumb_motor = Motor('A')
index_motor = Motor('B')
middle_motor = Motor('C')
pinky_motor = Motor('D')

def open_thumb(thumbool):
    #thumb motor
    if thumbool==False:
        thumb_motor.run_to_position(90)
    else:
        thumb_motor.run_to_position(0)

def move_fingers(fingers_list):
    #pinky motor
    if fingers_list[3] == 1:
        pinky_motor.run_to_position(0)
    else:
        pinky_motor.run_to_position(90)
    
    #index motor
    if fingers_list[0] == 1:
        index_motor.run_to_position(0)
    else:
        index_motor.run_to_position(-80)
    
    #middle fingers motor
    if fingers_list[1] == 0 and fingers_list[2] == 0:
        middle_motor.run_to_position(80)
    else:
        middle_motor.run_to_position(0)
        
#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
while True:
     
     ret, frame = cap.read() 
     #Unedit the below line if your live feed is produced upsidedown
     #flipped = cv2.flip(frame, flipCode = -1)
     
     #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
     frame1 = cv2.resize(frame, (320, 240))
    
    #Below is used to determine location of the joints of the fingers 
     a=findpostion(frame1)
     b=findnameoflandmark(frame1)
     
     #Below is a series of If statement that will determine if a finger is up or down and
     #then will print the details to the console
     if len(b and a)!=0:
        
        finger=[]
        if a[0][1:] < a[4][1:]: 
           finger.append(1)
           #print('a')
           thumb = 0
        else:
           finger.append(0)
           #print('b')
           thumb = 1
        fingers=[] 
        for id in range(0,5):
            if a[tip[id]][2:] < a[tip[id]-2][2:]:
               #print(b[tipname[id]])

               fingers.append(1)
    
            else:
               fingers.append(0)
     #Below will print to the terminal the number of fingers that are up or down          
     x=fingers + finger
     if thumb!= old_thumb:
         if thumb==0:
             open_thumb(False)
         else:
             open_thumb(True)
         old_thumb = thumb
     
     if fingers != old_fingers:
         move_fingers(fingers)
         old_fingers = fingers
     
     #Below shows the current frame to the desktop 
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     
     #Below states that if the |s| is press on the keyboard it will stop the system
     if key == ord("s"):
       break

