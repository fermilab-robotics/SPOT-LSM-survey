from abc import ABCMeta, abstractclassmethod
from collections import defaultdict

class DataAcquisition(metaclass=ABCMeta):
    """
        To acquire localization and digitizer's data 
    """
    def __init__(self,robot,tag,digitizer):
        self.robot=robot
        self.tag=tag
        self.digitizer=digitizer
        self.data=defaultdict(dict)

    @abstractclassmethod
    def l_daq(self):
        """
            daq for localization
        """
        pass
        # time=self.localization.get_time()
        # self.data[time]["vision"]=self.localization.visionxform()
        # self.data[time]["odom"]=self.localization.odomxform()
    
    @abstractclassmethod 
    def d_daq(self):
        """
            daq for digitizer
        """
        pass
        







    
