import cv2
import imutils
import time
import numpy as np

# Show debug info
debug = True

# if false an image of an dog is shown
showVideo = True 

# set frame size
FrameWidth = 1280
FrameHeight = 720

# time to remind the user to smile
smileReminder = 15

# time the user has to smile
timeToSmile = 10

# Get webcam
cam = cv2.VideoCapture(0)
# # or get Video Stream
# cam = cv2.VideoCapture("http://192.168.178.21:8080/video?type=some.mjpg")

# # load funny image
# dog = cv2.imread('images/image.jpg')
# # or show video
# video1 = cv2.VideoCapture("videos/video.mp4")

# Create the haar cascade for face and smile recognition
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml') 

# function to detect a face and a smile inside
def detectSmile(gray, frame): 
    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
    smileFound = False
    # search in found faces
    for (x, y, w, h) in faces: 
        if debug:
            cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2) 
        roi_gray = gray[y:y + h, x:x + w] 
        roi_color = frame[y:y + h, x:x + w] 
        # detect smiles
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20) 
  
        for (sx, sy, sw, sh) in smiles: 
            # smile found!
            if debug:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2) 
            smileFound = True
    return frame, smileFound

# display debug info if enabled
def debugInfo(frame, smile):
    # display total elapsed time in seconds
    cv2.putText(frame, "Elapsed time: " + str(elapsedTotal), (5, FrameHeight - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255)) 
    # display time smiled 
    cv2.putText(frame, "Time smiled: " + str(timeSmiled), (5, FrameHeight - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
    # display if smile detected or not
    if(smile):
        cv2.putText(frame, "Smile: Yes", (5, FrameHeight - 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)    
    else:
        cv2.putText(frame, "Smile: No", (5, FrameHeight - 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)  

# time since last rendered frame and start time
startTime = time.time()
prevTime = startTime   

# calculate time since last smiling and current time smiled 
sinceLastSmile = startTime
timeSmiled = 0

while True: 
    # Captures video_capture frame by frame 
    _, frame = cam.read() 

    # get current time
    curTime = time.time()
    # calculate elapsed time 
    elapsed = curTime - prevTime

    # if more than 0.2 seconds elapsed, draw new frame ~ 5 frames per second
    if(elapsed > 0.2):
        # resize image for better performance
        frame = imutils.resize(frame, width=FrameWidth, height=FrameHeight)

        # reset frame timer
        prevTime = curTime 

        # get total elapsed time
        elapsedTotal = int(curTime - startTime)

        # To capture image in monochrome                     
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

        # detect Smiles
        frame, smileFound = detectSmile(gray, frame)  

        # if smile detected add smiled time
        if(smileFound):
            timeSmiled += elapsed
            # if progress is complete, reset timer
            if(timeSmiled > timeToSmile):
                sinceLastSmile = curTime
                timeSmiled = 0

        # print debug info if enabled
        if debug:
            debugInfo(frame, smileFound)

        # if not smiled for more than "smileReminder" seconds -> smile
        elapsedSinceLastSmile = int(curTime - sinceLastSmile)
        if(elapsedSinceLastSmile >= smileReminder):
            # # offset for dog or video image
            # offsetY = int((FrameWidth/4)*3)

            # if showVideo: 
            #     ret, smileVideoFrame = video1.read()
            #     if not (ret):
            #         video1.set(cv2.CAP_PROP_POS_FRAMES, 0)
            #         ret, smileVideoFrame = video1.read()
            #     # resize image for better performance
            #     smileVideoFrame = imutils.resize(smileVideoFrame, width=int(FrameWidth/4), height=int(FrameHeight/4))
            #     frame[0:smileVideoFrame.shape[0], offsetY:offsetY+smileVideoFrame.shape[1]] = smileVideoFrame
            # else: 
            #     dog = imutils.resize(dog, width=int(FrameWidth/4), height=int(FrameHeight/4))
            #     frame[0:dog.shape[0], offsetY:offsetY+dog.shape[1]] = dog

            # Display text and current smile progress
            cv2.putText(frame, "Progress: ", (5,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0)) 
            cv2.rectangle(frame, (160, 40), (260, 60), (0, 0, 255), -1)
            progressSmiled = timeSmiled * 10  
            cv2.rectangle(frame, (160, 40), (160 + int(progressSmiled), 60), (0, 255, 0), -1)
            cv2.putText(frame, "Please smile :)", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0)) 
    
        # Displays the result on camera feed                      
        cv2.imshow('Video', frame)  
    
        # The control breaks once q key is pressed                         
        if cv2.waitKey(1) & 0xff == ord('q'):                
            break
  
# Release the capture once all the processing is done. 
cam.release()                                  
cv2.destroyAllWindows() 
