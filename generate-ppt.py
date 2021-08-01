from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import sys
import csv
import subprocess
import os
import glob
import time

#Create multiple blue highlighted content slide
def create_slides(lines):
  slidecount=0
  next_space = ""
  for count in lines:
    if " " != count[0]:
      slide = prs.slides.add_slide(bullet_slide)
      slidecount = slidecount + 1
      shapes = slide.shapes
      title_shape = shapes.title
      body_shape = shapes.placeholders[1]
      title_shape.text = titletext
      tf = body_shape.text_frame
      p = tf.paragraphs[0]
      space = ""
      for row in lines:
        line_color = RGBColor(0x00, 0x00, 0x00)
        next_space = ""
        if not ("।" in row[0] or "॥" in row[0]):
          next_space = "    "
        if " " == row[0]:
          next_space = ""
        if row[0].strip().endswith("वाच") or row[0].strip().endswith("ऊचुः") or "इति श्रीमद्भागवते महापुराणे पारमहंस्यां संहितायां" in row[0]:
          line_color = RGBColor(0xFF, 0x7F, 0x50)
          next_space = ""
        if row == count:
          line_color = RGBColor(0x00, 0x00, 0xFF)
        run = p.add_run()
        run.text = space + row[0] + "\n"
        font = run.font
        font.color.rgb = line_color
        space = next_space
  return slidecount
#end create_slides

#
# Main Code Starts
#
if len(sys.argv) != 2:
  adyayam_number = input ("Adhyayam Number: ")
else:
  adyayam_number=sys.argv[1]

titletext='SRIMAD BHAGAVATHAM - SKANDAM 10 ADHYAYA ' + adyayam_number
lyricsdata = csv.reader(open('C:/Users/rajar/srimad_bhaghavatham/sanskrit/canto10/chapter'+adyayam_number+".txt", encoding="UTF-8"))
prs = Presentation('template.pptm')
bullet_slide = prs.slide_layouts[1]
title_slide = prs.slide_layouts[0]
adyayam=""
last_line=""

## First Slide
slide = prs.slides.add_slide(title_slide)
shapes = slide.shapes
title_shape = shapes.title
title_shape.text = titletext
picture = shapes.placeholders[10].insert_picture('C:/Users/rajar/Pictures/Bhagavatham10/' + adyayam_number + '.png')
shapes.placeholders[13].text_frame.text = "श्रीमद्भागवते महापुराणे पारमहंस्यां संहितायां"
shapes.placeholders[14].text_frame.text = "दशमः स्कन्दः"
shapes.placeholders[15].text_frame.text = "श्रीमद्भागवतमहापुराणम्"
body_shape = shapes.placeholders[12]

#
# Debug only: For checking contents of the slide
#for shape in slide.placeholders:
#  print('%d %s' % (shape.placeholder_format.idx, shape.name))

## Main Loop to add content slides
firstrow=False
line=0
count=0
lines=[]
slidecount=1
for row in lyricsdata:
  if len(row) > 0:
    if not firstrow:
      body_shape.text_frame.text = row[0]
      adyayam = row[0]
      firstrow=True
    else:
      if "इति श्रीमद्भागवते महापुराणे पारमहंस्यां संहितायां" in row[0]:
        last_line = row[0]
      else:
        lines.append(row)
        line = line + 1
        if line > 7:
          #Create multiple blue highlighted content slide
          slidecount = slidecount + create_slides(lines)
          line = 0
          lines=[]
if len(lines) > 0:
  slidecount = slidecount + create_slides(lines)

## Last Ending Slide
slide = prs.slides.add_slide(title_slide)
slidecount = slidecount + 1
shapes = slide.shapes
title_shape = shapes.title
title_shape.text = titletext
picture = shapes.placeholders[10].insert_picture('C:/Users/rajar/Pictures/Bhagavatham10/' + adyayam_number + '.png')
shapes.placeholders[13].text_frame.text = "इति श्रीमद्भागवते महापुराणे पारमहंस्यां संहितायां"

found=False
last_line_words=last_line.replace("इति श्रीमद्भागवते महापुराणे पारमहंस्यां संहितायां ","").split(" ")
for word in last_line_words:
  if "ऽध्यायः" in word:
    found=True
  if not found:
    shapes.placeholders[14].text_frame.text = shapes.placeholders[14].text_frame.text + " " + word
  else:
    shapes.placeholders[12].text_frame.text = shapes.placeholders[12].text_frame.text + " " + word

prs.save('generated-ppt.pptm')

print ("Generated. Slide Count = ", slidecount)
next_action=input ("Export JPG (e) / Open (o): ")
if next_action == "e":
  files = glob.glob('Slide????.jpg')
  for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))
  p = subprocess.Popen(["C:/Program Files/Microsoft Office 15/root/office15/POWERPNT.EXE", "/M", "generated-ppt.pptm", "Save_PowerPoint_Slide_as_Images"])
  while not next(glob.iglob("Slide*" + str(slidecount) + ".jpg"), None):
    time.sleep(1)
  p.terminate()
  p.wait()
elif next_action == "o":
  p = subprocess.Popen(["C:/Program Files/Microsoft Office 15/root/office15/POWERPNT.EXE", "generated-ppt.pptm"])
