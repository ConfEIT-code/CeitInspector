#!/bin/sh
#Open the coredump
ulimit -c unlimited

#Clean and create coredump location
if [ -d "/corefile" ];then
rm -rf /corefile
fi
mkdir /corefile

#Specify the location for coredump
echo "/corefile/core-%e-%p-%t" > /proc/sys/kernel/core_pattern
