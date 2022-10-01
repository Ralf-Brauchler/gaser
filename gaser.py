#!/usr/bin/python
# coding=utf-8

import sys, time
import RPi.GPIO as GPIO
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s|[%(levelname)s]|%(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename= 'gaser.log',
                    filemode='a')
console = logging.StreamHandler()
logging.getLogger().addHandler(console)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

delayTime = 1
Digital_PIN = 24
sensorStatus = False
previousStatus = False
sumGas = 0.0

GPIO.setup(Digital_PIN, GPIO.IN, pull_up_down = GPIO.PUD_OFF)

print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '| starting up  | now | done')
logging.info('starting up|1|done')

while True:
    sensorStatus = GPIO.input(Digital_PIN)
    # logging.debug('| sensor polled  |' + str(sensorStatus) + '|polled')

    if sensorStatus != previousStatus:
        if sensorStatus:
            sumGas += 0.1
            logging.info('sensor change  |' + str(sensorStatus) + '|changed')
            logging.info('sum of gas     |' + str(sumGas) + '|kwh')
        else:
            logging.info('sensor change  |' + str(sensorStatus) + '|changed')

    previousStatus = sensorStatus
    time.sleep(delayTime)
