from accurad.accurad import ACCURAD as ACR 
from serial import SerialException
from .digitizer import Digitizer


class  Mirion(Digitizer):
    """
        Obtain rad dose from the Mirion device
    """
    def __init__(self,port):
        super(Digitizer,self).__init__()
        self.port=port
        self.d=None
    
    def get_config(self):
        """
            detect port for mirion 
        """
        try: 
            self.d= ACR(self.port)
        except SerialException as e:
            print(f"Error opening serial connection on {self.port}: {e}")
            return False
        return True
    
    def start(self):
        """
            getting the data
        """
        data= self.d.get_dose_rate
        if not data:
            print("no data")
            return None
        else:
            return data 
        
    
    def stop(self): 
        """
            close port
        """
        self.port.close()



        
    
        

    

    


