import u3
import LabJackPython
import pickle
import argparse

SCAN_FREQUENCY= 2  

parser=argparse.ArgumentParser()
parser.add_argument("-v","--verbose",action="store_true")
args=parser.parse_args()

class Digitizer(): 
    def __init__(self,device):
        self.device=device
        self.streaming=False
        self.data=dict()
    
    def GetConfig(self): 
        self.device.configIO(FIOAnalog=1)   #io configuration for ditgital  
        self.device.getCalibrationData()
        self.device.streamConfig(NumChannels=1, PChannels=[0], NChannels=[31], Resolution=3, ScanFrequency=SCAN_FREQUENCY)

    def streamInit(self):  
        self.device.streamStart()      #set the flag indicated stream started 
        self.streaming=True 

    def start(self): 
        self.GetConfig()
        self.streamInit()
        
        while self.streaming: 
            r=next(self.device.streamData())
            time=datetime.now()
            if not r: 
                print(f'No data : {datetime.now()}')
                continue
            else: 
                self.data.update({time:r['AIN0']})

    def stop(self):
        self.streaming=False
        self.device.streamStop() 
        self.device.close()



if __name__=="__main__":
    d=Digitizer(u3.U3())
    try: 
        while True: 
            d.start()
    except KeyboardInterrupt: 
        print('\n interuppted,collecting data..')
    finally: 
        pickle.dump( d.data, open( "/data/labjack.pickle", "wb" ))
        if args.verbose:
            read=pickle.load( open( "/data/labjack.pickle", "rb" ))
            for time in read:
                print(f'time: {time} \t voltages: {read[time]}')
