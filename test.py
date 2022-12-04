import sys
import os
from os import path
import glob
import wave, contextlib
import uuid
import datetime, time, math
import re
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

fname="c:/Users/rajar/Documents/Thirupavai/Exported/Bhagavatham/10-51.wav"
with contextlib.closing(wave.open(fname,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    durationSeconds = frames / float(rate)
    roundSeconds=math.floor(durationSeconds)
    microframes=(math.ceil((durationSeconds-roundSeconds)*1000/25)*25)/1000
    print("frames {} rate {} durationSeconds {} roundSeconds {} microframes {}".format(frames,rate,durationSeconds,roundSeconds,microframes))
    hours = durationSeconds // 3600
    minutes = (durationSeconds % 3600) // 60
    seconds = (durationSeconds % 60)
    print("%02d:%02d:%02d" % (hours,minutes,seconds))
