# plantwebserv
moisture and temp sensor through web site

To configure copy moist and web app folder to /home/pi on a raspberry pi
Then cd to /home/pi/moist and run sudo chmod a+x startup.sh

Then append /home/pi/moist/start.sh to the /etc/rc.local file before the exit 0 line

Ensure the Pi has a static IP, the website is viewable at 0.0.0.0:8080 (local host)
