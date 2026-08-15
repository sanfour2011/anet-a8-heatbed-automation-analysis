import serial
import time


class Gauge:
    min_Limit = -1
    max_Limit = 1

    def __init__(self, comPort):
        self.comPort = comPort
        self.serialPort = serial.Serial(self.comPort, baudrate=9600, timeout=0.8)
        self.retrieReading = 10  # how many times should be retried to read a valid responce
        # time.sleep(2)

    def Reconnect(self):
        self.serialPort.close()
        self.serialPort = serial.Serial(self.comPort, baudrate=9600, timeout=0.8)
        time.sleep(2)

    def Write2Gauge(self, cmd):
        self.serialPort.write(bytes(bytes(cmd+'\n', 'utf-8')))
        # time.sleep(0.5)
        resp = self.serialPort.read_until('\n').rstrip()
        return resp

    def Measure(self):
        resp = ""
        while True:
            if self.Write2Gauge('m') == b'OK':
                resp = self.Write2Gauge('g')
               # resp = resp.decode('ascii') #is it really needed??
                if self.IsValidMeasurement(resp):
                     return resp.decode('ascii')
            
            self.Reconnect()
                
    def IsValidMeasurement(self,measValue):
        if measValue == b'' or len(measValue) <=0:
            return False
        measValueAsFloat = float(measValue)
        if measValueAsFloat > 1 or measValueAsFloat < -1:
            return False
        return True

    def Close(self):
        self.serialPort.close()
        
    def TestMethod(self):
        print("hello from test method")
        
