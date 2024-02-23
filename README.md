<div align="center">

# SPOT-LSM-survey
Radiation survey with digitized Log Survey Meter (LSM) and Boston Dynamic SPOT robot
 </div>

<p align="center"><img src="./img/spot-removebg-preview.png" width="auto" height="200" /></p>
<p align="center"><img src="./img/FNAL-Logo-NAL-Blue.png" width="200" height="auto"></p>

<div align="center" >
<a href="https://github.com/boston-dynamics/spot-sdk"><img src="https://img.shields.io/badge/spot--sdk-FBD403?style=flat"/></a>
<a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white"/></a>
<a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.7-3776AB.svg?style=flat&logo=python&logoColor=white"/></a>
<a href="https://labjack.com/"><img src="https://img.shields.io/badge/LabJackPython-2.1.0-8B0000?style=flat"/></a>
</div>


Guideline for SPOT's development environment for this repository's container setting can be found at: <https://github.com/fermilab-robotics/spot-dev-environment> 

## CONCEPTS

### LOCALIZATION 

SPOT's localization data is essential in providing SPOT's definite locations in the world frame, in relative to where its dock (e.g:(0,0,0) point) is. This data is crucial in helping us identify the magnet from which we obtain the LSM radiation data from.

SPOT forms its localization via a system of waypoints and edges. Waypoints define named locations in the world, and edges define how to get from one waypoint to another. SPOT Frames and April Tag are core elements that make up the fundamental of the localization test.

#### SPOT Frames 

SPOT's location data is acquired in Odom and Vision Frames which are the two inertial frames of the robot.
Information about SPOT's Geometry and Frames: <https://dev.bostondynamics.com/docs/concepts/geometry_and_frames> 

#### April Tag 

AprilTag is a visual fiducial system. SPOT SDK includes modules(e.g:```world_object``` in the client library) that allow the implementation of AprilTag as raw data that assists with the establishing of waypoints. 

SPOT is capable of detecting AprilTags using its base cameras and retrieve the data into the object frame and will be treated as the ground truth reference object. The Tag plays an essential roles in assiting SPOT navigate through the world in a metrically consistent manner. 

In our case, April Tag assists us with our calibration purposes for localizing SPOT in the world, on top of SPOT's frame system itself. 

### LABJACK DIGITIGER READING 
The main duty of the LabJack digitizer is to take the actual radiation dose readings from the LSM and digitize them into bits that we could further process for our interests. 
LabJack has their own repositories [Exodriver](https://github.com/labjack/exodriver) and [LabJackPython](https://github.com/labjack/LabJackPython). These two libraries are already set up in the Docker container.

#### Exodriver 
Exodriver is what the LabJack digitizer use to access the USB library. 

#### LabJackPython
LabJackPython source code contains all the necessary modules to interact with the digitzer device for reading, writing, streaming data.

## CODE

### [Localizations](./revised/localizations/)  
Methods implemented in [localization module](./revised/localizations/localization.py) is refactored from <https://github.com/fermilab-robotics/localization_test>. 

Code components: 
1. `xformsnapshot`: method to get transform snapshot
2. `visionxform`: method to obtain body frame from vision frame
3. `odomxform`: method to obtain body frame from odom frame
4. `get_time`: method to get time stamp

### [LSM Digitizer](./revised/lsm_digitizers/)
The [digitizer module](./revised/lsm_digitizers/digitizer.py) includes methods to set up and configure the U3 DAQ device for streaming voltage readings from the LSM. 



### [Data Acquisitions](./revised/data_acquisitions/) 

The [data_acquisition module](./revised/data_acquisitions/data_acquisition.py) includes methods to process data for data report. 

Code componenets:

## DEVELOPMENT ENVIRONMENT SETUP
There are two options to set up the development environment: 
- [Vscode remote dev container](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker compose](https://docs.docker.com/compose/)

For testing out reading from U3 DAQ device, docker compose has to be used. 

### Remote Dev Container

1. Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
1. From the `command pallete` of vscode, select `Reopen in container`
The image will be built using the Dockerfile in the .devcontainer folder. [devcontainer.json](.devcontainer/devcontainer.json) is referenced to build up the container. 



### Docker Compose 

1. Build the based image

```
cd /path_to_your_cloned_repository

docker build -f .devcontainer/Dockerfile -t spot-lsm:v1.0 
```

2. Modify volume mount directory in docker-compose.yaml

Volume mount is being used for the container so that changes in local repository would be reflected inside the container. 
The very first line of volume mount, currently `/home/lpham/CODE/SPOT-LSM-survey` needed to be changed to an absolute path to where your local cloned repository is located. 

3. Spin up the container 

```
docker compose up -d 
```









  


