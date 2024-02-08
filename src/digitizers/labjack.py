import traceback
import u3
import LabJackPython 

from .digitizer import Digitizer

SCAN_FREQUENCY=1

class LabJack(Digitizer):
    """
        obtain rad dose from LabJack device 
    """
    def __init__(self):
        self.d=None 
        self.streaming=False

    def get_config(self): 
        """
            set up device for streaming
        """
        try: 
            self.d=u3.U3()
        except:
            print("".join(i for i in traceback.format_exc())) 
        else: 
            self.d.configIO(FIOAnalog=1)   #io configuration for ditgital  
            self.d.getCalibrationData()
            self.d.streamConfig(NumChannels=1, PChannels=[0], NChannels=[31], Resolution=3, ScanFrequency=SCAN_FREQUENCY)

    def start(self):
        """
            get the data
        """
        self.d.streamStart()
        try:
            data=next(self.device.streamData())
            if len(data['AIN0'])>0: return data['AIN0'][0]
            
        except: 
            print("no data")
    
    def stop(self):
        """
            stop streaming 
        """
        self.d.streamStop() 
        self.d.close()


        


