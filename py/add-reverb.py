from pedalboard import Pedalboard, load_plugin
from pedalboard.io import AudioFile
from pydub import AudioSegment
import sys
from os import path
from math import ceil

#
# Main Code Starts
#
if len(sys.argv) < 3:
  wav_file_name = input ("WAV File Name?: ")
  pitch = input ("Pitch(f)?: ")
  if pitch == "":
    pitch="f"
else:
  wav_file_name = sys.argv[1]
  pitch = sys.argv[2]

TEMP_FOLDER="C:/Users/rajar/AppData/Local/Temp/add_reverb.wav"

autotune_vst = load_plugin("C:/Program Files/Common Files/VST3/Auburn Sounds Graillon 2-64.vst3")

# print(autotune_vst.parameters.keys())
# dict_keys([
#   'bypass', 'preset', 'lead_gain_db', 
#   '2nd_sub_octave_amount_db', '2nd_sub_fifth_amount_db', 
#   '1st_sub_octave_amount_db', '1st_sub_fifth_amount_db', 
#   'dry_wet', 'dry_mix_db', 
#   'low_cut_frequency_hz', 'output_level_db', 
#   'placebo', 'bitdepth', 'quantize', 
#   'ring_mode', 'mod_octave_oct', 'mono_reduction', 
#   'pitch_shift_st', 'preserve_formants', 'correction', 
#   'pitch_smoothing_ms', 'snap_range_st', 'reference_hertz', 
#   'inertia', 'allow_c', 'allow_c_sharp', 'allow_d', 
#   'allow_d_sharp', 'allow_e', 'allow_f', 'allow_f_sharp', 
#   'allow_g', 'allow_g_sharp', 'allow_a', 'allow_a_sharp', 
#   'allow_b', 'inv_2nd_sub_octave', 
#   'inv_2nd_sub_quint', 'inv_1st_sub_octave_sharp', 
#   'inv_1st_sub_quint'
# ])

autotune_vst.correction = 20.0
autotune_vst.pitch_smoothing_ms = 1.5

# Load a VST3 or Audio Unit plugin from a known path on disk:
reverb_vst = load_plugin("C:/Program Files/Common Files/VST3/Steinberg/Basic FX Suite/REV-X_HALL.vst3")

# print(vst.parameters.keys())
# dict_keys([
#     'reverb_time', 'initial_delay', 'decay', 
#     'room_size', 'diffusion', 'hpf', 'lpf', 
#     'high_ratio', 'low_ratio', 'low_freq', 
#     'mix', 'bypass', 'vu'
# ])

# Set the "mix" parameter to 25, default is 100.0
reverb_vst.mix = 25.0

# Use this VST to process some audio:
with AudioFile(wav_file_name, 'r') as f:
  audio = f.read(f.frames)
  samplerate = f.samplerate
  num_channels = f.num_channels

board = Pedalboard([autotune_vst, reverb_vst])
#board = Pedalboard([reverb_vst])
effected = board(audio, samplerate)
with AudioFile(TEMP_FOLDER, 'w', samplerate, num_channels) as o:
  o.write(effected)

voice = AudioSegment.from_wav(TEMP_FOLDER)
tambura = AudioSegment.from_ogg("C:/Users/rajar/lmms/samples/tambura/%s.ogg" % pitch) - 25 # less -25db
tambura = tambura.set_channels(1)

tl = len(tambura)
vl = len(voice)
rc = int(ceil(vl/tl))
# print("vl = %d" % vl)
# print("tl = %d" % tl)
# print("tl repeat count = %d" % rc)

fulltambura = tambura.fade_in(2000) + (tambura * (rc-2)) + tambura.fade_out(2000)

# print("fulltambura len = %d" % len(fulltambura))

# mix voice with tambura
output = fulltambura.overlay(voice, position=0)

# save the result
output.export(wav_file_name.replace("Imported", "Exported"), format="wav")
