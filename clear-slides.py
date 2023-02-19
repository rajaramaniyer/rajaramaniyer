import glob
import sys
import os

canto="1"
if len(sys.argv) < 2:
  adyayam_number = input ("Canto " + canto.zfill(2) + " Adhyayam Number?: ")
  if adyayam_number == "":
    sys.exit(0)
else:
  adyayam_number = sys.argv[1]

ASTRING='SB-' + canto.zfill(2) + '-' + adyayam_number.zfill(2)
files = glob.glob(ASTRING + '-Slide????.jpg')
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

files = glob.glob(ASTRING + '.mp4')
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

files = glob.glob(ASTRING + '.pptm')
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

files = glob.glob(ASTRING + '.txt*')
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

files = glob.glob(ASTRING + '.mlt')
for f in files:
    try:
        os.rename(f, 'done/' + f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))
