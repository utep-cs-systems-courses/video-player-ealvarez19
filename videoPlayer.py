import threading
import queue
from producerConsumer import producerConsumerQueue
import os
import cv2
import numpy as np
clipFile = "clip.mp4"
########################################################
def extractFrames(clipFile,colorQueue):
    count = 0                                            #count frames
    vidcap = cv2.VideoCapture(clipFile)                  #vidcap object

    success,image = vidcap.read()                        #image bitmap

    while success and count < 72:
        print("Extracting frame ",count)
        colorQueue.insertFrame(image)                    #insert to colorQueue
        success,image = vidcap.read()                    #get next image
        count+=1
    print("Extraction complete")
    colorQueue.insertFrame(None)                         #mark the end of the queue

########################################################
def convertFrames(colorQueue,grayQueue):
    count = 0
    while True:
        if colorQueue.isEmpty():                           #if there are not frames continue
            #print("Color queue empty")
            continue
        else:            
            colorFrame = colorQueue.getFrame()             #get colorFrame
            if colorFrame is None:                         #if it is the end of the colorqueue, end
                break
            print("Converting frame %i to gray scale" % (count))
            grayFrame = cv2.cvtColor(colorFrame,cv2.COLOR_BGR2GRAY)
            grayQueue.insertFrame(grayFrame)               #insert grayFrame to grayQueue
            count+=1
    print("Finished converting frames")
    grayQueue.insertFrame(None)                            #mark the end of the grayqueue
#########################################################          
def displayFrames(grayQueue):
    count = 0
    while True:
        if grayQueue.isEmpty():                            #if there are not gray frames
            continue
        else:
            grayFrame = grayQueue.getFrame()               #get frame to display
            if grayFrame is None:                          #if it is the end of grayqueue, end
                break
            print("Displaying Frame %i" % (count))
            cv2.imshow('Video',grayFrame)                  #show frame to display
            if cv2.waitKey(42) and 0xFF == ord("q"):       #wait 42 msec
                break
            count+=1                  
    cv2.destroyAllWindows()                  
    print("Finished displaying all frames")
#########################################################    

colorQueue = producerConsumerQueue()                        #queue with color frames
grayQueue = producerConsumerQueue()                         #queue with gray frames

extractThread = threading.Thread(target = extractFrames, args = (clipFile,colorQueue))
convertThread = threading.Thread(target = convertFrames, args = (colorQueue,grayQueue))
displayThread = threading.Thread(target = displayFrames, args = {grayQueue})

#start threads
extractThread.start()
convertThread.start()
displayThread.start()
