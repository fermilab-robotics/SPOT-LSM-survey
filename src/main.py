#!/usr/bin/env python3

import sys
import os
import argparse
import time
import json

import bosdyn.client 
from bosdyn.client import util,create_standard_sdk
from bosdyn.client.util import authenticate

from localizations.spot import Spot
from localizations.april_tag import AprilTag
from digitizers.acr import Mirion
# from digitizers.labjack import LabJack
from data_acquisitions.data_acquisition import DataAcquisition
from data_acquisitions.data_export import HEADERS,process_data

robot_action="1.daq: walk the robot without exporting the data to csv after \n \
              2.exportData: only for processing obtained raw to csv data \n  3. walk the robot then export data to csv"
is_walking=lambda w: w if w in ["Y","N","y","n"] else False



def main(args):
    global file 
    # args 
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument('-r','--radMeter',default='Mirion',nargs='?',help="choice of rad detector",choices=['Mirion','LabJack'])
    parser.add_argument("-a","--action",help=robot_action,choices=["1","2","3"])
    options=parser.parse_args(args)
    print(options)

    #create robot obj.  & authenticate 
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot)
    robot.sync_with_directory()    

    #init all obj. import
    spot=Spot(robot)
    tag=AprilTag(robot)
    if not options.radMeter or options.radMeter=="Mirion": rad_detector=Mirion(port="/dev/ttyACM0")
    # if options.radMeter=="LabJack": rad_detector=LabJack() 
    # #daq obj 
    d=DataAcquisition(spot,tag,rad_detector)

    # #if action not specified, proceed with both walking the robot and export data 
    if not options.action or options.action!="2" :
        while True: 
            input("Press Enter when SPOT is ready..\n")
            d.bot_daq()
            d.tag_daq()
            d.d_daq()
            

            walking=input ("Walking to the next tag? Y/N \n")
            if not is_walking(walking) or is_walking(walking) in ['N','n']: 
                break 

            elif walking=="Y" or walking=="y":
                time.sleep(1)
                continue

            else: 
                rad_detector.stop()
                file=input("name file? \n")
                file_path = os.path.dirname(__file__)
                with open(os.path.join(file_path,f"data_acquisitions/data/{file}.json"),"w+") as f: 
                    json.dump(d.data,f,default=lambda o: o.__dict__,indent=4)
                   
                # if user wants data exported to csv after walking the robot
                if options.action!="1": 
                    process_data(f'{file}.json')
                   
                print("exiting..")
                break
    
    else: 
        print("Entering option to only process data")
        #if user only wants to process collected data 
        path=os.path.join(os.path.dirname(__file__),"data_acquisitions/data/")
        all_files=os.listdir(path)
        unprocessed_files=list(filter(lambda f:f.endswith(".json"),all_files))
        
        #prompt user to choose file to be processed
        user_options= None
        while user_options not in ["1","2"]:
            user_options=input("1.Proceed with the latest file in the folder \n2. List all files\n")

        #latest file option 
        if user_options=="1": 
            latest_file = max([(file, os.path.getctime(path+file)) \
                               for file in unprocessed_files],key=lambda x:x[-1])[0]
            process_data(latest_file)
        
        #list all files option
        else: 
            for file_number,file in enumerate(unprocessed_files): 
                print(f"option {file_number} : {file}")
            
            file_input=None
            while file_input not in list(range(len(unprocessed_files))):
                file_input= input("Choose a file number?\n")
                file_input=int(file_input)
            
            process_data(unprocessed_files[file_input])




if __name__=="__main__": 
    if not main(sys.argv[1:]):
        sys.exit(1)
    


        
        

