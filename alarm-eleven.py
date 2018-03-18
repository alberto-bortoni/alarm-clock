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


#################################
#          VARIABLES            #
#################################

butt = 13



#################################
#             INIT              #
#################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print('hello, world!')

player = subprocess.Popen(["mplayer", "-volume 0", "/home/eleven/Music/coldplay-cemeteriesOfLondon.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

time.sleep(5)

print('again!')


#################################
#             MAIN              #
#################################


while True:
  dummy = input()

  if dummy == 1:
    print('ta')
    player.terminate()
    print('ta')
  if dummy == 2:
    print ('ts')
    player.stdin.write('p')
    player.stdin.flush()
  if dummy == 3:
    print ('ts')
    player.stdin.write('9')
    print(player.stdout.readline())
    player.stdin.flush()
  if dummy == 4:
    player.stdin.write('0')
    player.stdin.flush()



#print('done')


#################################
#           SERVICES            #
#################################




