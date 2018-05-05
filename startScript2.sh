#!/bin/sh
sleep 10
hostname -I
sudo service myService start
echo "Web server running"
sudo python /home/pi/Desktop/Flow_Finder/serialRead/serialRead.py &
echo "serialRead started"
sudo python /home/pi/Desktop/Flow_Finder/dislpay/raspberrypi/python/main2.py &
echo "display started"
