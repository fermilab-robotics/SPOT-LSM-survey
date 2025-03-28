#!/bin/sh 

# This script is the entrypoint for container setup when deploying on CORE

host_ip=$(python3 src/get_self_ip.py)
python3 src/main.py --host-ip $host_ip --port 5000 $spot_host

exec "$@"
