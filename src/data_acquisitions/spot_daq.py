from bosdyn.client import util,create_standard_sdk
from bosdyn.client.util import authenticate

import argparse
import sys

sys.path.append("/home/lpham/CODE/SPOT-LSM-survey/src/")
from localizations.spot import Spot


def spot_data(robot): 
    # parser=argparse.ArgumentParser()
    # util.add_base_arguments(parser)
    # options=parser.parse_args()
    
    #sdk basic
    # sdk=create_standard_sdk('test')
    # robot=sdk.create_robot(options.hostname)
    # authenticate(robot)

    spot=Spot(robot)
    result=spot.visionxform().get_translation()

    
    
    with open("test.txt","a+") as f:
        print("writting result to file")
        f.write(f' {result.__repr__()} \n')
   
    
    

# if __name__=="__main__":
#     spot_data()

