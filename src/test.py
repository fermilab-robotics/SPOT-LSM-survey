import bosdyn.client 
from bosdyn.client import util,create_standard_sdk
from bosdyn.client.util import authenticate
import argparse
import sys

def test(args):
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    options=parser.parse_args(args) 
    sdk=create_standard_sdk('test')
    robot=sdk.create_robot(options.hostname)
    authenticate(robot) 

if __name__=="__main__":
    print(sys.argv[1:])
    test(sys.argv[1:])
    print("test successed")
