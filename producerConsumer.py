import threading
import queue

lock = threading.Lock()
class producerConsumerQueue():

    def __init__(self):
        self.full = threading.Semaphore(0)    #0 spots available
        self.empty = threading.Semaphore(10)  #10 spots available
        self.framesQueue = queue.Queue()

    def insertFrame(self,frame):               #insert into queue
        self.empty.acquire()                   #decrement empty (take available spot away)
        lock.acquire()                         #avoid collisions
        self.framesQueue.put(frame)            #insert frame
        lock.release()
        self.full.release()                    #increment full (take a spot)
        

    def getFrame(self):                        #get and delete from queue
        self.full.acquire()                    #decrement full (remove spot full)
        lock.acquire()
        frame = self.framesQueue.get()         #remove/get frame
        lock.release()
        self.empty.release()                   #increment empty (another empty spot available)
        return frame

    def isEmpty(self):                         #check if queue is empty
        lock.acquire()
        isEmpty = self.framesQueue.empty()
        lock.release()
        return isEmpty
