#!/bin/sh
useradd ftpadmin
# set the passwd 123456
cd /home/ftpadmin
mkdir var
cd var
mkdir ftp
cd ftp
mkdir public
cd public
touch hello.txt