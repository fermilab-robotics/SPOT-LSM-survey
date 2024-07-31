#!/bin/bash


for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    
    syspath="${sysdevpath%/dev}"
    devname="$(udevadm info -q name -p $syspath)"
    [[ "$devname" == "bus/"* ]] && continue
    e="$(udevadm info -q property --export -p $syspath)"
    eval $e


    [[ -z "$ID_SERIAL" ]] && continue
    if [[ $ID_SERIAL =~ "Mirion" ]]; then
        port="/dev/$devname"
        echo "export mirion_port=$port" > /etc/profile.d/mirion_port.sh
        mirion_port=$port  
        if [[ -n "$mirion_port" ]]; then break; fi
    fi
   

   
done


if [ -z "$mirion_port" ]; then
    echo "export mirion_port='default_value'" > /etc/profile.d/mirion_port.sh 
fi

echo "Mirion port: $mirion_port"
