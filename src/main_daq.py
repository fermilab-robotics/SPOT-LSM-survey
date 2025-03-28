#!/usr/bin/env python3
import argparse
import os
import csv 
import logging
from collections import defaultdict

import bosdyn.client 
from bosdyn.client import create_standard_sdk
from bosdyn.client.util import authenticate

from localizations.spot import Spot
from localizations.april_tag import AprilTag
from digitizers.acr import Mirion
from data_acquisitions.data_acquisition import DataAcquisition

path=os.path.dirname(__file__)
path_to_data_dir=os.path.join(path,"../src/data_acquisitions/data/")
path_to_temp=os.path.join(path,"../src/data_acquisitions/data/history.csv")

_LOGGER = logging.getLogger(__name__)


def establish_session(args):
    """ routine to handle sdk & spot object to call API """
    parser=argparse.ArgumentParser(args)
    bosdyn.client.util.add_base_arguments(parser)
    options=parser.parse_args(args)
    sdk=create_standard_sdk('spot_lsm_server')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot)
    robot.sync_with_directory()    
    return robot

def main_daq(robot):
    spot=Spot(robot)
    tag=AprilTag(robot)
    rad_detector=Mirion(port="/dev/ttyACM0")
    daq_handler=DataAcquisition(spot,tag,rad_detector)
    return daq_handler

def tick(daq_handler): 
    
    """Taking data"""

    logger=_LOGGER
    # spot data
    daq_handler.bot_daq()
    #mirion data 
    if not daq_handler.digitizer.get_config():
        logger.warning("no digitizer found!!")
    else:
        daq_handler.d_daq()
    #apriltag data
    if not daq_handler.tag.fiducial:
        logger.warning("no tag found!!")
    else:
        daq_handler.tag_daq()
    
    return daq_handler.data


def stop(data):

    """process obtained data"""

    spot_header=['Timestamp','Position X','Position Y','Position Z','Pitch','Roll','Yaw']
    tag_header=None
    mirion_header=["Radiation(mrem/h)","Radiation(counts/sec)"]
    logger=_LOGGER
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    with open(path_to_temp,'a+') as file: 
        fieldnames=[]
        for obj in data:
            if obj=="spot":
                spot_time=list(data[obj].keys())[0]
                spot_local=data[obj][spot_time]
                spot_data_arr=[spot_time,*spot_local.values()]
                assert len(spot_header)==len(spot_data_arr), "spot headers -values not equal"

                fieldnames+=spot_header
                spot_data_to_be_written={h:d for h,d in zip(spot_header,spot_data_arr)}
                writer=csv.DictWriter(file,fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(spot_data_to_be_written)
            
            if obj=='mirion':
                mirion_time=list(data[obj].keys())[0]
                mirion_data=data[obj][mirion_time]
                mirion_data_arr= list(mirion_data.values())[:2] #slicing for only mrem_per_hour and cnt/sec
                assert len(mirion_header)==len(mirion_data_arr), "mirion headers-values not equal"

                fieldnames+=mirion_header
                mirion_data_to_be_written={h:d for h,d in zip(mirion_header,mirion_data_arr)}
                writer1=csv.DictWriter(file,fieldnames=fieldnames)
                writer1.writeheader()
                writer1.writerow(mirion_data_to_be_written)
                
            if obj=="tag":
                tag_time=list(data[obj].keys())[0]
                tags=data[obj][tag_time]
                tag_names=[tags.keys()]
                for tag_idx,tag in enumerate(tags):
                    tag_header=f'{tag}_Position_X',f'{tag}_Position_Y',f'{tag}_Position_Z',f'{tag}_Pitch',f'{tag}_Roll',f'{tag}_Yaw'
                    fieldnames+=tag_header
                    # logger.debug(f'tag header: {tag_header}')
                    tag_data_arr=[*tags[tag].values()]
                    # logger.debug(f'tag data: {tag_data_arr}')
                    assert len(tag_header)==len(tag_data_arr), f"{tag} headers w len {len(tag_header)} isn't equal {len(tag_data_arr)}"

                    tag_data_to_be_written={h:d for h,d in zip(tag_header,tag_data_arr)}
                    writer2=csv.DictWriter(file,fieldnames=fieldnames)
                    writer2.writeheader()
                    writer2.writerow(tag_data_to_be_written)
        
        file.write("\n") ## insert a blank line at the end of each daq
    
        file.close()
   


def teardownsession():
    """ writting data """
    temp=open(path_to_temp,'r').read().strip().split("\n\n")
    file_name=None 
    data=defaultdict(dict)
    data_pnt=0
    field_headers=[]
   
    # treat each chunk of (spot,mirion,tag1,tag2,..) as a data_block for one data point
    # the first value of a data block will always be spot_time, this will be the time
    # we start taking data,  set this value to be our file name
    for data_block in temp:
        chunk_data=defaultdict(str)
        for header_line,value_line in zip(data_block.split("\n")[::2],data_block.split("\n")[1::2]): 
            for h,v in zip(header_line.split(","),value_line.split(",")):
                
                if h not in set(field_headers): 
                    field_headers.append(h)
                if v: 
                    chunk_data[h]=v
                    file_name=v if not file_name else file_name 

        data[data_pnt]=chunk_data
        data_pnt+=1
        

    # write data to official file whose name is the first timestamp of the data acquisition session
    assert file_name!=None, "file_name is NULL"
    path_to_file=os.path.join(path,f"../src/data_acquisitions/data/{file_name}.csv")
    with open(path_to_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_headers)
        writer.writeheader()
        for d in data.values():
            writer.writerow(d)
        file.close()









         
    








            
                
            

       


        
    

    






        
        

