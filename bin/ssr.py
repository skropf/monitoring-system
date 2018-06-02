import os
import sys
import time
import RPi.GPIO as GPIO

def logger(log):
    with open("../logs/monitoring.logs", 'a') as f:
        f.write("[" + str(time.strftime("%Y-%m-%d %X", time.localtime())) + "] " + log + "\n")
        f.close()

logger("Running script...")

# disable channel in use warning
GPIO.setwarnings(False)

# use RPi.GPIO layout
GPIO.setmode(GPIO.BCM)

mapping = { '1': 4, '2': 17, '3': 18, '4': 22, '5': 23, '6': 24, '7': 25, '8': 27 }

job = sys.argv[1] # on/off/read/...

if job == 'on' or job == 'off':
    logger("Turning ssr [" + sys.argv[2:] + "] " + job)

    # set pin to output
    for pin in sys.argv[2:]:
        GPIO.setup(mapping[pin], GPIO.OUT)

        if job == 'on':
            GPIO.output(mapping[pin], GPIO.HIGH)
        else:
            GPIO.output(mapping[pin], GPIO.LOW)

elif job == 'read':
    #cooling water temperature
    logger("Reading water temperature.")
    os.system("cat /sys/bus/w1/devices/*/w1_slave > ../data/.tempSensorData")
    temp = int(open('../data/.tempSensorData').readlines()[1].strip().split("t=")[1]) / 1000.0
    open('../data/coolingWaterTemp', 'w').write(str(temp))

    #other sensors to come...


elif job == 'pic':
    logger("Taking picture...")    
    os.system("/opt/vc/bin/raspistill -o ../data/images/i%04d.jpg")

#end
