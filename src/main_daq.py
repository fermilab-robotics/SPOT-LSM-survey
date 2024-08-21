#!/usr/bin/env python3
import argparse
import os
import csv 

import bosdyn.client 
from bosdyn.client import create_standard_sdk
from bosdyn.client.util import authenticate

from localizations.spot import Spot
from localizations.april_tag import AprilTag
from digitizers.acr import Mirion
from data_acquisitions.data_acquisition import DataAcquisition





def establish_session(args):
    parser=argparse.ArgumentParser(args)
    bosdyn.client.util.add_base_arguments(parser)
    options=parser.parse_args(args)
    sdk=create_standard_sdk('spot_lsm_server')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot)
    robot.sync_with_directory()    
    return robot

def main_daq(robot):
    #init all obj. import
    spot=Spot(robot)
    tag=AprilTag(robot)
    rad_detector=Mirion(port="/dev/ttyACM0")
    daq_handler=DataAcquisition(spot,tag,rad_detector)
    return daq_handler

def tick(daq_handler): 
    daq_handler.bot_daq()
    daq_handler.tag_daq()
    return daq_handler.data


def stop(data):
    """process obtained data"""
    spot_header=['spot_time','spot_vision','spot_vy','spot_vp','spot_vr']
    tag_header=None
    for obj in data:
        if obj=="spot":
            spot_time=list(data[obj].keys())[0]
            # print(f'spot time: {spot_time}')
            spot_local=data[obj][spot_time]
            spot_data_arr=[spot_time,*spot_local.values()]
            spot_data_to_be_written={h:d for h,d in zip(spot_header,spot_data_arr)}
            yield spot_data_to_be_written
            
        if obj=="tag":
            tag_time=list(data[obj].keys())[0]
            # print(f'tag_time: {tag_time}')
            tags=data[obj][tag_time]
            tag_names=[tags.keys()]
            for tag in tags:
                tag_header='tag_time',f'{tag}_vision',f'{tag}_vy',f'{tag}_vp',f'{tag}_vr'
                tag_data_arr=[tag_time,*tags[tag].values()]
                tag_data_to_be_written={h:d for h,d in zip(tag_header,tag_data_arr)}
                yield tag_data_to_be_written


def teardownsession(packed_data):
    path=os.path.dirname(__file__)
    path_to_file=os.path.join(path,"../src/data_acquisitions/data/official_data.csv")
    path_to_temp=os.path.join(path,"../src/data_acquisitions/data/temp.csv")
    header, header_set = [], set() #dynamic header for different no. of tags each daq
    #write all data to temp file w/o header
    with open(path_to_temp,"w+") as f:
        writer = csv.writer(f)
        writer.writerow(" ")
        for data in packed_data:
            for key in data:
                if key not in header_set:
                    header_set.add(key)
                    header.append(key)
            writer.writerow(data.get(key," ") for key in header) 
    f.close()
    #append header, write data to offical daq file
    with open(path_to_file,"w+") as g:
        f=open(path_to_temp,"r")
        writer = csv.writer(g)
        g.write(','.join(header)+f.read())
         
    









            
                
            

       


        
    

    



   
    
    # else: 
    #     # rad_detector.stop()
    #     file=input("name file? \n")
    #     file_path = os.path.dirname(__file__)
    #     with open(os.path.join(file_path,f"data_acquisitions/data/{file}.json"),"w+") as f: 
    #         json.dump(d.data,f,default=lambda o: o.__dict__,indent=4)
                   
                # if user wants data exported to csv after walking the robot
                # if options.action!="1": 
                #     process_data(f'{file}.json')
                   
        # print("exiting..")
                # break
    
   





        
        

