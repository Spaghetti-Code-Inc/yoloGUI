# program to capture single image from webcam in python

# importing OpenCV library
import cv2
import keyboard
import time

 
def runCamera():
    # initialize the camera
    cam_port = 0

    vid = cv2.VideoCapture(cam_port)

    # Determines if the 'vid' should grab a new frame or not
    getFrame = True

    while(vid.isOpened()):
        # reading the input using the camera
        if getFrame == True:
            ret,frame=vid.read()

        # THE BUTTON PRESS TO CHANGE
        # Once this key is pressed getFrame is flipped
        if keyboard.is_pressed("b"):
            if(getFrame): 
                getFrame = False

            else: 
                getFrame = True
            
            # Needed so holding down the button does not send multiple commands
            time.sleep(.2)

        # showing result, it take frame name and image

        # output
        cv2.imshow('Video',frame)

        if cv2.waitKey(1) & 0xFF ==ord('e'):
            break

    vid.release()

    cv2.destroyAllWindows()

runCamera()