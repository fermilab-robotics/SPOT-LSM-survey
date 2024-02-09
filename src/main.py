import sys
import argparse
import time

import bosdyn.client 
from bosdyn.client import util,create_standard_sdk
from bosdyn.client.util import authenticate

from localizations.spot import Spot
from localizations.april_tag import AprilTag
from digitizers.acr import Mirion
from data_acquisitions.data_acquisition import DataAcquisition

PORT='core-port'


def main(args):
    # args 
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    options=parser.parse_args(args)

    #create robot obj.  & authenticate 
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot)
    robot.sync_with_directory() 

    #init all obj. 
    spot=Spot(robot)
    tag=AprilTag(robot)
    rad_detector=Mirion(port=PORT)

    #daq obj 
    data=DataAcquisition(spot,tag,rad_detector)

    while True: 
        input("Press Enter to start..\n")
        data.bot_daq()
        data.tag_daq()
        data.d_daq()
        time.sleep()





if __name__=="__main__": 
    if not main(sys.argv[1:]):
        sys.exit(1)
