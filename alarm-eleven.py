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

# first disable the shutdown routine
subprocess.call(["/etc/init.d/listen-for-shutdown.sh", "stop"])

#################################
#          VARIABLES            #
#################################

#times in seconds
longPressTime     = 3
termLongTime      = 600
timeIncVol        = 5
startTime         = time.time()
lastTime          = time.time()
buttRisingTime    = None
buttFallingTime   = None
buttDuration      = None
longPressWaiting  = False
shortPressWaiting = False

#player volume
volume        = 10
volumeStep    = 2
maxVol        = 110
minVol        = 30

#hardware pin number for button
butt          = 13

#song related stuff
musicDir = "/home/eleven/Music/"
songs    = os.listdir(musicDir)
songsNum = len(songs)
randSong = randint(1, songsNum)-1

#button press sequence for shutting off alarm
exitSequence = 'sslssl'
exitFlag      = 0
snooze        = 0
numLongPresses    = 0
numShortPresses   = 0
buttSequence      = "" # empty sequence
prevBttnState = False

#################################
#           GPIO INIT           #
#################################

# gets called whenever there is a change in the button input
# detects rising or falling edge and records the duration of the press
# categorizes it as a short or long press according to pre determiend values above
def butt_callback(channel):
  global buttSequence, buttRisingTime, buttFallingTime, buttDuration, longPressTime, longPressWaiting, shortPressWaiting, numLongPresses, numShortPresses, prevBttnState
  buttValue = GPIO.input(channel)

  if buttValue and prevBttnState:
    prevBttnState   = False
    buttFallingTime = time.time()
    buttDuration    = (buttFallingTime - buttRisingTime) if buttRisingTime is not None else None

    print "Detected edge {} on channel {} at {} duration {}".format(buttValue, channel, buttRisingTime, buttDuration)

    if buttDuration > longPressTime:
      longPressWaiting   = True
      numLongPresses    += 1
      buttSequence      += 'l'
      print "LONG PRESS {}".format(numLongPresses)

    elif buttDuration is not None:
      shortPressWaiting  = True
      numShortPresses   += 1
      buttSequence      += 's'
      print "SHORT PRESS {}".format(numShortPresses)


    buttFallingTime = None
    buttDuration    = None
    buttRisingTime  = None
    print 'Sequence: {}'.format(buttSequence)

  else:
    prevBttnState   = True
    buttFallingTime = None
    buttDuration    = None
    buttRisingTime  = time.time()

# activates the GIPO on the Raspi as a pullup mode and defines its callback function
# add rising edge detection on a channel
GPIO.setmode(GPIO.BCM)
GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(butt, GPIO.BOTH, callback=butt_callback, bouncetime=100)

#################################
#       VOLUME CONTROLS         #
#################################

# increases volume by sending a character command to mplayer
# 0 is mplayer's command to increase
def increase_volume():
  global volume, player, maxVol
  if (volume < maxVol):
    volume = volume + volumeStep
    print "Increasing volume to {}".format(volume)
    player.stdin.write('0')
    player.stdin.flush()

# decreases volume by sending a character command to mplayer
# 9 is mplayer's command to decrease
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

# initialize mplayer with prefered condigurations and introduce a delay to allow it to boot correctly
# kill the subprocess after. This is a workaround to allow mplayer to actually start volume at the command sent
# otherwise it actually does not.
alarm = subprocess.Popen(["mplayer", "-volume", str(volume), "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
time.sleep(5)
alarm.terminate()

# boot player once again with the prefered commands, and random song, and now it will init as indicated
# delay to allow player to finalize initialization
player = subprocess.Popen(["mplayer", "-volume", "-1", "-volstep", str(volumeStep), "-loop", "0", "-really-quiet", musicDir+songs[randSong]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
time.sleep(10)


while exitFlag==0:
  # increase volume periodially as per timeIncVol
  if (time.time()-lastTime >= timeIncVol):
    lastTime = time.time()
    increase_volume()

  # if user presses button, either short or long, decrease volume
  if(longPressWaiting or shortPressWaiting):
    longPressWaiting  = False
    shortPressWaiting = False
    decrease_volume()

    # if the exit sequence is found in the string of button presses, start to exit
    # kill the current song and start a new player with the end alarm sound
    if(exitSequence in buttSequence):            #exit, snoozed
      print "Exit Sequence Activated"
      player.terminate()
      exitFlag = 1
      alarm = subprocess.Popen(["mplayer", "-volume", "75", "-really-quiet", "/home/eleven/Alarms/Alarm03.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
      time.sleep(6)
      alarm.terminate()

  # after a long time, terminate the program
  if (time.time()-startTime > termLongTime):
    player.terminate()
    exitFlag = 1


# first disable the shutdown routine
subprocess.call(["/etc/init.d/listen-for-shutdown.sh", "start"])

#EOF#
