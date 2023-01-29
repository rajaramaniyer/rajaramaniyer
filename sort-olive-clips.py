#!/opt/homebrew/opt/python@3.9/libexec/bin/python

from operator import inv
from os import path
import sys
import re

def get_lines(filename):
  file = open(filename, 'r', encoding="UTF-8")
  Lines = file.readlines()
  file.close()
  return Lines

def get_key(clip):
    direction=' '
    if clip['track_number'] >= 0:
        direction='+'
    return direction + str(abs(clip['track_number'])).rjust(2,'0') + '-' + str(abs(clip['in_value'])).rjust(10,'0')

def sort_clip_array(clip_array):
    sorted_clips=[]
    i=0
    clip_array.sort(key=lambda x: x['track_number'])

    new_clip_array = []
    sub_clip_array = []
    prev_track_number=None
    for clip in clip_array:
        if prev_track_number != clip['track_number']:
            if prev_track_number != None:
                sub_clip_array.sort(key=lambda x: x['in_value'])
                for sclip in sub_clip_array:
                    new_clip_array.append(sclip)
            sub_clip_array = []
        prev_track_number = clip['track_number']
        sub_clip_array.append(clip)
    if prev_track_number != None:
        sub_clip_array.sort(key=lambda x: x['in_value'])
        for sclip in sub_clip_array:
            new_clip_array.append(sclip)

    for clip in new_clip_array:
        clip['body'][0] = re.sub('id="\d+"', 'id="%d"' % i, clip['body'][0])
        sorted_clips.append(clip['body'])
        i += 1
    return sorted_clips
#
# Main Code Starts
#
if len(sys.argv) != 2:
  olive_file_name=input("OveFileName: ")
else:
  olive_file_name=sys.argv[1]

olive_file_lines = get_lines(olive_file_name)

clip_array = []

found_clip=False
current_clip=-1
file=open(olive_file_name.replace('.ove', '-sorted.ove'), 'w', encoding='utf-8')
for line in olive_file_lines:
    if "<clip" in line:
        found_clip=True
        current_clip += 1

        about_clip = {}
        rr=re.search(r"track=\"((-)?\d+)\"",line)
        about_clip['track_number']=int(rr.group(1))
        rr=re.search(r"in=\"(\d+)\" out=\"(\d+)\"",line)
        about_clip['in_value'] = int(rr.group(1))
        about_clip['out_value'] = int(rr.group(2))
        about_clip['body'] = []
        clip_array.append(about_clip)
    #
    if found_clip and "</sequence>" in line:
        found_clip=False
    #
    if found_clip:
        clip_array[current_clip]['body'].append(line)
    else:
        if current_clip != -1:
            sorted_clips = sort_clip_array(clip_array)
            for clip in sorted_clips:
                for l in clip:
                    file.write(l)
            current_clip = -1
    #
    if found_clip == False and current_clip == -1:
        file.write(line)
file.close()
