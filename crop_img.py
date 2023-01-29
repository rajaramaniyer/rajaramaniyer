#!/opt/homebrew/opt/python@3.9/libexec/bin/python

# shell script to run this python script
# ls -1a RangaShathakam/*.jpg | while read file
# do
#     file=$(echo $file | cut -f1 -d'.')
#     ./crop_img.py $file
# done

# Importing Image class from PIL module
from PIL import Image
import sys
import glob

image_file_name=input("ImgFileName: ")

files = sorted(glob.glob(image_file_name))
i=1
for f in files:
  # Opens a image in RGB mode
  im = Image.open(f)

  width, height = im.size
  top = 0
  bottom = height

  # Setting the points for cropped image
  left = 0
  right = (width / 2) + 100
  im.crop((left, top, right, bottom)).save('Image-' + str(i).zfill(2) + ".jpg")

  i+=1
  left = right
  right = width
  im.crop((left, top, right, bottom)).save('Image-' + str(i).zfill(2) + ".jpg")
  i+=1