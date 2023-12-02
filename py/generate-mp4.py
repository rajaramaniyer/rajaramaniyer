from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import glob
import os
import sys
from os import path

def get_lines(filename):
    file = open(filename, 'r', encoding="UTF-8")
    Lines = file.readlines()
    file.close()
    return Lines

#
# Main Code Starts
#
canto="1"
if len(sys.argv) < 2:
  file_dashakam_number=""
  if path.exists("dashakam_number.txt"):
    f=open("dashakam_number.txt")
    file_dashakam_number = f.readlines()[0]
    f.close()
  dashakam_number = input ("Dashakam Number?(" + file_dashakam_number + "): ")
  if dashakam_number == "" and file_dashakam_number != "":
    dashakam_number = file_dashakam_number
else:
  dashakam_number = sys.argv[1]
f=open("dashakam_number.txt", "w")
f.write(dashakam_number)
f.close()

ASTRING='Narayaneeyam-' + dashakam_number.zfill(3)

wavefilename="c:/Users/rajar/Documents/Thirupavai/Exported/Narayaneeyam/Narayaneeyam-" + dashakam_number.zfill(3) + ".wav"
if not os.path.exists(wavefilename):
    input(wavefilename + " does not exists")
    sys.exit()

# Get a list of all the images
images = glob.glob(ASTRING + "-Slide????.jpg")

# Sort the images by filename
images.sort()

print("slide count = %d" % len(images))

labelTrackFile=ASTRING + '.txt'
if not os.path.exists(labelTrackFile):
    input(labelTrackFile + " does not exists")
    sys.exit()

labels=get_lines(labelTrackFile)

print("label count = %d" % len(labels))

# Set the duration of each image
clips=[]
i=0
prev_value=0
distance=0
for image in images:
    duration = 3 # 3 seconds
    if i < len(labels):
        label=labels[i].split('\t')
        label_value=float(label[0])
        duration = float("%0.1f" % (label_value - prev_value))
        prev_value=label_value
        i+=1
    # print("Slide = %s, duration = %02.1f, time = %02d:%0.2f" % (image, duration, distance/60, distance%60))
    distance+=duration
    clip=ImageClip(image, duration=duration)
    clips.append(clip)

video=concatenate_videoclips(clips)
audio = AudioFileClip(wavefilename)
video = video.set_audio(audio)

# Save the video
video.write_videofile(ASTRING + ".mp4", fps=1)
