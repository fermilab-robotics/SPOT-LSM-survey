#!/bin/bash 

./port_detection.sh

if [ -f /etc/profile.d/mirion_port.sh ]; then
    echo "port exists" 
    source /etc/profile.d/mirion_port.sh
fi

# get the host ip of CORE, or host where the mission service is running  
python3 src/get_self_ip.py

python3 src/main.py --host-ip $test_ip $spot_host 

exec "$@"