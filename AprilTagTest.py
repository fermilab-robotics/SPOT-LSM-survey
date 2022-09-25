import argparse
import sys
import bosdyn.client
import bosdyn.client.util
from  bosdyn.client.world_object import WorldObjectClient 
from bosdyn.api import world_object_pb2

def main(argv): 
    #CLI 
    parser=argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser) 
    options=parser.parse_args(argv) 
    # create robot object + authentication
    sdk=bosdyn.client.create_standard_sdk('april_tag_client') 
    robot=sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)
    #create world obj. client for April Tag service 
    world_object_client=robot.ensure_client(WorldObjectClient.default_service_name)
    #requets April Tag 
    request_Tag=[world_object_pb2.WORLD_OBJECT_APRILTAG]
    fiducial_objects=world_object_client.list_world_objects(object_type=request_Tag).world_objects 
    print(fiducial_objects) 

if __name__=='__main__':
    if not main(sys.argv[1:]):
        sys.exit(1) 







