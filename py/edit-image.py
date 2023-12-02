from PIL import Image, ImageFont, ImageDraw

file_name=input('Full file name?: ')
image = Image.open(file_name)

width, height = image.size
new_width=round(height/1.15)
new_height=round(width*1.15)

if width > height:
    background = Image.new ('RGBA', (width, new_height), color=(255,255,255,0))
    background.paste(image, ((0,round((new_height-height)/2))))
else:
    background = Image.new ('RGBA', (new_width, height), color=(255,255,255,0))
    background.paste(image, (round((new_width-width)/2),0))

# title_font = ImageFont.truetype('arial.ttf', 20)

# title_text = "वेपथुश्चापि हृदये आराद्दास्यन्ति विप्रियम्"

# image_editable = ImageDraw.Draw(background)

# image_editable.rounded_rectangle([(round((new_width-width)/2), round(height*0.9)), (new_width-round((new_width-width)/2), height-5)], radius=5, fill=(0,0,0))

# image_editable.text((round((new_width-width)/2), round(height*0.9)+10), title_text, (237, 230, 211), font=title_font)

background.save(file_name)
