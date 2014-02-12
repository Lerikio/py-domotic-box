import pifacedigitalio
import threading

class RadioTransceiver(Thread):

    def _init_(self):
        self.piface = pifacedigitalio.PiFaceDigital()

        self.writeBuffer = []
        self.writeBufferMutex = Semaphore(value=1)
        self.writeBufferSemaphore = Semaphore(value=0)

        self.readBuffer = []

    def run():
        radioTransmitter = RadioTransmitter(self.writeBuffer, self.writeBufferMutex, self.writeBufferSemaphore, self.piface)
        radioTransmitter.start()

    def addToWriteBuffer(self, sequence):
        self.writeBufferMutex.acquire()
        this.writeBuffer.extend(sequence)
        self.writeBufferMutex.release()
        self.writeBufferSemaphore.release(len(sequence))


class RadioTransmitter(Thread): 
    
    def _init_(self, writeBuffer, writeBufferMutex, writeBufferSemaphore, piface):
        this.buffer = writeBuffer
        self.writeBuffer = writeBuffer
        self.writeBufferMutex = writeBufferMutex
        self.writeBufferSemaphore = writeBufferSemaphore
        self.piface = piface
        self.pin = 2
        
    def run():
        this.processBuffer()

    def processBuffer(self):
        self.piface.leds[self.pin].turn_off()
        self.writeBufferSemaphore.acquire()
        self.bufferMutex.acquire()
        toSend = this.buffer.pop()
        self.bufferMutex.release()
        if toSend[0] == 1: pfd.leds[self.pin].turn_on()
        t = threading.Timer(toSend[1]/1000, self.processBuffer)
        t.start()

#class RadioReceptor(Thread): 
    
