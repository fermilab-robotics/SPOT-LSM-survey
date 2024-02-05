from abc import ABCMeta, abstractclassmethod

class Digitizer(metaclass=ABCMeta): 

    """
        All methods for digitizer 
    """
    def __init__(self):
        pass

    @abstractclassmethod
    def get_config(self):
        """
           setup configurations for the device 
        """
        pass

    @abstractclassmethod
    def start(self):
        """
            start device 
        """

    @abstractclassmethod
    def stop(self):
        """
            stop device 
        """
















