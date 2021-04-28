import threading
import queue

lock = threading.Lock()
class producerConsumerQueue():

    def __init__(self):
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(10)
        self.framesQueue = queue.Queue()

    def insertFrame(self,frame):               #insert into queue
        self.empty.acquire()
        lock.acquire()
        self.framesQueue.put(frame)
        lock.release()
        self.full.release()
        

    def getFrame(self):                         #get and delete from queue
        self.full.acquire()
        lock.acquire()
        frame = self.framesQueue.get()
        lock.release()
        self.empty.release()
        return Frame

    def isEmpty(self):                         #check if is empty
        lock.acquire()
        isEmpty = framesQueue.empty()
        lock.release()
        return isEmpty
