import glob
import sys
import os

canto="1"
if len(sys.argv) < 2:
  dashakam_number = input ("Dashakam Number?: ")
  if dashakam_number == "":
    sys.exit(0)
else:
  dashakam_number = sys.argv[1]

ASTRING='Narayaneeyam-' + dashakam_number.zfill(3)
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

files = glob.glob(ASTRING + '.dat')
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

files = glob.glob(ASTRING + '.txt')
for f in files:
    try:
        os.rename(f, 'done/' + f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))
