# Copyright (c) 2023 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

"""Example of how to talk to the remote mission service examples in this directory."""

import argparse
import time
from contextlib import ExitStack

import grpc

import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.mission.remote_client
from bosdyn.api import service_customization_pb2
from bosdyn.api.mission import remote_pb2


_WHO_KEY = 'who'


def main():
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('--hello-world', action='store_true',
    #                    help='Target the Hello World remote mission service.')
   
    # parser.add_argument(
    #     '--user-string',
    #     help='Specify the user-string input to Tick. Set to the node name in Autowalk missions.')

    subparsers = parser.add_subparsers(help='Select how this service will be accessed.',
                                       dest='host_type')
    # Create the parser for the "local" command.
    local_parser = subparsers.add_parser('local', help='Connect to a locally hosted service.')
    bosdyn.client.util.add_service_endpoint_arguments(local_parser)
    # Create the parser for the "robot" command.
    robot_parser = subparsers.add_parser('robot',
                                         help='Connect to a service through the robot directory.')
    bosdyn.client.util.add_base_arguments(robot_parser)

    options = parser.parse_args()


    directory_name = 'stopper-svc'
    # directory_name='hello-world-callback'
    lease_resources = ()


    # If attempting to communicate directly to the service.
    if options.host_type == 'local':
        # Build a client that can talk directly to the RemoteMissionService implementation.
        client = bosdyn.mission.remote_client.RemoteClient()
        # Point the client at the service. We're assuming there is no encryption to set up.
        client.channel = grpc.insecure_channel(f'{options.host_ip}:{options.port}')
    # Else if attempting to communicate through the robot.
    else:
        # Register the remote mission client with the SDK instance.
        sdk = bosdyn.client.create_standard_sdk('RemoteMissionClientExample')
        sdk.register_service_client(bosdyn.mission.remote_client.RemoteClient,
                                    service_name=directory_name)
        print(f'service name:{directory_name}')

        robot = sdk.create_robot(options.hostname)
        bosdyn.client.util.authenticate(robot)

        # Create the remote mission client.
        client = robot.ensure_client(directory_name)

    input_params = service_customization_pb2.DictParam()

  
    # Use an ExitStack because we might or might not have a lease keep-alive
    # depending on command line arguments
    with ExitStack() as exit_stack:
        if lease_resources and options.host_type != 'local':
            lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
            exit_stack.enter_context(
                bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True,
                                                   return_at_exit=True))
        # Now run through a typical sequence of calls to the remote servicer.
        # Establish the session, telling the servicer to perform any one-time tasks.
        try:
            session_id = client.establish_session(lease_resources=lease_resources)
            

        except bosdyn.client.UnimplementedError:
            # EstablishSession is optional, so we can ignore this error.
            print('EstablishSession is unimplemented.')
            session_id = None

        # Begin ticking, and tick until the server indicates something other than RUNNING.
        response = client.tick(session_id, lease_resources=lease_resources, params=input_params)
        while response.status == remote_pb2.TickResponse.STATUS_RUNNING:
            time.sleep(0.1)
            response = client.tick(session_id, lease_resources=lease_resources, params=input_params)
        print(
            f'Servicer stopped with status {remote_pb2.TickResponse.Status.Name(response.status)}')
        if response.error_message:
            print(f'\tError message: {response.error_message}')

        try:
            # We're done ticking for now -- stop this session.
            client.stop(session_id)
            # We don't want to tick with this particular session every again -- tear it down.
            client.teardown_session(session_id)
        except bosdyn.client.UnimplementedError as exc:
            # The exception itself can tell us what's not implemented.
            print('Either Stop or TeardownSession is unimplemented.')


if __name__ == '__main__':
    main()
