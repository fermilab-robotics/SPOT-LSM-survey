# Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

"""this scripts run the main gRPC servicer, listening to request for taking localizations & rad data"""

import logging
import sys
import os
from datetime import datetime

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import service_customization_pb2
from bosdyn.api.mission import remote_pb2, remote_service_pb2_grpc
from bosdyn.client.auth import AuthResponseError
from bosdyn.client.directory_registration import (DirectoryRegistrationClient,
                                                  DirectoryRegistrationKeepAlive)
from bosdyn.client.lease import Lease, LeaseClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient
from bosdyn.client.server_util import GrpcServiceRunner, ResponseContext
from bosdyn.client.service_customization_helpers import (InvalidCustomParamSpecError,
                                                         validate_dict_spec)
from bosdyn.client.util import setup_logging
from bosdyn.mission import util

from main_daq import (establish_session,tick,stop,teardownsession,
                      main_daq,path_to_temp)
DIRECTORY_NAME = 'SPOT-LSM-svc'
AUTHORITY = 'remote-mission-main'
SERVICE_TYPE = 'bosdyn.api.mission.RemoteMissionService'

_LOGGER = logging.getLogger(__name__)
_ID_KEY="robotic-group"

class HelloWorldServicer(remote_service_pb2_grpc.RemoteMissionServiceServicer):
    """Every tick, logs 'Hello world!'

    Shows an example of these concepts:
     - Ticking.
     - Using inputs.
    """

    def __init__(self, logger=None):
        self.logger = logger or _LOGGER
        # Create the custom parameters.
        self.custom_params = service_customization_pb2.DictParam.Spec()
        self.robot=None
        self.data=None
        self.data_to_be_written=None
  
        
        try:
            # Validate the custom parameters.
            validate_dict_spec(self.custom_params)
        except InvalidCustomParamSpecError as e:
            self.logger.info(e)
            # Clear the custom parameters if they are invalid.
            self.custom_params.Clear()

    def Tick(self, request, context):
        """Logs time of taking data"""
        print("--------------------Tick--------------------")
        response = remote_pb2.TickResponse()
        
        with ResponseContext(response, request):
            handler=main_daq(self.robot)
            self.data=tick(handler)
            response.status = remote_pb2.TickResponse.STATUS_SUCCESS
        return response

    def EstablishSession(self, request, context):
        """ Setting up env for API call"""
        print("--------------------EstablishSession--------------------")
        response = remote_pb2.EstablishSessionResponse()
        usrname=os.getenv("BOSDYN_CLIENT_USERNAME")
        password=os.getenv("BOSDYN_CLIENT_PASSWORD")
        spot_host=os.getenv("spot_host")
        assert usrname!=None,"username is not provided"
        assert password!=None,"password is not provided"
        assert spot_host!=None,"SPOT host ip is not provided"
        
        with ResponseContext(response, request):
            self.logger.info('Environment Setup Success \n please empty out your history.csv if this is the start of your daq session')
            self.robot=establish_session([spot_host])
            response.status = remote_pb2.EstablishSessionResponse.STATUS_OK
        return response

    def Stop(self, request, context):
        print("--------------------Stop--------------------")
        response = remote_pb2.StopResponse()
        with ResponseContext(response, request):
            self.logger.info('Writting data to temp file')
            stop(self.data)
            teardownsession()
            self.logger.info(f'Writting data to csv file\n End of one request\n\n')
            response.status = remote_pb2.StopResponse.STATUS_OK
        return response

    def TeardownSession(self, request, context):
        response = remote_pb2.TeardownSessionResponse()
        print("--------------------TeardownSession--------------------")
        with ResponseContext(response, request):
            #teardownsession()
            self.logger.info(f'Tear down called\n\n')
            response.status = remote_pb2.TeardownSessionResponse.STATUS_OK
        return response

    def GetRemoteMissionServiceInfo(self, request, context):
        response = remote_pb2.GetRemoteMissionServiceInfoResponse()
        with ResponseContext(response, request):
            response.custom_params.CopyFrom(self.custom_params)
            epoch_time=response.header.request_received_timestamp.seconds
            #self.logger.info(f'Request received timestamp: {datetime.fromtimestamp(epoch_time)}')
        return response


def run_service(port, logger=None):
    # Proto service specific function used to attach a servicer to a server.
    add_servicer_to_server_fn = remote_service_pb2_grpc.add_RemoteMissionServiceServicer_to_server

    # Instance of the servicer to be run.
    service_servicer = HelloWorldServicer(logger=logger)
    return GrpcServiceRunner(service_servicer, add_servicer_to_server_fn, port, logger=logger)


if __name__ == '__main__':
    # Define all arguments used by this service.
    import argparse

    # Create the top-level parser.
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    bosdyn.client.util.add_service_endpoint_arguments(parser)
    options = parser.parse_args()
    
    setup_logging(options.verbose)

    # Create and authenticate a bosdyn robot object.
    sdk = bosdyn.client.create_standard_sdk('HelloWorldMissionServiceSDK')
    robot = sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)

    # Create a service runner to start and maintain the service on background thread.
    service_runner = run_service(options.port, logger=_LOGGER)

    # Use a keep alive to register the service with the robot directory.
    dir_reg_client = robot.ensure_client(DirectoryRegistrationClient.default_service_name)
    keep_alive = DirectoryRegistrationKeepAlive(dir_reg_client, logger=_LOGGER)
    keep_alive.start(DIRECTORY_NAME, SERVICE_TYPE, AUTHORITY, options.host_ip, service_runner.port)

    # at the end of session, combine finalized headers with data. 
    with keep_alive:
       
        service_runner.run_until_interrupt()
    

