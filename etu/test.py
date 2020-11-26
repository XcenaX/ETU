# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw 
# from etu.settings import BASE_DIR

# font = ImageFont.truetype( BASE_DIR + '//media//fonts//cmunss.ttf', 16)

# img = Image.open(BASE_DIR + "//media//dogovor.jpg")
# draw = ImageDraw.Draw(img)

# draw.text((100, 100),"Test", (0,0,0), font=font)
# absolute_path = BASE_DIR + "//media//dogovors//" + str(1) + ".jpg"
# img.save(absolute_path)
import requests

r = requests.post("http://127.0.0.1:8000/set_status/", data={
    "id": 1
})

print(r.text)