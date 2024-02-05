from bosdyn.client.world_object import WorldObjectClient 
from bosdyn.api import world_object_pb2


"""
    Request fiducial objects

""" 
def fiducial_req(world_object_client):
    req=[world_object_pb2.WORLD_OBJECT_APRILTAG]
    fiducial_obj=world_object_client.list_world_objects(object_type=req).world_objects
    return fiducial_obj[0]


