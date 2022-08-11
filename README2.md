# Localized LSM Data Acquisition 
This is the repository for SPOT localtization test refactored, combined with the data acquisition code for the digitized Log Survery Meter(LSM)

## SPOT Frame 
We acquire SPOT's location in its Odom and Vision Frame. These data will then be transformed to SPOT's body frame. Information about SPOT's Geometry and Frames: <https://dev.bostondynamics.com/docs/concepts/geometry_and_frames> 

## April Tag 
SPOT is capable of detecting AprilTag using robot's base cameras and retrive the data into its object frame. AprilTag is fiducial object that SPOT uses as ground truth reference object. Data obtained from object frame as AprilTag is detected will also be then transformed to robot's body frame 

## Localization Test Goal 
The entire purpose of initialize SPOT localization is  


## Repository Code Component
This repository is made up from the following code components: 
    1. Robot_state.py: this module is used to obtain the current robot state 
    2. Location.py:this module method to obtain the Robot location, establish April Tag requests
    3.Main:   


