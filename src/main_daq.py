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
path_to_file=os.path.join(path,"../src/data_acquisitions/data/official_data.csv")
path_to_temp=os.path.join(path,"../src/data_acquisitions/data/temp.csv")
path_to_header=os.path.join(path,"../src/data_acquisitions/data/headers.csv")

_LOGGER = logging.getLogger(__name__)


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

    spot_header=['spot_time','spot_vision','spot_vy','spot_vp','spot_vr']
    tag_header=None
    mirion_header=["mirion_time","mrem_p_h","counts_per_sec"]

    # 

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
                mirion_data_arr=[mirion_time] + list(mirion_data.values())[:2] #slicing for only mrem_per_hour and cnt/sec
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
                    tag_header='tag_time',f'{tag}_vision',f'{tag}_vy',f'{tag}_vp',f'{tag}_vr'
                    fieldnames+=tag_header
                    tag_data_arr=[tag_time,*tags[tag].values()]
                    assert len(tag_header)==len(tag_data_arr), f"tag {tag} headers and values not equal"

                    tag_data_to_be_written={h:d for h,d in zip(tag_header,tag_data_arr)}
                    writer2=csv.DictWriter(file,fieldnames=fieldnames)
                    writer2.writeheader()
                    writer2.writerow(tag_data_to_be_written)
        
        file.write("\n") ## insert a blank line at the end of each daq
    
        file.close()
   


def teardownsession():
    """ writting data """
    temp=open(path_to_temp,'r').read().split("\n\n")
    file_name=None 

    data=defaultdict(dict)
    data_pnt=0
    field_headers=[]

    # treat each chunk of (spot,mirion,tag1,tag2,..) as a data_block for one data point
    # the first value of a data block will always be spot_time, this will be the time
    # we sttart taking data,  set this value to be our file name
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

    #write data to file
    assert file_name!=None, "file_name is NULL"
    path_to_file=os.path.join(path,f"../src/data_acquisitions/data/{file_name}")
    with open(path_to_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_headers)
        writer.writeheader()
        for d in data.values():
            writer.writerow(d)
        file.close()









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
    """ go thru header file to retrieve header with most items"""
    f= open(path_to_header,"r").readlines() 
    max_headers=0 
    if not f:
        return []
    for line in f:
        line.strip()
        if max_headers < max(max_headers,len(line.split(','))):
            max_headers= max(max_headers,len(line.split(',')))
            headers= line.split(",") 
    return headers



def write_headers_to_file(headers_to_be_written,path_to_header): 
    with open(path_to_header,"a") as f:
        writer = csv.writer(f)
        writer.writerow(headers_to_be_written)
    f.close()




            
                
            

       


        
    

    






        
        

