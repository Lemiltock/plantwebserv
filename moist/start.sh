#!/bin/sh
cd /home/pi/moist;
sudo /usr/bin/python3 /home/pi/moist/moist.py &
cd /home/pi/webapp;
sudo /usr/bin/python3 /home/pi/webapp/app.py &
