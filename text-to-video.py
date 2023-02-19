#!/opt/homebrew/opt/python@3.9/libexec/bin/python

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def get_lines(filename):
    file = open(filename, 'r', encoding="UTF-8")
    Lines = file.readlines()
    file.close()
    return Lines

# Path to the audio file
audio_file = "/Users/rajaramaniyer/Documents/Waveform/Exported/VS-01-01.wav"
audio = AudioFileClip(audio_file)

# Get a list of all the images
background = "/Users/rajaramaniyer/books/background.png"
image_clip = ImageClip(background, duration=60)
# image_clip = ImageClip(background, duration=audio.duration)
# image_clip = image_clip.set_audio(audio)

labels=get_lines('/Users/rajaramaniyer/Movies/VS-01-01.txt')

print("labels count = %d" % len(labels))

textlines = get_lines("/Users/rajaramaniyer/Movies/sanskrit.txt")

# # Set the duration of each image
clips=[]
i=0
start_value=0
end_value=0
duration=0
lineheight=120
y=120
sublines=[]

for text in textlines:
    if len(text) <= 1:
        continue

    if len(sublines) == 8:
        duration = 0
        l = 0
        for subline in sublines:
            duration += subline[1]
        subclips=[]
        for subline in sublines:
            print (subline + (duration,))
            if l > 0:
                y = (lineheight * l) + 70
            else:
                y = 70
            clip = TextClip(subline[0], font='Devanagari-MT', color='silver', fontsize=90)
            clip = clip.set_start(subline[2])
            clip = clip.set_fps(1)
            clip = clip.set_duration(duration)
            clip = clip.set_position((70, y))
            subclips.append(clip)
            l+=1
            duration = float("%0.1f" % (duration - subline[1]))
        clips.append(CompositeVideoClip(subclips))
        sublines=[]
        break

    start_value=end_value
    if i < len(labels):
        end_value=float("%0.1f" % float(labels[i].split('\t')[0]))
        i+=1
    else:
        end_value=start_value+5
    duration = float("%0.1f" % (end_value - start_value))

    sublines.append((text, duration, start_value))


video=CompositeVideoClip([image_clip, concatenate_videoclips(clips)])

# # Save the video
video.write_videofile("/Users/rajaramaniyer/Movies/VS-01-01.mp4",fps=1)
