from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from etu.settings import BASE_DIR

font = ImageFont.truetype( BASE_DIR + '//media//fonts//cmunss.ttf', 35)

img = Image.open(BASE_DIR + "//media//dogovor.jpg").convert("RGB")

draw = ImageDraw.Draw(img)
draw.text((135, 415),"Test", (0,0,0), font=font)
absolute_path = BASE_DIR + "//media//dogovors//" + str(1) + ".jpg"
img.save(absolute_path)
