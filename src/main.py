import sys
import argparse
from datetime import datetime
import time
import pickle

import bosdyn.client 
from bosdyn.client import util,create_standard_sdk
from bosdyn.client.util import authenticate

from localizations.spot import Spot
from localizations.april_tag import AprilTag
from digitizers.acr import Mirion
from digitizers.labjack import LabJack
from data_acquisitions.data_acquisition import DataAcquisition
from data_acquisitions.data_export import HEADERS,process_data

PORT='core-port'
robot_action="1.daq: walk the robot without exporting the data to csv after \n \
              2.exportData: only for exporting to csv data \n  3. walk the robot then export it to csv"
check_val=lambda w: w if w in ["Y","N","y","n"] else raise_(ValueError("wrong value"))

def raise_(exception):
    raise exception


def main(args):
    global file 
    # args 
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument('-r','--radMeter',help="choice of rad detector",choices=['mirion','LabJack'])
    parser.add_argument("-a","--action",help=robot_action,choices=["1","2","3"])
    options=parser.parse_args(args)

    #create robot obj.  & authenticate 
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot)
    robot.sync_with_directory() 


    #init all obj. import
    spot=Spot(robot)
    tag=AprilTag(robot)
    if not options.radMeter or options.radMeter=="Mirion": rad_detector=Mirion(port=PORT)
    if options.radMeter=="LabJack": rad_detector=LabJack() 
    #daq obj 
    data=DataAcquisition(spot,tag,rad_detector)

    #if action not specified, proceed with both walking the robot and export data 
    if options.action!=2:
        while True: 
            input("Press Enter when SPOT is ready..\n")
            data.bot_daq()
            data.tag_daq()
            data.d_daq()
            while True: 
                try:
                    walking=input ("Walking to the next tag? Y/N \n")
                    if check_val(walking): break 

                except ValueError():
                    print("please only pick Y or N")
            if walking=="Y" or walking=="y":
                continue
            else: 
                rad_detector.stop()
                file=datetime.datetime.now()
                pickle.dump(data,open(f"data_acquisitions/{file}","wb+"))
                # if user want data exported to csv 
                if options.action==1: 
                    process_data(file)
                    print("data exported at data/{file}.csv")
                
                print("exiting..")
    
    else: 
        #if user only wants to process collected data 
        pass 



               
            
            
           

    

if __name__=="__main__": 
    main(sys.argv[1:])
    


        
        

