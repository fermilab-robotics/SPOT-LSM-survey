#!/bin/bash

port=''
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        syspath="${sysdevpath%/dev}"
        devname="$(udevadm info -q name -p $syspath)"
        [[ "$devname" == "bus/"* ]] && exit
        e="$(udevadm info -q property --export -p $syspath)"
        eval $e
        [[ -z "$ID_SERIAL" ]] && exit
        if [[ $ID_SERIAL =~ "Mirion" ]]; then
            port="/dev/$devname"
            echo $port
            sudo chmod 666 "$port"
            exit
        fi
    )
done
