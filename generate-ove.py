import sys
import os
import glob
import wave, struct

#
# Main Code Starts
#
if len(sys.argv) != 2:
  adyayam_number = input ("Adhyayam Number: ")
else:
  adyayam_number=sys.argv[1]

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
filename="adhyayam" + str(adyayam_number) + ".ove"
f = open(filename, "w")

f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<project>\n')
f.write('    <version>190219</version>\n')
f.write('    <url>{dir_path}/{filename}</url>\n'.format(filename=filename, dir_path=dir_path))
f.write('    <folders/>\n')
f.write('    <media>\n')

files=glob.glob("Slide????.jpg")

id=0
for slidename in files:
    id=id+1
    f.write('        <footage id="{id}" folder="0" name="{slidename}" url="{slidename}" duration="40000" using_inout="0" in="0" out="0" speed="1" alphapremul="0" startnumber="0" proxy="0" proxypath="">\n'.format(id=id, slidename=slidename))
    f.write('            <video id="0" width="1280" height="720" framerate="0.0000000000" infinite="1"/>\n')
    f.write('        </footage>\n')

wavfilename="../../Documents/Thirupavai/Exported/Bhagavatham/10-" + str(adyayam_number) + ".wav"

wavefile = wave.open(wavfilename, 'rb')
channels = wavefile.getnchannels()
frames = wavefile.getnframes()
rate = wavefile.getframerate()
duration = frames / float(rate)
sampwidth = wavefile.getsampwidth()
data = wavefile.readframes(frames) #read the all the samples from the file into a byte string
audioframes=round(duration*29.97)
wavefile.close()

id=id+1
f.write('        <footage id="{id}" folder="0" name="10-{adyayam_number}.wav" url="{wavfilename}" duration="{duration}" using_inout="0" in="0" out="0" speed="1" alphapremul="0" startnumber="0" proxy="0" proxypath="">\n'.format(id=id,adyayam_number=adyayam_number,wavfilename=wavfilename,duration=(round(duration * 1000000))))
f.write('            <audio id="0" channels="{channels}" layout="0" frequency="{rate}"/>\n'.format(channels=channels,rate=rate))
f.write('        </footage>\n')
f.write('    </media>\n')
f.write('    <sequences>\n')
f.write('        <sequence id="1" folder="0" name="Sequence 01" width="1280" height="720" framerate="29.9700000000" afreq="48000" alayout="3" open="1" workarea="0" workareaIn="0" workareaOut="0">\n')
id=0
imageduration=round(duration*29.97/len(files))
invalue=0
outvalue=0
for slidename in files:
    id=id+1
    invalue=outvalue
    outvalue=outvalue+imageduration
    if outvalue > audioframes:
        outvalue=audioframes
    f.write('            <clip id="{id}" enabled="1" name="{slidename}" clipin="0" in="{invalue}" out="{outvalue}" track="-1" r="192" g="160" b="128" autoscale="0" speed="1.0000000000" maintainpitch="0" reverse="0" type="0" media="{id}" stream="0">\n'.format(slidename=slidename,id=id,invalue=invalue,outvalue=outvalue))
    f.write('                <linked/>\n')
    f.write('                <effect name="Distort/Transform" enabled="1">\n')
    f.write('                    <row>\n')
    f.write('                        <field id="posx" value="640"/>\n')
    f.write('                        <field id="posy" value="360"/>\n')
    f.write('                    </row>\n')
    f.write('                    <row>\n')
    f.write('                        <field id="scalex" value="100"/>\n')
    f.write('                        <field id="scaley" value="100"/>\n')
    f.write('                    </row>\n')
    f.write('                    <row>\n')
    f.write('                        <field id="uniformscale" value="1"/>\n')
    f.write('                    </row>\n')
    f.write('                    <row>\n')
    f.write('                        <field id="rotation" value="0"/>\n')
    f.write('                    </row>\n')
    f.write('                    <row>\n')
    f.write('                        <field id="anchorx" value="0"/>\n')
    f.write('                        <field id="anchory" value="0"/>\n')
    f.write('                    </row>\n')
    f.write('                    <row>\n')
    f.write('                        <field id="opacity" value="100"/>\n')
    f.write('                    </row>\n')
    f.write('                    <row>\n')
    f.write('                        <field id="blendmode" value=""/>\n')
    f.write('                    </row>\n')
    f.write('                </effect>\n')
    f.write('            </clip>\n')

id=id+1
f.write('            <clip id="{id}" enabled="1" name="10-{adyayam_number}.wav" clipin="0" in="0" out="{duration}" track="0" r="128" g="192" b="128" autoscale="0" speed="1.0000000000" maintainpitch="0" reverse="0" type="0" media="{id}" stream="0">\n'.format(adyayam_number=adyayam_number,duration=audioframes,id=id))
f.write('                <linked/>\n')
f.write('                <effect name="/Volume" enabled="1">\n')
f.write('                    <row>\n')
f.write('                        <field id="volume" value="1"/>\n')
f.write('                    </row>\n')
f.write('                </effect>\n')
f.write('                <effect name="/Pan" enabled="1">\n')
f.write('                    <row>\n')
f.write('                        <field id="pan" value="0"/>\n')
f.write('                    </row>\n')
f.write('                </effect>\n')
f.write('            </clip>\n')
f.write('        </sequence>\n')
f.write('    </sequences>\n')
f.write('</project>\n')
f.close()