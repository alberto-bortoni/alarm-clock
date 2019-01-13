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

longPressTime = 1
timeIncVol = 5
timeButt = 2
snoozeInc = 2
volume = 10
volumeStep = 2
maxVol = 110
medVol = 90
minVol = 30

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
buttSequence = "" # empty sequence

#################################
#         GPIO INIT             #
#################################
def butt_callback(channel):
  global buttSequence, buttRisingTime, buttFallingTime, buttDuration, longPressTime, longPressWaiting, shortPressWaiting, numLongPresses,numShortPresses
  buttValue = GPIO.input(channel)
  if buttValue:
    buttFallingTime = time.time()
    buttDuration = (buttFallingTime - buttRisingTime) if buttRisingTime is not None else None
  else:
    buttFallingTime = None
    buttDuration = None
    buttRisingTime = time.time()

  print "Detected edge {} on channel {} at {} duration {}".format(buttValue, channel, buttRisingTime, buttDuration)
  if buttDuration > longPressTime:
    print "LONG PRESS"
    longPressWaiting = True
    numLongPresses += 1
    buttSequence += 'l'

  elif buttDuration is not None:
    shortPressWaiting = True
    numShortPresses += 1
    buttSequence += 's'
    print "SHORT PRESS {}".format(numShortPresses)

  print 'Sequence: {}'.format(buttSequence)

GPIO.setmode(GPIO.BCM)
GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(butt, GPIO.BOTH, callback=butt_callback)  # add rising edge detection on a channel

#################################
#       VOLUME CONTROLS         #
#################################
def increase_volume():
  global volume, player, maxVol
  if (volume < maxVol):
    volume = volume + volumeStep
    print "Increasing volume to {}".format(volume)
    player.stdin.write('0')
    player.stdin.flush()

def decrease_volume():
  global volume, player, minVol
  if (volume > minVol):
    volume = volume - volumeStep
    print "Decreasing volume to {}".format(volume)
    player.stdin.write('9')
    player.stdin.flush()

#################################
#             MAIN              #
#################################

alarm = subprocess.Popen(["mplayer", "-volume", str(volume), "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
time.sleep(5)
alarm.terminate()

player = subprocess.Popen(["mplayer", "-volume", "-1", "-volstep", str(volumeStep), "-loop", "0", "-really-quiet", musicDir+songs[randSong]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
time.sleep(10)

exitSequence = 'sslssl' #button press sequence for shutting off alarm

while exitFlag==0:
  if (time.time()-lastTime >= timeIncVol):  #increase volume
    lastTime = time.time()
    increase_volume()

  if(longPressWaiting or shortPressWaiting):                  #start snooze/exit
    decrease_volume()                       #reduce noise every button

    if(exitSequence in buttSequence):            #exit, snoozed
      print "Exit Sequence Activated"
      player.terminate()
      exitFlag=1
      alarm = subprocess.Popen(["mplayer", "-volume", "75", "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
      time.sleep(6)
      alarm.terminate()

  if (time.time()-startTime > 600):         #exit program, too long
    player.terminate()
    exitFlag=1

#EOF#
