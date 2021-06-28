from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import sys
import csv

def create_slides(lines):
  space = ""
  next_space = ""
  for count in lines:
    if " " != count[0]:
      slide = prs.slides.add_slide(bullet_slide)
      shapes = slide.shapes
      title_shape = shapes.title
      body_shape = shapes.placeholders[1]
      title_shape.text = titletext
      tf = body_shape.text_frame
      p = tf.paragraphs[0]
      for row in lines:
        line_color = RGBColor(0x00, 0x00, 0x00)
        next_space = ""
        if not ("।" in row[0] or "॥" in row[0]):
          next_space = "    "
        if " " == row[0]:
          next_space = ""
        if "उवाच" in row[0] or "इति श्रीमद्भागवते महापुराणे पारमहंस्यां संहितायां" in row[0]:
          line_color = RGBColor(0xFF, 0x7F, 0x50)
          next_space = ""
        if row == count:
          line_color = RGBColor(0x00, 0x00, 0xFF)
        run = p.add_run()
        run.text = space + row[0] + "\n"
        font = run.font
        font.color.rgb = line_color
        space = next_space
#end create_slides

#
# Main Code Starts
#
if len(sys.argv) != 2:
  print ("Pass Adhyayam Number")
  sys.exit(1)

titletext='SRIMAD BHAGAVATHAM - SKANDAM 10 ADHYAYA ' + sys.argv[1]
lyricsdata = csv.reader(open('lyrics.csv', encoding="UTF-8"))
prs = Presentation('template.pptx')
bullet_slide = prs.slide_layouts[1]
title_slide = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide)
shapes = slide.shapes
title_shape = shapes.title
title_shape.text = titletext
body_shape = shapes.placeholders[12]
#
# For checking contents of the slide
#for shape in slide.placeholders:
#  print('%d %s' % (shape.placeholder_format.idx, shape.name))

firstrow=False
line=0
count=0
lines=[]
for row in lyricsdata:
  if len(row) > 0:
    if not firstrow:
      body_shape.text_frame.text = row[0]
      firstrow=True
    else:
      lines.append(row)
      line = line + 1
      if line > 7:
        create_slides(lines)
        line = 0
        lines=[]
if len(lines) > 0:
  create_slides(lines)

prs.save('generated-ppt.pptx')

#blank_slide_layout = prs.slide_layouts[6]
#slide = prs.slides.add_slide(blank_slide_layout)
#
#left = top = Inches(1)
#width = Inches(11)
#height = Inches(0.5)
#
#for row in lyricsdata:
#  if len(row) > 0:
#    txBox = slide.shapes.add_textbox(left, top, width, height)
#    txBox.text_frame.text = row[0]
#    top = top + Inches(0.5)
#    if top > Inches(6):
#      top = Inches(1)
#      slide = prs.slides.add_slide(blank_slide_layout)
