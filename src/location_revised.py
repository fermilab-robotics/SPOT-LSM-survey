from abc import ABCMeta
from collections import defaultdict


class Location():
    
    """ 
        meta class to establish location

        Args: robot: robot object from bosdyn API 
              data: dictionaries of data i.g: data[timestamp]={odom:xxx,vision:xxx} 
    """
    data=defaultdict(dict)

    def __init__(self,robot):
        self.robot=robot
    

    def Xformsnapshop(self): 
        """ 
            method for obtain transform snapshot 

            Args: 
        """
        

    def odomXform(self):
        """ 
            method for ODOM to BODY frames 

            Args: 
        """

    def visionXform(self): 
         """ 
            method for VISION to BODY frames 

            Args: 
        """

    def get_time(self):
        """ 
            get time stamps
            
            Args: 
        """

    def _run(self):
        """
            run command to pass start getting data. 
         
        """