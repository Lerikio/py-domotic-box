import pifacedigitalio
import threading

class RadioReceptor:
    def onReception(self):
        return 'hello'

class RadioTransmitter:
    
    def _init_(self):
        self.buffer = []
        this.bufferSemaphore = thread.allocate_lock()
        pfd = pifacedigitalio.PiFaceDigital();
        

    def processBuffer(self):
        this.bufferLock.acquire()
        pfd.leds[2].turn_off()
        toSend = buffer.pop()
        if value == 1: pfd.leds[2].turn_on()
        else 
           
        
        this.bufferLock.release()
        return 0
        
    