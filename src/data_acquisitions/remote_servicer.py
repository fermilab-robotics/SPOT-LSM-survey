import logging
import sys

from google.protobuf import json_format

import bosdyn.client.util
from bosdyn.api import data_acquisition_pb2, data_acquisition_plugin_service_pb2_grpc
from bosdyn.client.data_acquisition_plugin_service import (Capability, DataAcquisitionPluginService,
                                                           DataAcquisitionStoreHelper)
from bosdyn.client.data_acquisition_store import DataAcquisitionStoreClient
from bosdyn.client.directory_registration import (DirectoryRegistrationClient,
                                                  DirectoryRegistrationKeepAlive)
from bosdyn.client.math_helpers import SE3Pose

from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.server_util import GrpcServiceRunner
from bosdyn.client.util import setup_logging

from data_acquisition import quat_to_Euler


sys.path.append("/home/lpham/CODE/SPOT-LSM-survey/src/")
from localizations.spot import Spot



DIRECTORY_NAME = 'spot-lsm-data-acquisition'
AUTHORITY = 'spot-mirion'
CAPABILITY = Capability(name='spot-lsm', description='radiation measurement', channel_name='spot')


_LOGGER = logging.getLogger('spot-lsm')


class SpotLsm: 

    def __init__(self, sdk_robot):
        self.client = sdk_robot.ensure_client(RobotStateClient.default_service_name)
        self.spot=Spot(sdk_robot)

    def get_spot_data(self, request: data_acquisition_pb2.AcquirePluginDataRequest,
                         store_helper: DataAcquisitionStoreHelper):
        state = self.client.get_robot_state(timeout=1)
        
        data_id = data_acquisition_pb2.DataIdentifier(action_id=request.action_id,data_name="spot_data",
                                                      channel=CAPABILITY.channel_name)

        store_helper.cancel_check()
        store_helper.state.set_status(data_acquisition_pb2.GetStatusResponse.STATUS_SAVING)

        message = data_acquisition_pb2.AssociatedMetadata()
        message.reference_id.action_id.CopyFrom(request.action_id)

        message.metadata.data.update(
            {
                "vision": json_format.MessageToJson(self.spot.visionxform().to_proto())
            
            }
        )

        #example for another field of data
        data_id2= data_acquisition_pb2.DataIdentifier(action_id=request.action_id,data_name="test_data",
                                                      channel='test')
        
        message2 = data_acquisition_pb2.AssociatedMetadata()
        message2.reference_id.action_id.CopyFrom(request.action_id)
        message.metadata.data.update(
            {
                "percentage": state.power_state.locomotion_charge_percentage.value 
            
            }
        )

      
        _LOGGER.info('Retrieving battery data: %s', message.metadata.data)

        store_helper.store_metadata(message, data_id)
        store_helper.store_metadata(message2, data_id2)

    
def make_servicer(sdk_robot):
    """Create the data acquisition servicer """
    
    adapter = SpotLsm(sdk_robot)
    return DataAcquisitionPluginService(sdk_robot, [CAPABILITY], adapter.get_spot_data,logger=_LOGGER)



def run_service(sdk_robot, port):
    """Create and run the battery plugin service."""
    # Proto service specific function used to attach a servicer to a server.
    add_servicer_to_server_fn = data_acquisition_plugin_service_pb2_grpc.add_DataAcquisitionPluginServiceServicer_to_server

    # Instance of the servicer to be run.
    return GrpcServiceRunner(make_servicer(sdk_robot), add_servicer_to_server_fn, port,
                             logger=_LOGGER)



def main():
    # Define all arguments used by this service.
    import argparse
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    bosdyn.client.util.add_payload_credentials_arguments(parser)
    bosdyn.client.util.add_service_endpoint_arguments(parser)
    options = parser.parse_args()

    setup_logging(options.verbose)

    sdk = bosdyn.client.create_standard_sdk('BatteryPlugin')
    robot = sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)

    service_runner = run_service(robot, options.port)


    # Use a keep alive to register the service with the robot directory.
    dir_reg_client = robot.ensure_client(DirectoryRegistrationClient.default_service_name)
    keep_alive = DirectoryRegistrationKeepAlive(dir_reg_client, logger=_LOGGER)
    keep_alive.start(DIRECTORY_NAME, DataAcquisitionPluginService.service_type, AUTHORITY,
                     options.host_ip, service_runner.port)

    # Attach the keep alive to the service runner and run until a SIGINT is received.
    with keep_alive:
        service_runner.run_until_interrupt()

if __name__ == '__main__':
    main()