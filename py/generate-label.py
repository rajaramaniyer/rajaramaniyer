from pydub import AudioSegment, silence
import sys
from os import path
from statistics import mean

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
label_file_name = ASTRING + '.txt'
voice_data = ASTRING + '.dat'

lyrics_file='C:/Users/rajar/books/narayaneeyam/narayaneeyam-'+dashakam_number.zfill(3)+".txt"
if not path.exists(lyrics_file):
  input("Lyrics file does not exists. " + lyrics_file)
  sys.exit()

file = open(lyrics_file, 'r', encoding="UTF-8")
filelines = file.readlines()
file.close()
filelines.append('\n')

blocks=[]
block=[]
purefilelines=[]
linecount=0
firstline=True
secondline=True
for line in filelines:
  if firstline:
    firstline=False
    continue
  if not firstline and secondline:
    secondline=False
    continue
  if len(line.strip()) == 0:
    if len(block) > 0:
      textblock={}
      textblock['linecount']=len(block)
      textblock['lines']=block
      textblock['linelen']=len(block[0])
      blocks.append(textblock)
    block=[]
  else:
    block.append(line.strip())
    linecount+=1
    purefilelines.append(line.strip())

print('Total labels expected = %d' % linecount)

if path.exists(label_file_name):
  ss = []
  l=0
  with open(label_file_name, 'r', encoding="UTF-8") as f:
    lines = f.readlines()
    for line in lines:
      s = line.strip().split("\t")
      if l < len(purefilelines):
        textline=purefilelines[l]
      else:
        textline=""
      ss.append("%s\t%s\t%s\n" % (s[0], s[1], textline))
      l+=1
  with open(label_file_name, 'w', encoding="UTF-8") as f:
    f.writelines(ss)
  print("Label file exists. Just corrected text in it: " + label_file_name)
  sys.exit()

IMPORTED_FOLDER="C:/Users/rajar/Documents/Thirupavai/Imported/Narayaneeyam- Sruti F(M)/"
voice_file_name = IMPORTED_FOLDER + ASTRING + ".wav"
voice = AudioSegment.from_wav(voice_file_name)
if path.exists(voice_data) and path.getmtime(voice_file_name) < path.getmtime(voice_data):
  with open(voice_data, 'r') as f:
    ss=[]
    ssLines = f.readlines()
    for line in ssLines:
      s = line.strip().split("\t")
      ss.append([int(s[0]),int(s[1])])
else:
  ss = silence.detect_silence(voice, min_silence_len=350, silence_thresh=-24)
  with open(voice_data, 'w') as f:
    for s in ss:
      f.write(str(s[0])+"\t"+str(s[1])+"\n")

file = open(label_file_name, 'w', encoding="UTF-8")
prev=0
labelcount=0
prev_b=0
b=0
l=0
prev_line=''

long_threshold_4=7800
short_threshold_4=2500
threshold_3=3800

for s in ss:
    go_ahead=False

    if prev == 0:
      prev=s[1]
    else:
      # print("b = %d; l = %d; labelcount = %d; blocks[b]['linecount'] = %d" % (b,l,labelcount,blocks[b]['linecount']))
      line=blocks[b]['lines'][l]
      if prev_line == '':
        go_ahead=True
      else:
        if blocks[prev_b]['linecount'] <= 3 and s[1] - prev > threshold_3:
          go_ahead=True
        elif blocks[prev_b]['linecount'] == 4 and s[1] - prev > (short_threshold_4 if blocks[prev_b]['linelen'] <= 32 else long_threshold_4):
          go_ahead=True

    if go_ahead:
      prev_line=line
      file.write("%.3f\t%.3f\t%s\n" % (s[0]/1000, s[0]/1000, prev_line))
      labelcount+=1
      l+=1
      if l >= blocks[b]['linecount']:
        prev_b=b
        b+=1
        l=0
      prev=s[1]
      if b >= len(blocks):
        break
file.close()

print('Total labels generated = %d' % labelcount)
