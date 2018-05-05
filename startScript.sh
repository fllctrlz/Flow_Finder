#!/bin/sh
sleep 10
hostname -I
hostname -I > /home/pi/Desktop/Flow_Finder/ip.txt
sudo service myService start
echo "webserver started"
sudo python /home/pi/Desktop/Flow_Finder/serialRead/serialRead.py &
echo "serialRead started"
sudo python /home/pi/Desktop/Flow_Finder/dislpay/raspberrypi/python/main.py &
echo "display program ran"