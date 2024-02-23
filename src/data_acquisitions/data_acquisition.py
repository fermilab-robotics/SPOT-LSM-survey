
from collections import defaultdict,namedtuple
import datetime

Data = namedtuple('data', ['time','data'])

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
        self.r_data=defaultdict(set)
        self.bot_flag=False
        self.data_pts=0 


    def bot_daq(self):
        """
            daq for spot data
        """
        time=self.robot.get_time()
        self.bot_flag=True
        vision=self.robot.visionxform()
        odom=self.robot.odomxform()
        self.data_pts+=1
        self.bot_data[self.data_pts]['vision']=Data(time,vision)
        self.bot_data[self.data_pts]['odom']=Data(time,odom)

    
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
            self.tag_data[self.data_pts]['vision']=Data(time,vision)
            self.tag_data[self.data_pts]['odom']=Data(time,odom)


     

    def d_daq(self):
        """
            daq for digitizer data 
        """
        if self.digitizer.get_config():
            dose=self.digitizer.start()
            time=datetime.datetime.now()
            self.r_data[self.data_pts]=Data(time,dose)

        







    
