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
timeIncVol = 5
timeButt = 2
snoozeInc = 2
volume = 10
volumeStep = 2
maxVol = 110
medVol = 90

butt = 13
exitFlag = 0
snooze = 0


musicDir = "/home/eleven/Music/"
songs = os.listdir(musicDir)
songsNum=len(songs)
randSong = randint(1, songsNum)-1

#################################
#             INIT              #
#################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(butt, GPIO.RISING, callback=butt_rising)  # add rising edge detection on a channel
GPIO.add_event_detect(butt, GPIO.FALLING, callback=butt_falling)

startTime = time.time()
thisTime = time.time()
lastTime = time.time()
buttRisingTime = None
buttFallingTime = None
buttDuration = None
longPressWaiting = False
shortPressWaiting = False
numLongPresses = 0
numShortPresses = 0

#################################
#         GPIO INIT             #
#################################

butt_rising(channel):
  buttRisingTime = time.time()
  print "Rising edge detected on channel %i at %f".format(channel, buttRisingTime)

butt_falling(channel):
  buttFallingTime = time.time()
  buttDuration = (buttFallingTime - buttRisingTime) if buttRisingTime is not None else None
  print "Detected falling edge on channel %i at %f duration %f".format(channel, buttRisingTime, buttDuration)
  if buttDuration > longPressTime:
    longPressWaiting = True
    numLongPresses += 1
  else:
    shortPressWaiting = True
    numShortPresses += 1

#################################
#             MAIN              #
#################################

alarm = subprocess.Popen(["mplayer", "-volume", str(volume), "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
time.sleep(5)
alarm.terminate()

player = subprocess.Popen(["mplayer", "-volume", "-1", "-volstep", str(volumeStep), "-loop", "0", "-really-quiet", musicDir+songs[randSong]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
time.sleep(10)

while exitFlag==0:

  if (time.time()-lastTime >= timeIncVol):  #increase volume
    if(volume<maxVol):
      player.stdin.write('0')
      player.stdin.flush()
      lastTime = time.time()
      volume = volume+volumeStep

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
          volume = volume-volumeStep

      if(snooze >= snoozeTimes):            #exit, snoozed
        player.terminate()
        exitFlag=1
        alarm = subprocess.Popen(["mplayer", "-volume", "75", "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        time.sleep(6)
        alarm.terminate()

    snooze = 0                              #reset counter

  if (time.time()-startTime > 600):         #exit program, too long
    player.terminate()
    exitFlag=1

#EOF#
