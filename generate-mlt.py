import sys
import os
import glob
import wave, struct
import uuid
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def getTimeString(totalmilliseconds):
    milliseconds=str(round(totalmilliseconds)%1000).zfill(3)
    hours=str(round(totalmilliseconds/1000/60/60)).zfill(2)
    minutes=str(round((totalmilliseconds/1000/60)%60)).zfill(2)
    seconds=str(round((totalmilliseconds/1000)%60)).zfill(2)
    return "{hours}:{minutes}:{seconds}.{milliseconds}".format(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

#
# Main Code Starts
#
if len(sys.argv) != 2:
  adyayam_number = input ("Adhyayam Number: ")
else:
  adyayam_number=sys.argv[1]

wavefilename="c:/Users/rajar/Documents/Thirupavai/Exported/Bhagavatham/10-" + str(adyayam_number) + ".wav"

wavefile = wave.open(wavefilename, 'rb')
channels = wavefile.getnchannels()
frames = wavefile.getnframes()
rate = wavefile.getframerate()
durationMilliSeconds = round(frames / float(rate) * 1000)
duration=getTimeString(durationMilliSeconds)
sampwidth = wavefile.getsampwidth()
#data = wavefile.readframes(frames) #read the all the samples from the file into a byte string
audioframes=round(frames / float(rate) * 25)
wavefile.close()

file1 = open('c:/Users/rajar/Documents/Thirupavai/Bhagavatham.tracktionedit', 'r')
lines = file1.readlines()
file1.close()
mydoc = []
startFound=False
for line in lines:
    if "<MARKERTRACK" in line.strip():
        startFound = True
    if startFound:
        mydoc.append(line)
    if "</MARKERTRACK" in line.strip():
        startFound = False

markers = parseString('\n'.join(mydoc)).getElementsByTagName('MARKERCLIP')

block1=[]
block2=[]
block3=[]
block4=[]
block2.append('  <playlist id="main_bin" title="Shotcut version 21.06.29">\n')
block2.append('    <property name="shotcut:projectAudioChannels">2</property>\n')
block2.append('    <property name="shotcut:projectFolder">0</property>\n')
block2.append('    <property name="xml_retain">1</property>\n')
#
block4.append('  <playlist id="playlist0">\n')
block4.append('    <property name="shotcut:video">1</property>\n')
block4.append('    <property name="shotcut:name">V1</property>\n')

id=0
files=glob.glob("Slide????.jpg")

equalslideduration=getTimeString(durationMilliSeconds/len(files))
prevmarker=0
for slidename in files:
    #
    if id < len(markers):
        marker=float(markers[id].attributes["start"].value)
        print("marker={:},prevmarker={:}".format(marker,prevmarker))
        slideduration=getTimeString((marker-prevmarker)*1000)
        prevmarker=marker
    else:
        slideduration=equalslideduration    
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
    block1.append('    <property name="shotcut:hash">{hashvalue}</property>\n'.format(hashvalue=hashvalue))
    block1.append('    <property name="creation_time">2021-07-10T13:27:34</property>\n')
    block1.append('    <property name="xml">was here</property>\n')
    block1.append('  </producer>\n')
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
    block4.append('    <entry producer="producer{id}" in="00:00:00.000" out="{slideduration}"/>\n'.format(id=id+len(files),slideduration=slideduration))
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
block4.append('  <chain id="chain0" out="{duration}">\n'.format(duration=duration))
block4.append('    <property name="length">{audioframes}</property>\n'.format(audioframes=audioframes))
block4.append('    <property name="eof">pause</property>\n')
block4.append('    <property name="resource">{wavefilename}</property>\n'.format(wavefilename=wavefilename))
block4.append('    <property name="mlt_service">avformat-novalidate</property>\n')
block4.append('    <property name="seekable">1</property>\n')
block4.append('    <property name="audio_index">0</property>\n')
block4.append('    <property name="video_index">-1</property>\n')
block4.append('    <property name="mute_on_pause">0</property>\n')
block4.append('    <property name="shotcut:hash">b3bca2344e8bcab5d610cfc6ece30f2f</property>\n')
block4.append('    <property name="shotcut:caption">{wavefilename}</property>\n'.format(wavefilename=os.path.basename(wavefilename)))
block4.append('  </chain>\n')
block4.append('  <playlist id="playlist1">\n')
block4.append('    <property name="shotcut:audio">1</property>\n')
block4.append('    <property name="shotcut:name">A1</property>\n')
block4.append('    <entry producer="chain0" in="00:00:00.000" out="{duration}"/>\n'.format(duration=duration))
block4.append('  </playlist>\n')
block4.append('  <tractor id="tractor0" title="Shotcut version 21.06.29" in="00:00:00.000" out="{duration}">\n'.format(duration=duration))
block4.append('    <property name="shotcut">1</property>\n')
block4.append('    <property name="shotcut:projectAudioChannels">2</property>\n')
block4.append('    <property name="shotcut:projectFolder">0</property>\n')
block4.append('    <property name="shotcut:scaleFactor">1.41493</property>\n')
block4.append('    <track producer="background"/>\n')
block4.append('    <track producer="playlist0"/>\n')
block4.append('    <track producer="playlist1" hide="video"/>\n')
block4.append('    <transition id="transition0">\n')
block4.append('      <property name="a_track">0</property>\n')
block4.append('      <property name="b_track">1</property>\n')
block4.append('      <property name="mlt_service">mix</property>\n')
block4.append('      <property name="always_active">1</property>\n')
block4.append('      <property name="sum">1</property>\n')
block4.append('    </transition>\n')
block4.append('    <transition id="transition1">\n')
block4.append('      <property name="a_track">0</property>\n')
block4.append('      <property name="b_track">1</property>\n')
block4.append('      <property name="version">0.9</property>\n')
block4.append('      <property name="mlt_service">frei0r.cairoblend</property>\n')
block4.append('      <property name="threads">0</property>\n')
block4.append('      <property name="disable">1</property>\n')
block4.append('    </transition>\n')
block4.append('    <transition id="transition2">\n')
block4.append('      <property name="a_track">0</property>\n')
block4.append('      <property name="b_track">2</property>\n')
block4.append('      <property name="mlt_service">mix</property>\n')
block4.append('      <property name="always_active">1</property>\n')
block4.append('      <property name="sum">1</property>\n')
block4.append('    </transition>\n')
block4.append('  </tractor>\n')
block4.append('</mlt>\n')

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
filename="adhyayam" + str(adyayam_number) + ".mlt"
f = open(filename, "w")

f.write('<?xml version="1.0" standalone="no"?>\n')
f.write('<mlt LC_NUMERIC="C" version="7.1.0" title="Shotcut version 21.06.29" producer="main_bin">\n')
f.write('  <profile description="PAL 4:3 DV or DVD" width="1920" height="1080" progressive="1" sample_aspect_num="1" sample_aspect_den="1" display_aspect_num="16" display_aspect_den="9" frame_rate_num="25" frame_rate_den="1" colorspace="709"/>\n')

for block in block1:
    f.write(block)
for block in block2:
    f.write(block)
for block in block3:
    f.write(block)
for block in block4:
    f.write(block)
f.close();