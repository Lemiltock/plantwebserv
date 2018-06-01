import os
import glob
import Adafruit_ADS1x15
from flask import Flask, render_template, send_file
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

adc = Adafruit_ADS1x15.ADS1015()

def read_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    if lines[0].strip()[-3:] != 'YES':
        return 'error'
    equals_pos = lines[1].find('t=1')
    if equals_pos != -1:
        return float(lines[1][equals_pos+2:]) / 1000.0

app = Flask(__name__)

@app.route('/')
def images():
    temp = read_temp()
    return render_template('index.html', temp=temp, moist=adc.read_adc(0, gain=2/3))

@app.route('/fig')
def fig():
    try:
        from io import BytesIO
    except ImportError:
        from StringIO import StringIO
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    t = datetime.datetime.now()
    path = '/home/pi/moist/data/'
    file = str(getattr(t, 'day')).zfill(2) + str(getattr(t, 'month')).zfill(2) + str(getattr(t, 'year'))
    raw = []
    temp = []
    moist = []
    times = []
    hold = []

    try:
        with open(path + file, 'r') as log:
            for line in log:
                raw.append(line)
    except:
        print('error in log file')
    else:
        log.close()

    for l in raw:
        hold = l.split()
        moist.append(hold[0])
        temp.append(hold[1])
        times.append(hold[2])
    
    fig = plt.figure()
    host = fig.add_subplot(111)
    par1 = host.twinx()
    host.set_ylim(0, 1000)
    par1.set_ylim(10, 30)
    host.set_xlabel('time in minutes')
    host.set_ylabel('moisture')
    par1.set_ylabel('temperature')
    p1, = host.plot(times, moist, color='b', label='moisture')
    p2, = par1.plot(times, temp, color='r', label='temperature')
    lns = [p1, p2]
    host.legend(handles=lns, loc='best')
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True, host='0.0.0.0', port=8080)
