import time
import Adafruit_ADS1x15
import os
import glob
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = f.readlines()
        f.close()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
         return float(lines[1][equals_pos+2:])/ 1000.0

adc = Adafruit_ADS1x15.ADS1015()

while True:
    avg = []
    for i in range(29):
        avg.append(adc.read_adc(0, gain=2/3))
        time.sleep(10)
    t = datetime.datetime.now()
    path = '/home/pi/moist/data/'
    file = str(getattr(t, 'day')).zfill(2) + str(getattr(t, 'month')).zfill(2) + str(getattr(t, 'year'))
    logtime = str((getattr(t, 'hour')* 60) + getattr(t, 'minute'))
    moist = float(sum(avg))/len(avg)
    temp =  read_temp()
    with open(path + file, 'a') as log:
        log.write(str(moist) + ' ')
        log.write(str(temp) + ' ')
        log.write(logtime + '\n')
        log.close()
