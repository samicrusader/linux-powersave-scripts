#!/bin/bash
# taken from https://askubuntu.com/questions/619875/disabling-intel-turbo-boost-in-ubuntu/619881#619881
# modified to force no_turbo off

if [[ -z $(which rdmsr) ]]; then
    echo "msr-tools is not installed." >&2
    exit 1
fi

if [[ ! -z $1 && $1 != "enable" && $1 != "disable" ]]; then
    echo "Invalid argument: $1" >&2
    echo ""
    echo "Usage: $(basename $0) [disable|enable]"
    exit 1
fi

cores=$(cat /proc/cpuinfo | grep processor | awk '{print $3}')
for core in $cores; do
    if [[ $1 == "disable" ]]; then
        sudo wrmsr -p${core} 0x1a0 0x4000850089
    fi
    if [[ $1 == "enable" ]]; then
        sudo wrmsr -p${core} 0x1a0 0x850089
    fi
    state=$(sudo rdmsr -p${core} 0x1a0 -f 38:38)
    if [[ $state -eq 1 ]]; then
        echo "core ${core}: disabled"
    else
        echo "core ${core}: enabled"
    fi
done
if [[ $1 == "enable" ]]; then # no need to set to 1 on disable, already set when powersave governor is enabled
    echo "0" > /sys/devices/system/cpu/intel_pstate/no_turbo
    echo "enabled turbo on pstate driver"
fi
exit 0