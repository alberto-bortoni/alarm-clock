#! /usr/bin/python

import mpylayer
import os
import time
import subprocess
from subprocess import PIPE, STDOUT
import shlex
print('hello, world!')

#os.system('mpg123 ~/Music/coldplay-cemeteriesOfLondon.mp3 &')

player = subprocess.Popen(["mplayer", "/home/eleven/Music/coldplay-cemeteriesOfLondon.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#player = subprocess.Popen(["mpg123", "-C", "/home/eleven/Music/coldplay-cemeteriesOfLondon.mp3"], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
#player = subprocess.Popen(["mpg123", "/home/eleven/Music/coldplay-cemeteriesOfLondon.mp3"])
time.sleep(5)
#player.terminate()
#player.stdin.write("pause")
#player.stdin.flush()

print('again!')

#mp = mpylayer.MPlayerControl()
#mp.loadfile('~/Music/coldplay-cemeteriesOfLondon.mp3')
#mp.volume = 70


#dummy = input()


while True:
  dummy = input()

  if dummy == 1:
    print('ta')
    player.terminate()
    print('ta')
  if dummy == 2:
    print ('ts')
    player.stdin.write('p')
    #print player.stdout.read()
    #player.stdin.close()
    #stdout, stderr = player.communicate(input="s")[0]
    player.stdin.flush()
  if dummy == 3:
    print ('ts')
    player.stdin.write('9')
    print(player.stdout.readline())
    player.stdin.flush()
  if dummy == 4:
    player.stdin.write('0')
    player.stdin.flush()

#mgp123 ~/Music/coldplay-cementeriesOfLondon.mp3

#print('done')
