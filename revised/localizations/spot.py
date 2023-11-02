from bosdyn.api import robot_state_pb2, robot_state_service_pb2_grpc
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.frame_helpers import get_a_tform_b

from .localization import Localization 


class Spot(Localization):
    """ 
        SPOT the robot to obtain the localization itself 
    """ 

    def __init__(self,robot):
        super(Spot,self).__init__(robot)
        print('spot created ..')
    
    def xformsnapshot(self):
        """
            transform snapshots to convert between SPOT kinematic states 
            
            Returns: namespace transform_snapshot in SPOT state. 
        """
        self._robot_state_client=self.robot.ensure_client(RobotStateClient.default_service_name)
        self._robot_state=self._robot_state_client.get_robot_state()
        return self._robot_state
    
    def visionxform(self):
        """ 
            convert between SPOT kinematic VISION to BODY state

            Returns: 
        """
        key_frame="vision"
        return get_a_tform_b(self.xformsnapshot(),key_frame,"body")

    def odomxform(self):
        """
            transform from ODOM to BODY frames 
        """
        pass

    def get_time(self):
        """
            get timestamps
        """


    

