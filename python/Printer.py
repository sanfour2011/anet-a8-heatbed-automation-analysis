import serial
import time

class anetA8Plus:
    
    def __init__(self, comPort):
        self.comPort = comPort
        self.serialPort = serial.Serial(comPort, baudrate=115200, timeout=1)
        # self.xLim_min = xLim_min
        # self.xLim_max = xLim_max
        # self.yLim_min = yLim_min
        # self.yLim_max = yLim_max
        # self.zLim_min = zlim_min
        # self.zlim_max = zlim_max

    
    def ReadFromPrinter(self):
        msg = self.serialPort.read_until('\n').rstrip()   
        if msg == b'': # test an empty string
            return 'error'
        return msg.decode('ascii')    
        
    def Write2Printer(self,cmd): 
        self.serialPort.write(bytes(bytes(cmd+'\n', 'utf-8')))
        resp = self.ReadFromPrinter()    
        if resp == b'':
            return 'error'
        return resp        

    def Connect2Printer(self):        
        while 1:##loop with timeout
            serialString = self.serialPort.read_until('\n').rstrip()
            serialString = serialString.decode('ascii')
            if serialString == 'echo:SD card ok':
                return True            
        raise NameError("Could not connect to Printer over Serial Port: ",self.comPort)
        
    def PrinterConf(self):
        cmd = 'G91\n' #G91: use relative positioning for the XYZ axes
        resp = self.Write2Printer(cmd)
        if resp != 'ok':
            raise RuntimeError("error setting Printer to Relative Move G91")
            
        return True
     
    def MoveXY(self,x,y):
        cmd = "G1 X{0} Y{1}\n".format(x,y)  
        resp = self.Write2Printer(cmd)  
        if resp != 'ok':
            raise NameError("error MoveXY cmd: ",cmd)
        return True
        
    def MoveX(self,x):
        cmd = "G1 X{0}\n".format(x)
        resp = self.Write2Printer(cmd)   
        if resp != 'ok':
            raise NameError("error MoveX cmd: ",cmd)
        return True   

    def MoveY(self,y):
        cmd = "G1 Y{0}\n".format(y)
        resp = self.Write2Printer(cmd)  
        if resp != 'ok':
            raise NameError("error MoveY cmd: ",cmd)       
        return True
        
    def MoveZ(self,z):
        cmd = "G1 Z{0}\n".format(z)
        resp = self.Write2Printer(cmd)  
        if resp != 'ok':
            raise NameError("error MoveY cmd: ",cmd)       
        return True  
     
    def ReturnHome(self,x=False,y=False,z=False):
        cmd = "G28"
        if x :
            cmd+=' X'
        if y :
            cmd+=' Y'
        if z:
            cmd+=' Z'
        cmd +='\n'
        self.Write2Printer(cmd)      
        if self.WaitForMotionDone() != True:
            raise RuntimeError()('error ReturnHome cmd:{}'.format(cmd))
        return True
    
    def GetCurrentPosition(self):
            #M114
            #X:0.00 Y:127.00 Z:145.00 E:0.00 Count X:0 Y:10160 Z:116000 <--- ?? stimmt das ??
        st = self.Write2Printer("M114")
        kor = st.split(" ")
        x = kor[0].split(":")[1]
        y = kor[1].split(":")[1]
        z = kor[2].split(":")[1]
        return x,y,z
            
    def PrintCurrent(self):
        pass   
        #M909 - DAC Print Values

    def GetFirmwareInfo(self):
        #M115 - Firmware Info
        return self.Write2Printer("M115")

    def WaitForMotionDone(self):
        self.Write2Printer("M400")#M400 - Finish Moves
        while self.ReadFromPrinter().find('busy') != -1: ##echo:busy: processing<\n> 
            time.sleep(0.6)           
        #danach kommt ein OK
        return True
    
    def TestMethod(self):
        print("hello from PrinterClass")

    def TestMethod_2(self):
        self.TestMethod()

    def Close(self):
        self.serialPort.close()
    
    