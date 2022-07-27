import time
import datetime
import bosdyn.client 
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_id import RobotIdClient  
from bosdyn.client.frame_helpers import get_a_tform_b 
from bosdyn.client.frame_helpers import VISION_FRAME_NAME,ODOM_FRAME_NAME

#Robot Kinematic State with tranform snapshop & timestamp 
class KRobotState:@tag:notebookLayout
    def __init__(self,robot): 
        self._robot=robot
        self._robot_state_client=robot.ensure_client(RobotStateClient.default_service_name) 
        self.RobotState=self._robot_state_client.get_robot_state()
        self._transformSnapshot=None
        self._RobotTime=None 
    def getTransformSnapshot(self): 
        self._transformSnapshot= self.RobotState.kinematic_state().transforms_snapshot
        return  self._transformSnapshot
    def GetTimeStamp(self): 
        self._RobotTime=self.RobotState.kinematic_state().acquisition_timestamp
        return self._RobotTime 