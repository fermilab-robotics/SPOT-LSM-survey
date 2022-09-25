import bosdyn.client.util
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot_state import RobotStateClient 
import argparse
import sys
from bosdyn.client.frame_helpers import get_a_tform_b 
from bosdyn.client.frame_helpers import VISION_FRAME_NAME,ODOM_FRAME_NAME
sys.path.append('/workspaces/spot-dev-environment/')
from Location import *


#test for Odom to Body frame transformation 
def RobotOdomXform(robot): 
    dummy=Location(robot) 
    dummy.OdomTransform()
    print(dummy.fromOdom)
#test for Robot Location all steps 
def RobotLocationTest(robot): 
    dummy=RobotLocation(robot)
    dummy.start() #start obtaining data 
    print(f'{dummy.fromOdom}\n{dummy.fromVision}\n{dummy.Time}')
#test requesting Apriltag 
def TagRequestTest(robot): 
    dummy=AprilTag(robot)
    #dummy.AprilOdomTransform()
    #dummy.AprilVisionTransform()
    #print(dummy.fromOdom)
    #print(dummy.fromVision)
    dummy.start()
    print(f'{dummy.fromOdom}\n{dummy.fromVision}\n')












def main(argv): 
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    options=parser.parse_args(argv) 
    #create robot object to invoke SPOT    
    sdk=create_standard_sdk('Location Test')
    robot=sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)
    #all tests 
    #RobotOdomXform(robot)
    #RobotLocationTest(robot)
    TagRequestTest(robot)


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)






