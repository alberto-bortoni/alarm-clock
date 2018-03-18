#! /usr/bin/python

import os
import time
from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('started')

if(GPIO.input(13)):
  print('22')


while True:
  #if(GPIO.input(12) == 0):
   # print('12') 
  #if(GPIO.input(13) == 0):
   # print('13')
  #if(GPIO.input(16) == 0):
   # print('16')
  if(GPIO.input(13)==0):
    print('22')

  time.sleep(1)

