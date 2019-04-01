#!/usr/bin/env python

import mpylayer
import os
import time
import subprocess
from subprocess import PIPE, STDOUT
import shlex
from time import sleep
import RPi.GPIO as GPIO




GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
  falling = GPIO.wait_for_edge(13, GPIO.FALLING)
  time.sleep(0.2)

  if falling is not None:
    rising = GPIO.wait_for_edge(13, GPIO.RISING, timeout=10000)
    if rising is None:
      alarm = subprocess.Popen(["mplayer", "-volume", "75", "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
      time.sleep(6)
      alarm.terminate()
      #subprocess.call(['shutdown', '-h', 'now'], shell=False)
