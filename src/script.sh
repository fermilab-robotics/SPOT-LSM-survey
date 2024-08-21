#!/bin/bash
python3 data_acquisitions/remote_servicer.py --payload-credentials-file $CRED_FILE --host-ip=$self_ip $spot_host
