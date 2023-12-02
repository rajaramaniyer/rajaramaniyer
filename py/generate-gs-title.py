import sys
import os
import os.path
from os import path
import time
import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def get_lines(filename):
  file = open(filename, 'r', encoding="UTF-8")
  Lines = file.readlines()
  file.close()
  return Lines

#
# Main Code Starts
#
if len(sys.argv) < 2:
  song_number=int(input("Song Number: "))
else:
  song_number=int(sys.argv[1])
SONG_PREFIX="GS" + str(song_number).zfill(3)
USERPROFILE=os.environ['USERPROFILE']
RSFOLDER=USERPROFILE + "\\books\\srisrianna\\radhikashathakam\\"
index_file=RSFOLDER + "index.txt"

if not path.exists(index_file):
  input("Index file does not exists. " + index_file)
  sys.exit()

index_lines=get_lines(index_file)
if len(index_lines) < (song_number):
  input("Index file does not have title for song " + str(song_number))
  sys.exit()
title_meta=index_lines[song_number-1].rstrip("\n").split("|")
raga_meta=title_meta[1].split(" - ")

title_text = title_meta[0].rstrip(" ") + " | " + raga_meta[0].lstrip(" ") + " | " + str(song_number).zfill(3) + " Govinda Shathakam"
desc_text = """
#GovindaShatakam #SriSriAnna #MythiliRajaraman

Song %d: %s
Ragam: %s
Talam: %s
Composed by: Sri Sri Krishnapremi Swamigal

Part of this playlist: https://www.youtube.com/playlist?list=PLdBTiOEoG70n_aTSZgIGi3pOtyO7D2Tky
""" % (song_number,title_meta[0],raga_meta[0],raga_meta[1])

print(title_text)
print(desc_text)

time.sleep(60)
