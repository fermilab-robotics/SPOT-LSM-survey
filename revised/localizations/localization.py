from abc import ABCMeta, abstractclassmethod

class Localization(metaclass=ABCMeta): 

    """ 
        interface  to obtain localization data  
        Args : sdk robot    
    """
    def __init__(self,robot):
        self.robot=robot

    @abstractclassmethod
    def xformsnapshot(self):
        """
            transform snapshots to convert between frames 
        """
        pass 

    @abstractclassmethod
    def visionxform(self):
        """
            transform from VISION to BODY frames 
        """
        pass 

    @abstractclassmethod
    def odomxform(self):
        """
            transform from ODOM to BODY frames 
        """
        pass

    @abstractclassmethod 
    def get_time(self):
        """
            get timestamps
        """


    