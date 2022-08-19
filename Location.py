import time
import datetime
import bosdyn.client 
from bosdyn.client import create_standard_sdk
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_id import RobotIdClient  
from bosdyn.client.frame_helpers import get_a_tform_b 
from bosdyn.client.frame_helpers import VISION_FRAME_NAME,ODOM_FRAME_NAME
from bosdyn.client.world_object import WorldObjectClient 
from bosdyn.api import world_object_pb2
from Robot_state import KRobotState

#Location data with methods for tranforming from SPOT's Odom and Vision frames
class Location():
    fromOdom=[]
    fromVision=[]
    Time=[]
    def __init__(self,robot,ToFrame="body"):
        self.RoboOBJ=KRobotState(robot)
        self.robot_state=self.RoboOBJ.RobotState
        self.FromFrame=None 
        self.ToFrame=ToFrame
        self.TransformSnapshot=None
        self.fiducial_objects=None
    def OdomTransform(self): 
        if  self.fiducial_objects!= None:
            self.FromFrame=ODOM_FRAME_NAME
        else:
            self.FromFrame="odom"
            self.TransformSnapshot=self.RoboOBJ.getTransformSnapshot()
            odom=get_a_tform_b(self.TransformSnapshot,self.FromFrame,self.ToFrame)
            self.fromOdom.append(odom)
         
    def VisionTransform(self): 
        if  self.fiducial_objects!= None:
            self.FromFrame=VISION_FRAME_NAME
        else: 
            self.FromFrame="vision"
            vision=get_a_tform_b(self.TransformSnapshot,self.FromFrame,self.ToFrame)
            self.fromVision.append(vision)
    def TimeStamp(self): 
        self.Time.append(self.RoboOBJ.GetTimeStamp())
        
#robot location data 
class RobotLocation(Location):
    def __init__(self,robot):
       super().__init__(robot) 
    def start(self): 
      self.OdomTransform()
      self.VisionTransform()
      self.TimeStamp()

#april tag location data 
class AprilTag(Location): 
    def __init__(self,robot):
        self.world_object_client=robot.ensure_client(WorldObjectClient.default_service_name)
        self.fiducial_objects=None
        self.ToFrame= None 
        super().__init__(robot)
    #request Tag
    def RequestFiducial(self): 
        request_fiducials=[world_object_pb2.WORLD_OBJECT_APRILTAG]
        self.fiducial_objects=self.world_object_client.list_world_objects(object_type=request_fiducials).world_objects
        return self.fiducial_objects
    def AprilOdomTransform(self): 
        if  self.fiducial_objects != None:
            super().OdomTransform()
            for fiducial in self.fiducial_objects:
                self.ToFrame=fiducial.apriltag_properties.frame_name_fiducial
                self.TransformSnapshot= fiducial.transforms_snapshot
                odom=get_a_tform_b(self.TransformSnapshot,super().FromFrame,self.ToFrame) 
                self.fromOdom.append(odom) 
    def AprilVisionTransform(self): 
        if  self.fiducial_objects != None:
            super().VisionTransform()
            for fiducial in self.fiducial_objects:
                self.ToFrame=fiducial.apriltag_properties.frame_name_fiducial
                self.TransformSnapshot= fiducial.transforms_snapshot
                vision=get_a_tform_b(self.TransformSnapshot,super().FromFrame,self.ToFrame)
                self.fromOdom.append(vision)    
    def TagTime(self):
        self.Time.append(datetime.datetime.now()) 
    def start(self): 
        self.RequestFiducial()
        self.AprilOdomTransform()
        self.AprilVisionTransform()
        self.TagTime()

           

