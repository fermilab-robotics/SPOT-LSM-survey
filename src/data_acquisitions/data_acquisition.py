
from collections import defaultdict
import datetime

class DataAcquisition():
    """
        To acquire localization and digitizer's data 
    """
    def __init__(self,robot,tag,digitizer):
        self.robot=robot
        self.tag=tag
        self.digitizer=digitizer
        self.bot_data=defaultdict(dict)
        self.tag_data=defaultdict(dict)
        self.d_data=defaultdict(set)
        self.bot_flag=False


    def bot_daq(self):
        """
            daq for spot data
        """
        time=self.robot.get_time()
        self.bot_flag=True
        vision=self.robot.visionxform()
        odom=self.robot.odomxform()
        self.bot_data[time]['vision']=vision
        self.bot_data[time]['odom']=odom

    
    def tag_daq(self):
        """
            daq for april tag data 
        """
        if not self.bot_flag:
            print("Take spot's localization first")
        else:     
            time=self.tag.get_time()
            vision=self.tag.visionxform()
            odom=self.tag.odomxform()
            self.tag_data[time]['vision']=vision
            self.tag_data[time]['odom']=odom


     

    def d_daq(self):
        """
            daq for digitizer data 
        """
        if self.digitizer.get_config():
            dose=self.digitizer.start()
            time=datetime.datetime.now()
            self.d_daq[time]=dose
        







    
