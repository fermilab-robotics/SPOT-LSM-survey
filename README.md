# SPOT localization test refactored
This is the repository for SPOT localtization test refactored. It follows the guideline for SPOT's development environment set up at: <https://github.com/fermilab-robotics/spot-dev-environment> 

## SPOT Frames 
SPOT's location data is acquired in Odom and Vision Frames which are the two inertial frames of the robot.
Information about SPOT's Geometry and Frames: <https://dev.bostondynamics.com/docs/concepts/geometry_and_frames> 

## April Tag 
AprilTag is a visual fiducial system. SPOT SDK includes modules(e.g:```world_object``` in the client library) that allow the implementation of AprilTag as raw data that assists with the establishing of waypoints. 

SPOT forms its localization via a system of waypoints and edges. Waypoints define named locations in the world, and edges define how to get from one waypoint to another. 

SPOT is capable of detecting AprilTags using its base cameras and retrieve the data into the object frame and will be treated as the ground truth reference object. The Tag plays an essential roles in assiting SPOT navigate through the world in a metrically consistent manner. 

## Localization Test Goal 



## Repository Code Component
This repository is made up from the following code components: 
1. Robot_state.py: this module is used to obtain the current robot state 
2. Location.py:this module includes method to obtain the Robot location, and establish April Tag requests
3. Main: all the necessary operations needed to obtain localization data from SPOT and serializing obtained data is included here.   


