from bosdyn.client.math_helpers import quat_to_eulerZYX
from collections import namedtuple


Frames = namedtuple('frame', ['yaw','pitch','roll'])


def spot_data(data:dict,result:dict)->None:

    """"
        analyze Spot's localization data
    """
    result["spot time"]=data['vision'].time
    result["spot vision x"]=data['vision'].data.x
    result["spot vision y"]=data['vision'].data.y
    result["spot vision x"]=data['vision'].data.z
    result["spot vision yaw"]=quat_to_Euler(data['vision'].data).yaw
    result["spot vision pitch"]=quat_to_Euler(data['vision'].data).pitch
    result["spot vision roll"]=quat_to_Euler(data['vision'].data).roll
    result["spot odom x"]=data['odom'].data.x
    result["spot odom y"]=data['odom'].data.y
    result["spot odom z"]=data['odom'].data.z
    result["spot odom yaw"]=quat_to_Euler(data['odom'].data).yaw
    result["spot odom pitch"]=quat_to_Euler(data['odom'].data).pitch
    result["spot odom roll"]=quat_to_Euler(data['odom'].data).roll


def tag_data(data:dict,result:dict)->None:
    """
        analyze tag data 
    """
    result["tag time"]=data['vision'].time
    result["tag vision x"]=data['vision'].data.x
    result["tag vision y"]=data['vision'].data.y
    result["tag vision x"]=data['vision'].data.z
    result["tag vision yaw"]=quat_to_Euler(data['vision'].data).yaw
    result["tag vision pitch"]=quat_to_Euler(data['vision'].data).pitch
    result["tag vision roll"]=quat_to_Euler(data['vision'].data).roll
    result["tag odom x"]=data['odom'].data.x
    result["tag odom y"]=data['odom'].data.y
    result["tag odom z"]=data['odom'].data.z
    result["tag odom yaw"]=quat_to_Euler(data['odom'].data).yaw
    result["tag odom pitch"]=quat_to_Euler(data['odom'].data).pitch
    result["tag odom roll"]=quat_to_Euler(data['odom'].data).roll



def quat_to_Euler(frame):
    """
        method to convert Quaternions to Euler Angles
    """

    rot=quat_to_eulerZYX(frame.rot)
    return Frames(rot[0],rot[1],rot[2])