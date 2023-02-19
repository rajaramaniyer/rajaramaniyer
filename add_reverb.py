from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
from pydub import AudioSegment
import sys
from os import path
from math import ceil

#
# Main Code Starts
#
canto="1"
if len(sys.argv) < 2:
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

ASTRING=canto.zfill(2) + '-' + adyayam_number.zfill(2)

IMPORTED_FOLDER="C:/Users/rajar/Documents/Thirupavai/Imported/Bhagavatham/01 Pratama skandam/"
EXPORTED_FOLDER="C:/Users/rajar/Documents/Thirupavai/Exported/Bhagavatham/"
TEMP_FOLDER="C:/Users/rajar/AppData/Local/Temp/"

voice = AudioSegment.from_wav(IMPORTED_FOLDER + ASTRING + ".wav")
tambura = AudioSegment.from_ogg("C:/Users/rajar/lmms/samples/tambura/f.ogg") - 25 # less -25db
tambura = tambura.set_channels(1)

tl = len(tambura)
vl = len(voice)
rc = int(ceil(vl/tl))
print("vl = %d" % vl)
print("tl = %d" % tl)
print("tl repeat count = %d" % rc)

fulltambura = tambura.fade_in(2000) + (tambura * (rc-2)) + tambura.fade_out(2000)

print("fulltambura len = %d" % len(fulltambura))

# vl = 381207
# tl = 4502
# tl repeat count = 85
# fulltambura len = 382651

# mix sound2 with sound1, starting at 5000ms into sound1)
output = fulltambura.overlay(voice, position=0)

# save the result
output.export(TEMP_FOLDER + ASTRING + ".wav", format="wav")

# Load a VST3 or Audio Unit plugin from a known path on disk:
vst = load_plugin("C:/Program Files/Common Files/VST3/Steinberg/Basic FX Suite/REV-X_HALL.vst3")

# print(vst.parameters.keys())
# dict_keys([
#     'reverb_time', 'initial_delay', 'decay', 
#     'room_size', 'diffusion', 'hpf', 'lpf', 
#     'high_ratio', 'low_ratio', 'low_freq', 
#     'mix', 'bypass', 'vu'
# ])

# Set the "mix" parameter to 25, default is 100.0
vst.mix = 25.0

# Use this VST to process some audio:
with AudioFile(TEMP_FOLDER + ASTRING + '.wav', 'r') as f:
  audio = f.read(f.frames)
  samplerate = f.samplerate
  effected = vst(audio, samplerate)
  with AudioFile(EXPORTED_FOLDER + ASTRING + '.wav', 'w', f.samplerate, f.num_channels) as o:
    o.write(effected)
