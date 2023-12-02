import sys
import os
import shutil
from os import path
import glob

#
# Main Code Starts
#
canto="3"
canto_title="तृतीय स्कन्धः"
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

from_slide = int(input("Slides to duplicate from?: "))-1
to_slide = int(input("Slides to duplicate to?: "))-1

ASTRING='SB-' + canto.zfill(2) + '-' + adyayam_number.zfill(2)

files = glob.glob(ASTRING + '-Slide????.png')
for i in range(len(files)-1, to_slide, -1):
  os.rename(files[i], (ASTRING + '-Slide%04d.png' % (i+1+to_slide-from_slide+1)))

for i in range(from_slide, to_slide+1):
  shutil.copyfile(files[i], (ASTRING + '-Slide%04d.png' % (i+1+to_slide-from_slide+1)))
