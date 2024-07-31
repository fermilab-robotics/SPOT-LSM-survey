#!bin/bash 

./port_detection.sh

if [ -f /etc/profile.d/mirion_port.sh ]; then
    echo "port exists" 
    source /etc/profile.d/mirion_port.sh
fi


python3 main.py $spot_host 

exec "$@"