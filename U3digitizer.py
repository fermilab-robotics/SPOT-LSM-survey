import sys
from unicodedata import ucd_3_2_0 
sys.path.append('/usr/local/lib/')
sys.path.append('/LabJackPython/src/')

import LabJackPython
import u3
d=u3.U3() 


#help(u3)

class Digitizer(): 
    def __init__(self,device):
        self.device=device 
    def GetConfig(self): 
        self.readDefaultsConfig() #Reads the power-up defaults stored in flash
        self.device.configU3()
        d.configIO()   #io configuration  
        d.getAIN() #get an AIN
        ain0Command = u3.AIN(0, 31, True) #analog input ain command
        d.getCalibrationData()
        d.ReadFeedback()
    def run(self): 
        self.device.streamConfig()    #function in u3 
        self.device.streamStart()      #funciton in LabJackPython
        self.service.streamData()
    def start(self): 
        self.device.open()
        self.run()
        self.device.close()
    def DumpData(self):
        #to be continued
