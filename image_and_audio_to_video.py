#!/opt/homebrew/opt/python@3.9/libexec/bin/python

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import glob

def get_lines(filename):
    file = open(filename, 'r', encoding="UTF-8")
    Lines = file.readlines()
    file.close()
    return Lines

# Path to the audio file
audio_file = "/Users/rajaramaniyer/Documents/Waveform/Exported/VS-01-01.wav"

# Get a list of all the images
images = glob.glob("/Users/rajaramaniyer/books/Slide????.png")

# Sort the images by filename
images.sort()

print("images count = %d" % len(images))

labels=get_lines('/Users/rajaramaniyer/Movies/VS-01-01.txt')

print("labels count = %d" % len(labels))

# # Set the duration of each image
clips=[]
i=0
prev_value=0
distance=0
for image in images:
    duration = 3 # 3 seconds
    if i < len(labels):
        label_value=float(labels[i].split('\t')[0])
        duration = float("%0.1f" % (label_value - prev_value))
        prev_value=label_value
        i+=1
    # print("Slide = %s, duration = %02.1f, time = %02d:%0.2f" % (image, duration, distance/60, distance%60))
    distance+=duration
    clip=ImageClip(image, duration=duration)
    clips.append(clip)

video=concatenate_videoclips(clips)
audio = AudioFileClip(audio_file)
video = video.set_audio(audio)

# # Save the video
video.write_videofile("/Users/rajaramaniyer/Movies/VS-01-01.mp4",fps=1)
