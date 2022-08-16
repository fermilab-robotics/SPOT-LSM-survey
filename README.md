# SPOT localization test refactored
This is the repository for SPOT localtization test refactored. It follows the guideline for SPOT's development environment set up at: <https://github.com/fermilab-robotics/spot-dev-environment> 

## SPOT Frames 
SPOT's location data is acquired in its Odom and Vision Frame. These data will then be transformed to SPOT's body frame. 
Information about SPOT's Geometry and Frames: <https://dev.bostondynamics.com/docs/concepts/geometry_and_frames> 

## April Tag 
SPOT is capable of detecting AprilTag using robot's base cameras and retrieve the data into its object frame. AprilTag is a fiducial object that SPOT uses as ground truth reference object. Data obtained from object frame as AprilTag is detected will also be then transformed to SPOT's body frame 

## Localization Test Goal 
SPOT localizes itself via a system of points and edges. 
To be continued... 

## Repository Code Component
This repository is made up from the following code components: 
    1. Robot_state.py: this module is used to obtain the current robot state 
    1. Location.py:this module includes method to obtain the Robot location, and establish April Tag requests
    1.Main: all the necessary operations needed to obtain localization data from SPOT and serializing obtained data is included here.   


