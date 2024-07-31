from time import ctime

from bosdyn.api import world_object_pb2
from bosdyn.client.world_object import WorldObjectClient 
from bosdyn.client.frame_helpers import get_a_tform_b,VISION_FRAME_NAME,ODOM_FRAME_NAME


from .localization import Localization
from .fiducial_request import fiducial_req

class AprilTag(Localization):
    """
        Localization test from April Tags  
    """

    def __init__(self,robot):
        super(AprilTag,self).__init__(robot)
        print('April Tag created..')
        self.world_object_client=self.robot.ensure_client(WorldObjectClient.default_service_name)
        self.fiducial=fiducial_req(self.world_object_client)


    
    def xformsnapshot(self):
        """
            transform snapshots to convert between April Tag's kinematic states
        """
        snapshot=[]
        if not self.fiducial: 
            print('No tag found')
        for f in self.fiducial: 
            snapshot.append(f.transforms_snapshot)
        return snapshot 
        
    def visionxform(self):
        """ 
            convert between April tag kinematic VISION to BODY state
    
        """
        key_frame=VISION_FRAME_NAME
        vision=[]
        if not self.fiducial: 
            print("no tag detected. try again")
        else: 

            for xform,f in zip(self.xformsnapshot(),self.fiducial):
                tag_vision=get_a_tform_b(xform,key_frame,f.apriltag_properties.frame_name_fiducial)
                vision.append(tag_vision)
            return vision 

        # if self.fiducial:
        #     body_frame=self.fiducial.apriltag_properties.frame_name_fiducial
        #     return get_a_tform_b(self.xformsnapshot(),key_frame,body_frame)
        
        
        
    def odomxform(self):
        """
            convert between April tag kinematic VISION to BODY state
        """
        key_frame=ODOM_FRAME_NAME
        odom=[]
        if not self.fiducial: 
            print("no tag detected. try again")
        else: 

            for xform,f in zip(self.xformsnapshot(),self.fiducial):
                tag_odom=get_a_tform_b(xform,key_frame,f.apriltag_properties.frame_name_fiducial)
                odom.append(tag_odom)
            return odom


        # if self.fiducial:
        #     body_frame=self.fiducial.apriltag_properties.frame_name_fiducial
        #     return get_a_tform_b(self.xformsnapshot(),key_frame,body_frame)
        # else: 
        #     print("no tag detected. try again")
    
    def get_time(self):
        """
            get tag time 
        """
        time=self.fiducial[0].acquisition_time.seconds
        return ctime(time)





        
    



