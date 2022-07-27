import time
import datetime
import bosdyn.client 
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_id import RobotIdClient  
from bosdyn.client.frame_helpers import get_a_tform_b 
from bosdyn.client.frame_helpers import VISION_FRAME_NAME,ODOM_FRAME_NAME
from bosdyn.client.world_object import WorldObjectClient 
from bosdyn.api import world_object_pb2
from Robot_state import KRobotState 
from Location import * 
import argparse
import pickle  

def main(argv):
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_common_arguments(parser)
    parser.add_argument('--vs',action='store_true',default=False)
    options=parser.parse_args(argv)
#create robot object to invoke SPOT    
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.host_name)
    robot.authenticate(options.username, options.password)
#time sync 
    robot.time_sync.wait_for_sync() 
#create object to obtain Location Data
    robot_localization= RobotLocation(robot)
    fiducial_localization= AprilTag(robot)
#log robot info 
    
    try: 
        while True: 
            input('Press Enter to log robot and fiducial positions...')
            robot_localization.start()
            fiducial_localization.start()
            with open('RobotData.pickle','wb') as Robotfile: 
                pickle.dump(robot_localization, Robotfile)
            with open('TagData.pickle','wb') as Tagfile: 
                pickle.dump(fiducial_localization, Tagfile)

    except KeyboardInterrupt: 
        print("Caught Keyboard Interupt, exitting")
        return True 