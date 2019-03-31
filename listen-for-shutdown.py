#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(13, GPIO.FALLING)

subprocess.call(['shutdown', '-h', 'now'], shell=False)
