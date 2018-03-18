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


print('hello, world!')
test = "/home/eleven/Music/coldplay-cemeteriesOfLondon.mp3"

player = subprocess.Popen(["mplayer", "-volume 0", test], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

time.sleep(5)
player.terminate()

print('again!')

