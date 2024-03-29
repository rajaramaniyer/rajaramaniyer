import sys
import os
from os import path
import glob
import wave, contextlib
import uuid
import time, math
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import subprocess

def getTimeString(totalmilliseconds):
    milliseconds=str(math.floor(totalmilliseconds)%1000).zfill(3)
    hours=str(math.floor(totalmilliseconds/1000/60/60)).zfill(2)
    minutes=str(math.floor((totalmilliseconds/1000/60)%60)).zfill(2)
    seconds=str(math.floor((totalmilliseconds/1000)%60)).zfill(2)
    return "{hours}:{minutes}:{seconds}.{milliseconds}".format(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

#
# Main Code Starts
#
canto="1"
if len(sys.argv) != 2:
  file_adyayam_number=""
  if path.exists("adyayam_number.txt"):
    f=open("adyayam_number.txt")
    file_adyayam_number = f.readlines()[0]
    f.close()
  adyayam_number = input ("Canto " + canto.zfill(2) + " Adhyayam Number?(" + file_adyayam_number + "): ")
  if adyayam_number == "" and file_adyayam_number != "":
    adyayam_number = file_adyayam_number
else:
  adyayam_number = sys.argv[1]
f=open("adyayam_number.txt", "w")
f.write(adyayam_number)
f.close()

ASTRING='SB-' + canto.zfill(2) + '-' + adyayam_number.zfill(2)

wavefilename="c:/Users/rajar/Documents/Thirupavai/Exported/Bhagavatham/"+canto.zfill(2)+"-" + adyayam_number.zfill(2) + ".wav"
if not os.path.exists(wavefilename):
    input(wavefilename + " does not exists")
    sys.exit()

duration="00:00:00.000"
durationSeconds=0.0
with contextlib.closing(wave.open(wavefilename,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    durationMilliSeconds = round(float(frames) / float(rate) * 1000.0)
    duration = getTimeString(durationMilliSeconds)

labelTrackFile=ASTRING + '.txt'
if not os.path.exists(labelTrackFile):
    input(labelTrackFile + " does not exists")
    sys.exit()

file1 = open(labelTrackFile, 'r')
labelTrack = file1.readlines()
file1.close()

audioHash=uuid.uuid4().hex

tractor_id=0
transition_id=0

block1=[]
block2=[]
block3=[]
block4=[]
block2.append('  <playlist id="main_bin">\n')
block2.append('    <property name="xml_retain">1</property>\n')
block2.append('    <entry producer="chain0" in="00:00:00.000" out="{}"/>\n'.format(duration))
#
block4.append('  <playlist id="playlist0">\n')
block4.append('    <property name="shotcut:video">1</property>\n')
block4.append('    <property name="shotcut:name">V1</property>\n')

id=0
files=sorted(glob.glob(ASTRING + "-Slide????.jpg"))

if len(files) == 0:
    print("Slides are missing. run generate-ppt")
    input ("Press enter to continue...")

equalslideduration=getTimeString(round(durationMilliSeconds/len(files)))
if len(labelTrack) > 0 and len(files)-1 != len(labelTrack):
    if len(labelTrack) < len(files):
        prev=-1
        for label in labelTrack:
            durationParts = label.split("\t")
            if prev != -1 and prev != durationParts[0]:
                print("Line " + str(id+1) + " is having a break")
                break
            prev=durationParts[1]
            id+=1
    print("WARNING: labelTrack and slideCount are Not in sync.")
    print("There are %d labels while there are %d slides" %(len(labelTrack), len(files)))
    input ("Press enter to continue...")

id=0
currentTime=time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime())
prevmarker=0
prevlabelpos=0.0
for slidename in files:
    if id < len(labelTrack):
        durationParts = labelTrack[id].split("\t")
        mins=0
        if float(durationParts[1]) - float(durationParts[0]) == 0:
            seconds=float(durationParts[0])-prevlabelpos
            prevlabelpos=float(durationParts[0])
        else:
            seconds=float(durationParts[1]) - float(durationParts[0])
        roundSeconds=math.floor(seconds)
        microframes=(math.floor((seconds-roundSeconds)*1000/25)*25)-25
        if microframes < 0:
            microframes = 600 + microframes
            roundSeconds -= 1
        slideduration="00:%02.0f:%02.0f.%03.0f" %(mins, roundSeconds, microframes)
    else:
        slideduration=equalslideduration
    sd=slideduration.split(':')
    t=(float(sd[1])*60)+float(sd[2])-0.52
    tstart="00:%02.0f:%02.3f" %(int(t/60), t%60)
    #
    hashvalue=uuid.uuid4().hex
    #
    block1.append('  <producer id="producer{id}" in="00:00:00.000" out="03:59:59.960">\n'.format(id=id))
    block1.append('    <property name="length">04:00:00.000</property>\n')
    block1.append('    <property name="eof">pause</property>\n')
    block1.append('    <property name="resource">{slidename}</property>\n'.format(slidename=slidename))
    block1.append('    <property name="ttl">1</property>\n')
    block1.append('    <property name="aspect_ratio">1</property>\n')
    block1.append('    <property name="progressive">1</property>\n')
    block1.append('    <property name="seekable">1</property>\n')
    block1.append('    <property name="mlt_service">qimage</property>\n')
    block1.append('    <property name="creation_time">{currentTime}</property>\n'.format(currentTime=currentTime))
    block1.append('    <property name="shotcut:hash">{hashvalue}</property>\n'.format(hashvalue=hashvalue))
    block1.append('    <property name="xml">was here</property>\n')
    block1.append('  </producer>\n')

    if 'Slide0001' not in slidename:
        block1.append('  <tractor id="tractor{tractor_id}" in="00:00:00.000" out="00:00:00.520">\n'.format(tractor_id=tractor_id))
        block1.append('    <property name="shotcut:transition">lumaMix</property>\n')
        block1.append('    <track producer="producer{id}" in="{tstart}" out="{slideduration}"/>\n'.format(id=id-1,tstart=tstart,slideduration=slideduration))
        block1.append('    <track producer="producer{id}" in="00:00:00.000" out="00:00:00.520"/>\n'.format(id=id))
        block1.append('    <transition id="transition{transition_id}" out="00:00:00.520">\n'.format(transition_id=transition_id))
        block1.append('      <property name="a_track">0</property>\n')
        block1.append('      <property name="b_track">1</property>\n')
        block1.append('      <property name="factory">loader</property>\n')
        block1.append('      <property name="mlt_service">luma</property>\n')
        block1.append('      <property name="alpha_over">1</property>\n')
        block1.append('    </transition>\n')
        block1.append('    <transition id="transition{transition_id}" out="00:00:00.520">\n'.format(transition_id=transition_id+1))
        block1.append('      <property name="a_track">0</property>\n')
        block1.append('      <property name="b_track">1</property>\n')
        block1.append('      <property name="start">-1</property>\n')
        block1.append('      <property name="accepts_blanks">1</property>\n')
        block1.append('      <property name="mlt_service">mix</property>\n')
        block1.append('    </transition>\n')
        block1.append('  </tractor>\n')
        tractor_id+=1
        transition_id+=2

    #
    block2.append('    <entry producer="producer{id}" in="00:00:00.000" out="00:00:03.960"/>\n'.format(id=id))
    #
    block3.append('  <producer id="producer{id}" in="00:00:00.000" out="03:59:59.960">\n'.format(id=id+len(files)))
    block3.append('    <property name="length">04:00:00.000</property>\n')
    block3.append('    <property name="eof">pause</property>\n')
    block3.append('    <property name="resource">{slidename}</property>\n'.format(slidename=slidename))
    block3.append('    <property name="ttl">1</property>\n')
    block3.append('    <property name="aspect_ratio">1</property>\n')
    block3.append('    <property name="progressive">1</property>\n')
    block3.append('    <property name="seekable">1</property>\n')
    block3.append('    <property name="mlt_service">qimage</property>\n')
    block3.append('    <property name="shotcut:hash">{hashvalue}</property>\n'.format(hashvalue=hashvalue))
    block3.append('    <property name="creation_time">2021-07-10T13:27:34</property>\n')
    block3.append('    <property name="xml">was here</property>\n')
    block3.append('    <property name="shotcut:caption">{slidename}</property>\n'.format(slidename=slidename))
    block3.append('  </producer>\n')
    #
    block4.append('    <entry producer="producer{id}" in="00:00:00.000" out="{slideduration}"/>\n'.format(id=id+len(files),slideduration=tstart))
    block4.append('    <entry producer="tractor{tractor_id}" in="00:00:00.000" out="00:00:00.520"/>\n'.format(tractor_id=tractor_id))
    #
    id=id+1
#
block2.append('  </playlist>\n')
block2.append('  <producer id="black" in="00:00:00.000" out="{duration}">\n'.format(duration=duration))
block2.append('    <property name="length">{duration}</property>\n'.format(duration=duration))
block2.append('    <property name="eof">pause</property>\n')
block2.append('    <property name="resource">0</property>\n')
block2.append('    <property name="aspect_ratio">1</property>\n')
block2.append('    <property name="mlt_service">color</property>\n')
block2.append('    <property name="mlt_image_format">rgba</property>\n')
block2.append('    <property name="set.test_audio">0</property>\n')
block2.append('  </producer>\n')
block2.append('  <playlist id="background">\n')
block2.append('    <entry producer="black" in="00:00:00.000" out="{duration}"/>\n'.format(duration=duration))
block2.append('  </playlist>\n')
#
block4.append('  </playlist>\n')
block4.append('  <chain id="chain1" out="{duration}">\n'.format(duration=duration))
block4.append('    <property name="length">{duration}</property>\n'.format(duration=duration))
block4.append('    <property name="eof">pause</property>\n')
block4.append('    <property name="resource">{wavefilename}</property>\n'.format(wavefilename=wavefilename))
block4.append('    <property name="mlt_service">avformat-novalidate</property>\n')
block4.append('    <property name="seekable">1</property>\n')
block4.append('    <property name="audio_index">0</property>\n')
block4.append('    <property name="video_index">-1</property>\n')
block4.append('    <property name="mute_on_pause">0</property>\n')
block4.append('    <property name="shotcut:hash">{audioHash}</property>\n'.format(audioHash=audioHash))
block4.append('    <property name="shotcut:caption">{wavefilename}</property>\n'.format(wavefilename=os.path.basename(wavefilename)))
block4.append('  </chain>\n')
block4.append('  <playlist id="playlist1">\n')
block4.append('    <property name="shotcut:audio">1</property>\n')
block4.append('    <property name="shotcut:name">A1</property>\n')
block4.append('    <entry producer="chain1" in="00:00:00.000" out="{duration}"/>\n'.format(duration=duration))
block4.append('  </playlist>\n')
block4.append('  <tractor id="tractor{tractor_id}" title="Shotcut version 21.10.31" in="00:00:00.000" out="{duration}">\n'.format(tractor_id=tractor_id,duration=duration))
block4.append('    <property name="shotcut">1</property>\n')
block4.append('    <property name="shotcut:projectAudioChannels">2</property>\n')
block4.append('    <property name="shotcut:projectFolder">0</property>\n')
block4.append('    <track producer="background"/>\n')
block4.append('    <track producer="playlist0"/>\n')
block4.append('    <track producer="playlist1" hide="video"/>\n')
block4.append('    <transition id="transition{transition_id}">\n'.format(transition_id=transition_id))
block4.append('      <property name="a_track">0</property>\n')
block4.append('      <property name="b_track">1</property>\n')
block4.append('      <property name="mlt_service">mix</property>\n')
block4.append('      <property name="always_active">1</property>\n')
block4.append('      <property name="sum">1</property>\n')
block4.append('    </transition>\n')
block4.append('    <transition id="transition{transition_id}">\n'.format(transition_id=(transition_id+1)))
block4.append('      <property name="a_track">0</property>\n')
block4.append('      <property name="b_track">1</property>\n')
block4.append('      <property name="version">0.9</property>\n')
block4.append('      <property name="mlt_service">frei0r.cairoblend</property>\n')
block4.append('      <property name="threads">0</property>\n')
block4.append('      <property name="disable">1</property>\n')
block4.append('    </transition>\n')
block4.append('    <transition id="transition{transition_id}">\n'.format(transition_id=(transition_id+2)))
block4.append('      <property name="a_track">0</property>\n')
block4.append('      <property name="b_track">2</property>\n')
block4.append('      <property name="mlt_service">mix</property>\n')
block4.append('      <property name="always_active">1</property>\n')
block4.append('      <property name="sum">1</property>\n')
block4.append('    </transition>\n')
block4.append('  </tractor>\n')
block4.append('</mlt>\n')

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
filename=ASTRING + ".mlt"
f = open(filename, "w")

f.write('<?xml version="1.0" standalone="no"?>\n')
f.write('<mlt LC_NUMERIC="C" version="7.1.0" title="Shotcut version 21.10.31" producer="main_bin">\n')
f.write('  <profile description="PAL 4:3 DV or DVD" width="1920" height="1080" progressive="1" sample_aspect_num="1" sample_aspect_den="1" display_aspect_num="16" display_aspect_den="9" frame_rate_num="25" frame_rate_den="1" colorspace="709"/>\n')
f.write('  <chain id="chain0" out="{duration}">\n'.format(duration=duration))
f.write('    <property name="length">{duration}</property>\n'.format(duration=duration))
f.write('    <property name="eof">pause</property>\n')
f.write('    <property name="resource">{wavefilename}</property>\n'.format(wavefilename=wavefilename))
f.write('    <property name="mlt_service">avformat-novalidate</property>\n')
f.write('    <property name="seekable">1</property>\n')
f.write('    <property name="audio_index">0</property>\n')
f.write('    <property name="video_index">-1</property>\n')
f.write('    <property name="mute_on_pause">0</property>\n')
f.write('    <property name="xml">was here</property>\n')
f.write('    <property name="shotcut:hash">{audioHash}</property>\n'.format(audioHash=audioHash))
f.write('  </chain>\n')

for block in block1:
    f.write(block)
for block in block2:
    f.write(block)
for block in block3:
    f.write(block)
for block in block4:
    f.write(block)
f.close();

p = subprocess.Popen(["C:/Program Files/Shotcut/shotcut.exe", filename])
