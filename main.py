import time
import datetime
import sys
import bosdyn.client 
import bosdyn.client.util
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_id import RobotIdClient  
from bosdyn.client.frame_helpers import get_a_tform_b 
from bosdyn.client.frame_helpers import VISION_FRAME_NAME,ODOM_FRAME_NAME
from bosdyn.client.world_object import WorldObjectClient 
from bosdyn.api import world_object_pb2
from Robot_state import KRobotState 
from Location import * 
from U3digitizer import *
import argparse
import pickle  

def main(argv):
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    #parser.add_argument('--vs',action='store_true',default=False)
    options=parser.parse_args(argv)
#create robot object to invoke SPOT    
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    #robot.authenticate(options.username, options.password)

#time sync 
    robot.time_sync.wait_for_sync() 
#create object to obtain Location Data
    robot_localization= RobotLocation(robot)
    fiducial_localization= AprilTag(robot)
#create object for U3 digitizer 
    U3device=Digitizer(u3.U3(debug=True))

#log robot info 
    
    try: 
        
        input('Press Enter to log robot and fiducial positions...')
        robot_localization.start()
        fiducial_localization.start()
        U3device.start()
        with open('RobotData.pickle','wb') as Robotfile: 
            pickle.dump(robot_localization, Robotfile)
        with open('TagData.pickle','wb') as Tagfile: 
            pickle.dump(fiducial_localization, Tagfile)
        with open('LSmdata.pickle','wb') as Digitizerfile: 
            pickle.dump(U3device, Digitizerfile)
    except KeyboardInterrupt: 
        Robotfile.close()
        Tagfile.close()
        Digitizerfile.close() 
        print("Caught Keyboard Interupt, exitting")
        

def Datareport(robotfile,tagfile,lsmfile):
'''Each of these data load contains 3 list fromOdom, fromVision, TimeStamp'''
    RobotLoad=pickle.load(open(robotfile,'rb'))
    TagLoad=pickle.load(open(tagfile,'rb'))
    LSMLoad=pickle.load(open(lsmfile,'rb'))
    Robotdata= RobotLoad.__dict__   #pickle load stores data as dictionary
    Tagdata=TagLoad.__dict__
    LSMdata= LSMLoad.__dict__
    i=0
    f=open('report.csv','w')
    f.write('From ODOM')
    while i<len(Robotdata['TimeStamp']): 
        f.write(Robotdata['fromOdom'][i])
        i+=1
    



    

         



     


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
