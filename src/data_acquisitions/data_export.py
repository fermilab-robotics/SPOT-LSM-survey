import os
import pickle
from csv import DictWriter
from collections import defaultdict,namedtuple


from data_analysis import spot_data,tag_data



HEADERS=[
        "data points",
        "rad time","rad dose",
        "spot time",
        "spot vision x","spot vision y", "spot vision z",
        "spot vision yaw","spot vision pitch","spot vision roll",
        "spot odom x","spot odom y","spot odom z",
        "spot odom yaw","spot odom pitch","spot odom roll",
        "tag time",
        "tag vision x"," tag vision y"," tag vision z",
        "tag vision yaw","tag vision pitch","tag vision roll",
        "tag odom x","tag odom y", "tag odom z",
        "tag odom yaw","tag odom pitch","tag odom roll",   
    ]

cur_path = os.path.dirname(__file__)

def process_data(file):
    processed=[]
    daq=pickle.load(open(file,"rb"))
    data_points=daq.bot_data.keys()
    writer=DictWriter(open(os.path.join(cur_path,f"./data/{file}.csv")))

    for d in data_points: 
        pending_data=defaultdict(float)
        pending_data={k:0.0 for k in HEADERS}
        pending_data["data points"]=d
        
        if daq.r_data[d]: 
            pending_data["rad time"]=daq.r_data[d].time
            pending_data["rad dose"]=daq.r_data[d].data

        if daq.bot_data[d]:spot_data(daq.bot_data[d],pending_data)
            
        if daq.tag_data[d]:tag_data(daq.tag_data[d],pending_data)
        #write data 
        writer.writeheader()
        writer.writerow(pending_data)


           





        

    






