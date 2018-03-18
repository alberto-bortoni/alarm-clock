#! /usr/bin/python

import os
import time
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butt = 13

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('started')

if(GPIO.input(butt)):
  print('22')


while True:
  if(GPIO.input(butt)==0):
    print('22')

  time.sleep(1)

