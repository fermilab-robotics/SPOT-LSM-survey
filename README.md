# LSM READ WITH SPOT LOCALIZATION DATA 
This repository includes the code to obtain the Log Survey Meter(LSM) data with defined locations taken from the  SPOT's localization test. The repository contains two main parts: 
1. SPOT localtization test   
2. Data acquisition from LabJack digitizer 
Guideline for SPOT's development environment for this repository's container setting can be found at: <https://github.com/fermilab-robotics/spot-dev-environment> 

## LOCALIZATION TEST 
SPOT's localization test is essential in providing SPOT's definite locations in the world frame, in relative to where its dock (e.g:(0,0,0) point) is located. This data is crucial in helping us to identify the magnet from which we obtain the LSM data from.

SPOT forms its localization via a system of waypoints and edges. Waypoints define named locations in the world, and edges define how to get from one waypoint to another. SPOT Frames and April Tag are core elements that make up the fundamental of the localization test.

###### SPOT Frames 
SPOT's location data is acquired in Odom and Vision Frames which are the two inertial frames of the robot.
Information about SPOT's Geometry and Frames: <https://dev.bostondynamics.com/docs/concepts/geometry_and_frames> 

###### April Tag 
AprilTag is a visual fiducial system. SPOT SDK includes modules(e.g:```world_object``` in the client library) that allow the implementation of AprilTag as raw data that assists with the establishing of waypoints. 

SPOT is capable of detecting AprilTags using its base cameras and retrieve the data into the object frame and will be treated as the ground truth reference object. The Tag plays an essential roles in assiting SPOT navigate through the world in a metrically consistent manner. 

In our case, April Tag assists us with our calibration purposes for localizing SPOT in the world, on top of SPOT's frame system itself. 

## LABJACK DIGITIGER READING 
The main duty of the LabJack digitizer is to take the actual radiation dose reading from the LSM and digitize it into bits that we could further process on the acquired data. Information about our LabJack
`U3digitizer.py` module stream the data from the digitizer. 
LabJack has their own repositories [Exodriver](https://github.com/labjack/exodriver) and [LabJackPython](https://github.com/labjack/LabJackPython). These two repositories are imported into this container using Docker command. Below are some details on what each repository do and how to set them up so that `U3digitizer.py` could import modules from them.   
###### Exodriver 
Exodriver is what the LabJack digitizer use to access the USB library. After the container is built from the Dockerfile. Open a bash terminal: 
```
cd /exodriver
sudo ./install.sh 
```
All the USB modules needed to interface with the device after the above steps could be found in `/usr/local/lib/`. This path should be added to `sys.path` in the code that is used to interface with the device.  

###### LabJackPython
LabJackPython source code contains all the necessary modules to interact with the digitzer device for reading, writing, streaming data. The repository comes within this container. After the container is built, open a bash terminal: 
```
cd /LabJackPython 
sudo python3 setup.py install

``` 
## ABOUT THE CODE 
###### LOCALIZATION TEST 
The original repository for our SPOT's localization test is at <https://github.com/fermilab-robotics/localization_test>. 
The localization test code in this repository is refactored from the repository mentioned above. 
Here are the break down of the code components: 
1. `Robot_state.py`: this module is used to obtain the current robot state 
2. `Location.py`:this module includes method to obtain the Robot location, time stamps and to establish April Tag requests 
3. `Main`: all the necessary operations needed to obtain localization data from SPOT and serializing objects that carry the data. 
###### DIGITIZER DATA STREAMING 
`U3digitizer.py` is the only module that contains code to get all what we need from the digitizer. 
  


