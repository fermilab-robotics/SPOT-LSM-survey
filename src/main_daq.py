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

path=os.path.dirname(__file__)
path_to_file=os.path.join(path,"../src/data_acquisitions/data/official_data.csv")
path_to_temp=os.path.join(path,"../src/data_acquisitions/data/temp.csv")
path_to_header=os.path.join(path,"../src/data_acquisitions/data/headers.csv")


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
    daq_handler.d_daq()
    return daq_handler.data


def stop(data):
    """process obtained data"""
    spot_header=['spot_time','spot_vision','spot_vy','spot_vp','spot_vr']
    tag_header=None
    mirion_header=["mirion_time","mrem_p_h","counts_per_second","mrem","duration"]
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
        if obj=='mirion':
            mirion_time=list(data[obj].keys())[0]
            mirion_data=data[obj][mirion_time]
            mirion_data_arr=[mirion_time,*mirion_data.values()]
            mirion_data_to_be_written={h:d for h,d in zip(mirion_header,mirion_data_arr)}
            yield mirion_data_to_be_written



def teardownsession(packed_data):
    """ writting data """
    curr_headers= header_storage(path_to_header) 
    header_set = set(curr_headers) #set keeps header unique, non-retitive
    
    #write all data to temp file w/o header
    with open(path_to_temp,"a") as f:
        writer = csv.writer(f)
        for data in packed_data:
            for key in data.keys():
                #check key's existence in set
                if key not in header_set:
                    header_set.add(key)
                    curr_headers.append(key)
                #default to blank for header w/o data
            writer.writerow(data.get(key," ") for key in curr_headers) 
    f.close()

    #write headers of the current call to  the header file 
    write_headers_to_file(curr_headers,path_to_header) 

def finalize_csv(path_to_file,path_to_temp,path_to_header): 
    try: 
        headers=open(path_to_header,"r").readlines()[-1]
    except IndexError: 
        return 
    with open(path_to_file,"w+") as g:
        f=open(path_to_temp,"r")
        writer = csv.writer(g)
        g.write(headers+f.read())
         
    


def header_storage(path_to_header):
    f= open(path_to_header,"r").readlines() 
    headers= [] if not f else f[-1].strip().split(",")   #retrieve most updated header 
    return headers



def write_headers_to_file(headers_to_be_written,path_to_header): 
    with open(path_to_header,"a") as f:
        writer = csv.writer(f)
        writer.writerow(headers_to_be_written)
    f.close()




            
                
            

       


        
    

    






        
        

