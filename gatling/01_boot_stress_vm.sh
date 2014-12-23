#!/bin/bash -x

function get_uuid () { cat - | grep " id " | awk '{print $4}'; }
MY_DEFAULT_NET=`neutron net-show work-net | get_uuid`

nova boot --flavor standard.small \
    --image "centos-base" \
    --key-name key-for-internal --user-data userdata_stress.txt \
    --security-groups sg-all-from-console,sg-web-from-internet \
    --availability-zone az1 \
    --nic net-id=${MY_DEFAULT_NET} stress-test
