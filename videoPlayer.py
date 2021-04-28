import threading
import queue
from producerConsumer import producerConsumerQueue
import os
import cv2

clipFile = "clip.mp4"

########################################################
def extractFrames(clipFile,colorQueue):
    count = 0                                            #count frames
    vidcap = cv2.VideoCapture(clipFile)                  #vidcap object

    success,image = vidcap.read()                        #image bitmap

    while success and count < 72:                        
        success,jpegImage = cv2.imencode('.jpeg',image)  #convert image to jpeg
        colorQueue.insertFrame(jpegImage)                #insert to colorQueue
        success,image = vidcap.read()                    #get next image
        count+=1

    print("Extraction complete")

########################################################
def convertFrames(colorQueue,grayQueue):
    while True:
        if colorQueue.empty():                           #if there are not frames continue
            continue
        colorFrame = colorQueue.getFrame()
        grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        grayQueue.insertFrame(grayFrame)
#########################################################          
def displayFrames(grayQueue):
    while True:
        if grayFrame.isEmpty():                         #if there are not gray frames
            continue
        if count == 72:                                 
            break
        displayFrame = grayFrame.getFrame()             #frame to display
        cv2.imshow('Video',frame)                       #show frame to display
        if cv2.waitKey(42) and 0xFF == ord('q'):        #wait 42 msec
            break
        count+=1                  
    cv2.destroyAllWindows()                  
    
#########################################################    

colorQueue = producerConsumerQueue()
grayQueue = producerConsumerQueue()

extractThread = threading.Thread(target = extractFrames, args = (clipFile,colorQueue))
convertThread = threading.Thread(target = convertFrames, args = (colorQueue,grayQueue))
displayThread = threading.Thread(target = convertFrames, args = (grayQueue))
