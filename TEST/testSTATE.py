import bosdyn.client.util
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot_state import RobotStateClient 
import argparse
import sys
sys.path.append('/workspaces/spot-dev-environment/')
from Robot_state import KRobotState

#test for time sync 
def TimeSyncTest(robot): 
    return robot.time_sync.wait_for_sync()
#test for getting the robot current state, output to a text file. 
def RobotStateTest(robot): 
    dummy= KRobotState(robot)
    with open("RobotstateReport.text",'w') as f:
        print(dummy.RobotState,file=f)
        f.close()
#test for Transform SnapShot GET method 
def XSnapShotTest(robot):
    dummy= KRobotState(robot) 
    print(dummy.getTransformSnapshot()) 


      



    
def main(argv):
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    options=parser.parse_args(argv)
    #create robot object to invoke SPOT    
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)
    #TimeSyncTest(robot)
    #RobotStateTest(robot)
    XSnapShotTest(robot)


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)


    


    







