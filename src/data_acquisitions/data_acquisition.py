from bosdyn.client.math_helpers import quat_to_eulerZYX
from collections import defaultdict,namedtuple

import os
from datetime import datetime
import time
import logging 


logger=logging.getLogger(__name__)

Data = namedtuple('data', ['time','data'])
Frames = namedtuple('frame', ['yaw','pitch','roll'])

#set timezone 
os.environ['TZ'] = 'CST6CDT'
time.tzset()

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



    def bot_daq(self):
        """
            daq for spot data
        """
        time=self.robot.get_time()
        
        self.bot_flag=True
        vision=self.robot.visionxform()
        Position_X,Position_Y,Position_Z=vision.get_translation()

        self.bot_data[time]={}
        self.bot_data[time].update({'Position X':Position_X})
        self.bot_data[time].update({'Position Y':Position_Y})
        self.bot_data[time].update({'Position Z':Position_Z})

        bot_euler_angle=quat_to_Euler(vision)
        self.bot_data[time].update({'Pitch':bot_euler_angle.pitch})
        self.bot_data[time].update({'Roll':bot_euler_angle.roll})
        self.bot_data[time].update({'Yaw':bot_euler_angle.yaw})
        
        self.data['spot']={time:self.bot_data[time]}
        logger.info(f"data for spot taken at {time}")
    
    def tag_daq(self):
        """
            daq for april tag data 
        """
        if not self.bot_flag:
            logger.warning("Take spot's localization first")
        else:     
            
            vision=self.tag.visionxform()
            
            time=self.tag.get_time()
            self.tag_data[time]={}
            
            for idx,f in enumerate(self.tag.fiducial): 
                self.tag_data[time].update({f.name:{}})
                logger.info(f"data for {f.name} taken at {time}")
                tag_position_X,tag_position_Y,tag_position_Z= vision[idx].get_translation()
                self.tag_data[time][f.name].update({'Position X':tag_position_X})
                self.tag_data[time][f.name].update({'Position Y':tag_position_Y})
                self.tag_data[time][f.name].update({'Position Z':tag_position_Z})

                tag_euler_angle=quat_to_Euler(vision[idx])
                self.tag_data[time][f.name].update({'Picth':tag_euler_angle.pitch})
                self.tag_data[time][f.name].update({'Roll':tag_euler_angle.roll})
                self.tag_data[time][f.name].update({'Yaw':tag_euler_angle.yaw})

            self.data['tag']={time:self.tag_data[time]}
            # logger.info(f"data for tags taken at {time}")

     

    def d_daq(self):
        """
            daq for digitizer data 
        """
        if self.digitizer.get_config():
            dose=list(self.digitizer.start())
            time=datetime.now().strftime("%m_%d_%Y_%H:%M:%S")
           
            # self.r_data[self.data_pts]=Data(time,dose)
            self.r_data[time]={}
            self.r_data[time].update({"mrem_p_h":dose[0]})
            self.r_data[time].update({"counts_per_second":dose[1]})
          
            self.r_data[time].update({"mrem":dose[2]})
            self.r_data[time].update({"duration":dose[3]})
            self.data['mirion']={time:self.r_data[time]}
            logger.info(f"data for mirion taken at {time}")
        else:
            logger.warning("port can't be accessed!!!")
            

        







    
