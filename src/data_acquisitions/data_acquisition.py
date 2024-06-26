from bosdyn.client.math_helpers import quat_to_eulerZYX
from collections import defaultdict,namedtuple
import datetime
import json

Data = namedtuple('data', ['time','data'])
Frames = namedtuple('frame', ['yaw','pitch','roll'])

def quat_to_Euler(frame):
    """
        method to convert Quaternions to Euler Angles
    """

    rot=quat_to_eulerZYX(frame.rot)
    return Frames(rot[0],rot[1],rot[2])

class DataAcquisition():
    """
        To acquire localization and digitizer's data 
    """
    def __init__(self,robot,tag,digitizer):
        self.robot=robot
        self.tag=tag
        self.digitizer=digitizer
        self.data=defaultdict(dict)
        self.bot_data=defaultdict(dict)
        self.tag_data=defaultdict(dict)
        self.r_data=defaultdict(set)
        self.bot_flag=False
        self.data_pts=0
        print('ready to take data..')


    def bot_daq(self):
        """
            daq for spot data
        """
        time=self.robot.get_time()
        self.bot_flag=True
        vision=self.robot.visionxform()
        # odom=self.robot.odomxform()
        self.data_pts+=1
        self.bot_data[time]={}
        self.bot_data[time].update({'vision':vision})
        bot_euler_angle=quat_to_Euler(vision)
        self.bot_data[time].update({'yaw':bot_euler_angle.yaw})
        self.bot_data[time].update({'pitch':bot_euler_angle.pitch})
        self.bot_data[time].update({'roll':bot_euler_angle.roll})
        # self.bot_data[time].update({'odom':odom})
        self.data[self.data_pts]['spot']={time:self.bot_data[time]}
    
    def tag_daq(self):
        """
            daq for april tag data 
        """
        if not self.bot_flag:
            print("Take spot's localization first")
        else:     
            time=self.tag.get_time()
            vision=self.tag.visionxform()
            # odom=self.tag.odomxform()
            self.tag_data[time]={}
            self.tag_data[time].update({'vision':vision})
            tag_euler_angle=quat_to_Euler(vision)
            self.tag_data[time].update({'yaw':tag_euler_angle.yaw})
            self.tag_data[time].update({'pitch':tag_euler_angle.pitch})
            self.tag_data[time].update({'roll':tag_euler_angle.roll})
            # self.tag_data[time].update({'odom':odom})
            self.data[self.data_pts]['tag']={time:self.tag_data[time]}

     

    def d_daq(self):
        """
            daq for digitizer data 
        """
        if self.digitizer.get_config():
            dose=list(self.digitizer.start())
            time=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # self.r_data[self.data_pts]=Data(time,dose)
            self.r_data[time]={}
            self.r_data[time].update({"mrem_p_h":dose[0]})
            self.r_data[time].update({"counts_per_second":dose[1]})
            self.r_data[time].update({"mrem":dose[2]})
            self.r_data[time].update({"duration":dose[3]})
            self.data[self.data_pts]['mirion']={time:self.r_data[time]}
            

        







    
