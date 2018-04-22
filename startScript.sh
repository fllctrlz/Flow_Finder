#!/bin/sh
sleep 10
hostname -I
sudo service myService start
sudo python /home/pi/Desktop/Flow_Finder/serialRead/serialRead.py
