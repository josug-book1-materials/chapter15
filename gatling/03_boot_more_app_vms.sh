#!/bin/bash -x

boot_app_server() {
    nova boot --flavor $flavor --image "centos-base" \
        --key-name key-for-internal --user-data userdata_app.txt \
        --security-groups sg-all-from-console,sg-all-from-app-net,sg-all-from-dbs-net \
        --availability-zone az1 \
        --nic net-id=${MY_DMZ_NET} --nic net-id=${MY_APP_NET} --nic net-id=${MY_DBS_NET} \
        $name
}

function get_uuid () { cat - | grep " id " | awk '{print $4}'; }
MY_DMZ_NET=`neutron net-show dmz-net | get_uuid`
MY_APP_NET=`neutron net-show app-net | get_uuid`
MY_DBS_NET=`neutron net-show dbs-net | get_uuid`

if [ -n "$1" ]; then
    name=$1
    flavor=${2:-standard.xsmall}
    boot_app_server $name $flavor
else
    boot_app_server app02-xsmall standard.xsmall
    boot_app_server app03-small  standard.small
    boot_app_server app04-medium standard.medium
fi
