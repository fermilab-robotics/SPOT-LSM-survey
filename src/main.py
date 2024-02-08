import sys
import argparse

import bosdyn.client 
from bosdyn.client import util,create_standard_sdk
from bosdyn.client.util import authenticate

from localizations.spot import Spot

def main(args):
    parser=argparse.ArgumentParser()
    
    bosdyn.client.util.add_base_arguments(parser)

    options=parser.parse_args(args)

    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot)
    robot.sync_with_directory() 

    spot=Spot(robot)
    xformsnapshot=spot.xformsnapshot()
    print(xformsnapshot)


if __name__=="__main__": 
    if not main(sys.argv[1:]):
        sys.exit(1)
