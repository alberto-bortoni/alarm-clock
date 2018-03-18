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


#################################
#          VARIABLES            #
#################################

snoozeTimes = 10
timeIncVol = 1
timeButt = 2
snoozeInc = 2

butt = 13
exitFlag = 0
snooze = 0


musicDir = "/home/eleven/Music/"
songs = os.listdir(musicDir)
songsNum=len(musicDir)
randSong = randint(1, songsNum)-1

#################################
#             INIT              #
#################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

startTime = time.time()
thisTime = time.time()
lastTime = time.time()
buttTime = time.time()

#################################
#             MAIN              #
#################################

player = subprocess.Popen(["mplayer", "-volume", "10", "-volstep", "1", musicDir+songs[randSong]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

while exitFlag==0:

  if (time.time()-lastTime >= timeIncVol):  #increase volume
    player.stdin.write('0')
    player.stdin.flush()
    lastTime = time.time()

  if(GPIO.input(butt)==0):                  #start snooze/exit
    time.sleep(0.25)
    buttTime = time.time()

    while (time.time()-buttTime < timeButt):

      if(GPIO.input(butt)==0):              #count snooze, reset timer
        buttTime = time.time()
        snooze = snooze+1
        for num in range(1, snoozeInc):
          player.stdin.write('9')           #reduce noise every button
          player.stdin.flush()
          time.sleep(0.25)

      if(snooze >= snoozeTimes)             #exit, snoozed
        player.terminate()
        exitFlag=1

  if (time.time()-startTime > 600):         #exit program, too long
    player.terminate()
    exitFlag=1


#################################
#           SERVICES            #
#################################




