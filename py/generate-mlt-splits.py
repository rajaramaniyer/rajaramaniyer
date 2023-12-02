import sys
import os
from os import path
import glob
import wave, struct, contextlib
import uuid
import datetime, time, math
import re
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

if len(sys.argv) != 2:
    label_file_name = input ("Label File Name: ")
else:
    label_file_name = sys.argv[1]

if path.exists(label_file_name):
    f=open(label_file_name)
    labels = f.readlines()
    f.close()
else:
    input ("Label File Name does not exists: " + label_file_name)
    sys.exit()

f=open("sankrit.txt", "r", encoding="UTF-8")
stext=f.readlines()
f.close()

f=open("tamil.txt", "r", encoding="UTF-8")
ttext=f.readlines()
f.close()

block1=[]
block2=[]

line=0
producerId=1
filterId=0
prevSlideDuration="00:00:00.000"
for label in labels:
    mm=0
    hh=0
    durationParts = label.split("\t")
    originalSeconds=float(durationParts[0])
    #print("originalSeconds = {originalSeconds}".format(originalSeconds=originalSeconds))
    mm=math.floor(originalSeconds/60)
    hh=math.floor(originalSeconds/60/60)
    #print("mm = {mm}".format(mm=mm))
    #print("hh = {hh}".format(hh=hh))
    seconds=originalSeconds-float(mm*60)
    #print("seconds = {seconds}".format(seconds=seconds))
    mm=mm-(hh*60)
    #print("mm = {mm}".format(mm=mm))
    roundSeconds=math.floor(seconds)
    microframes=(math.floor((seconds-roundSeconds)*1000/25)*25)-25
    if microframes < 0:
        microframes = 600 + microframes
        roundSeconds -= 1
    slideduration="%02.0f:%02.0f:%02.0f.%03.0f" %(hh, mm, roundSeconds, microframes)

    block1.append('  <producer id="producer{id}" in="00:00:00.000" out="03:59:59.960">'.format(id=producerId))
    block1.append('    <property name="length">04:00:00.000</property>')
    block1.append('    <property name="eof">pause</property>')
    block1.append('    <property name="resource">c:/Users/rajar/Pictures/govinda-dhasyam.png</property>')
    block1.append('    <property name="ttl">1</property>')
    block1.append('    <property name="aspect_ratio">1</property>')
    block1.append('    <property name="progressive">1</property>')
    block1.append('    <property name="seekable">1</property>')
    block1.append('    <property name="mlt_service">qimage</property>')
    block1.append('    <property name="creation_time">2022-02-04T02:37:15</property>')
    block1.append('    <property name="xml">was here</property>')
    block1.append('    <property name="shotcut:hash">3f67fb7361d49331f0441c800d628387</property>')
    block1.append('    <property name="shotcut:caption">govinda-dhasyam.png</property>')
    block1.append('    <filter id="filter{id}" in="{inVal}" out="{outVal}">'.format(id=filterId,inVal=prevSlideDuration,outVal=slideduration))
    block1.append('      <property name="background">color:#00000000</property>')
    block1.append('      <property name="mlt_service">affine</property>')
    block1.append('      <property name="shotcut:filter">affineSizePosition</property>')
    block1.append('      <property name="transition.fill">1</property>')
    block1.append('      <property name="transition.distort">0</property>')
    block1.append('      <property name="transition.rect">-840 -100 2400 1350 1</property>')
    block1.append('      <property name="transition.valign">middle</property>')
    block1.append('      <property name="transition.halign">center</property>')
    block1.append('      <property name="shotcut:animIn">00:00:00.000</property>')
    block1.append('      <property name="shotcut:animOut">00:00:00.000</property>')
    block1.append('      <property name="transition.threads">0</property>')
    block1.append('      <property name="transition.fix_rotate_x">0</property>')
    block1.append('    </filter>')
    block1.append('    <filter id="filter{id}" in="{inVal}" out="{outVal}">'.format(id=(filterId+1),inVal=prevSlideDuration,outVal=slideduration))
    block1.append('      <property name="argument">{text}</property>'.format(text=stext[line].rstrip('\n')))
    block1.append('      <property name="geometry">0 0 1920 1080 1</property>')
    block1.append('      <property name="family">Sanskrit Text</property>')
    block1.append('      <property name="size">106</property>')
    block1.append('      <property name="weight">500</property>')
    block1.append('      <property name="style">normal</property>')
    block1.append('      <property name="fgcolour">#ffffffff</property>')
    block1.append('      <property name="bgcolour">#00000000</property>')
    block1.append('      <property name="olcolour">#aa000000</property>')
    block1.append('      <property name="pad">0</property>')
    block1.append('      <property name="halign">right</property>')
    block1.append('      <property name="valign">bottom</property>')
    block1.append('      <property name="outline">3</property>')
    block1.append('      <property name="mlt_service">dynamictext</property>')
    block1.append('      <property name="shotcut:filter">dynamicText</property>')
    block1.append('      <property name="shotcut:usePointSize">1</property>')
    block1.append('      <property name="shotcut:animIn">00:00:00.000</property>')
    block1.append('      <property name="shotcut:animOut">00:00:00.000</property>')
    block1.append('      <property name="shotcut:pointSize">80</property>')
    block1.append('    </filter>')
    block1.append('    <filter id="filter{id}" in="{inVal}" out="{outVal}">'.format(id=(filterId+2),inVal=prevSlideDuration,outVal=slideduration))
    block1.append('      <property name="argument">{text}</property>'.format(text=ttext[line].rstrip('\n')))
    block1.append('      <property name="geometry">0 0 1920 1080 1</property>')
    block1.append('      <property name="family">Sanskrit Text</property>')
    block1.append('      <property name="size">93</property>')
    block1.append('      <property name="weight">500</property>')
    block1.append('      <property name="style">normal</property>')
    block1.append('      <property name="fgcolour">#ffffffff</property>')
    block1.append('      <property name="bgcolour">#00000000</property>')
    block1.append('      <property name="olcolour">#aa000000</property>')
    block1.append('      <property name="pad">0</property>')
    block1.append('      <property name="halign">right</property>')
    block1.append('      <property name="valign">top</property>')
    block1.append('      <property name="outline">3</property>')
    block1.append('      <property name="mlt_service">dynamictext</property>')
    block1.append('      <property name="shotcut:filter">dynamicText</property>')
    block1.append('      <property name="shotcut:usePointSize">1</property>')
    block1.append('      <property name="shotcut:animIn">00:00:00.000</property>')
    block1.append('      <property name="shotcut:animOut">00:00:00.000</property>')
    block1.append('      <property name="shotcut:pointSize">70</property>')
    block1.append('    </filter>')
    block1.append('  </producer>')

    block2.append('  <entry producer="producer{id}" in="{inVal}" out="{outVal}"/>'.format(id=producerId,inVal=prevSlideDuration,outVal=slideduration))

    prevSlideDuration=slideduration
    producerId += 1
    filterId += 3
    line += 1

f=open("a.txt","w",encoding="UTF-8")
for block in block1:
    f.write(block)
    f.write('\n')
f.write('\n\n\n')
for block in block2:
    f.write(block)
    f.write('\n')
f.close()
