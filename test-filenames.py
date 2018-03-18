#! /usr/bin/python
#################################
#             HEAD              #
#################################
import mpylayer
import os
import time
import subprocess
from subprocess import PIPE, STDOUT
import shlex
from time import sleep
import RPi.GPIO as GPIO
from random import *

GPIO.setmode(GPIO.BCM)
butt = 13

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('started')

print('hello, world!')
test = "/home/eleven/Music/"
song = "coldplay-cemeteriesOfLondon.mp3"

dirs = os.listdir(test)
print(dirs)

siz=len(dirs)

print(siz)
rand = randint(1, siz)-1
print(rand)
print(dirs[rand])

#player = subprocess.Popen(["mplayer", "-volume", "50", "-volstep", "2", test+dirs[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

#time.sleep(10)
#player.terminate()

print('again!')


#while True:
if(GPIO.input(butt)==0):
  print('22')
  #player.stdin.write('p')
  #player.stdin.flush()

#time.sleep(1)
