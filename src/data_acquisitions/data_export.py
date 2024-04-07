#!/usr/bin/env python3

import os
import json 
from csv import DictWriter
from collections import defaultdict


from .data_analysis import spot_data,tag_data



HEADERS=[
        "data points",
        "rad time","rad dose",
        "spot time",
        "spot vision x","spot vision y", "spot vision z",
        "spot vision yaw","spot vision pitch","spot vision roll",
        "tag time",
        "tag vision x","tag vision y","tag vision z",
        "tag vision yaw","tag vision pitch","tag vision roll",
    ]


def process_data(file):
    cur_path = os.path.dirname(__file__)
    with open(os.path.join(cur_path,f"./data/{file}"),"rb") as f: 
        daq=json.load(f)

    file=file.split('.')[0] #get file name
    csv_file=open(os.path.join(cur_path,f"./data/{file}.csv"),"w+")
    writer=DictWriter(csv_file,fieldnames=HEADERS)
    writer.writeheader()

    for d in daq: 
        pending_data=defaultdict(float)
        pending_data={k:0.0 for k in HEADERS}
        pending_data["data points"]=d
        
        if daq[d]["mirion"]:
            mirion_data=daq[d]["mirion"]
            for md in mirion_data:
                pending_data["rad time"]=md 
                pending_data["rad dose"]=mirion_data[md]["mrem"]


        if daq[d]["spot"]: 
            spot_data(daq[d]["spot"],pending_data)
        
            
        if daq[d]["tag"]:
            tag_data(daq[d]["tag"],pending_data)
        
        # write data 
        writer.writerow(pending_data)
    
    print(f"data exported at data/{file}.csv")




#debugging only
if __name__=="__main__":
    process_data("test.json")


           





        

    






