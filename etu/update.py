import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','etu.settings')
django.setup()

from api.models import *
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup as BS
import time
from django.utils import timezone

from django.core.files import File
from tempfile import NamedTemporaryFile
from time import sleep

from selenium import webdriver
from urllib.request import urlopen
import re
options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

domain = "https://www.technodom.kz"
types = ["/atyrau/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki?page=", "/atyrau/smartfony-i-gadzhety/smartfony-i-telefony/smartfony?page="]

def get_urls(html, urls):
    items = ItemToBuy.objects.all()
    
    for item in html.findAll("a", {"class": "ProductCard-Content"}): #html.select(".thumb_main"):        
        url_name = item.get("href").split('/')[6]
        print(url_name)
        if len(items.filter(url_name=url_name)) == 0:
            urls.append(item.get("href"))
        
    return urls
        

def get_all_urls(count):
    urls = []    
    for category in types:
        for i in range(1,count+1):
            driver.get(domain + category + str(i))
            sleep(2)   
            html = driver.page_source
            #r = requests.get(domain+"atyrau/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki?page=" + str(i))
            
            html = BS(html, 'html.parser')
            f = open("test.html", "w+", encoding="utf-8")
            f.write(str(html))
            f.close()
            urls = get_urls(html, urls)        
        
    return urls

def parse_one_item(url):
    driver.get(domain + url) 
    sleep(6)   
    html = driver.page_source
    html = BS(html, 'html.parser')
    url_name = url.split('/')[6]
    print(url_name)

    name = html.select_one(".ProductHeader-Title").text  
    print(name)

    #name = html.findAll("h1", {"class": "ProductHeader-Title"})[0].text    
    price = html.select_one(".ProductInformation-Price").text    
    splited = price.split(u'\xa0')
    price = splited[0] + splited[1]
    splited = re.split('\W+', price)
    price = int(splited[0])

    #price = int(price.replace(u'\xa0', u' ').replace(" ", "")[:-1])
    print(price)

    image_href = list(html.select_one("picture.Image.Image_ratio_custom.Image_isLoaded.Image_isReal.ProductGallery-Image").children)[0].get("src")    
    print(image_href)

    item_type_name = list(html.select("li.Breadcrumbs-Crumb"))[2].text
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(image_href).read())
    img_temp.flush()

    if len(Type.objects.filter(name=item_type_name)) == 0:
        Type.objects.create(name=item_type_name)

    item_type = Type.objects.filter(name=item_type_name).first()

    if len(Provider.objects.filter(name="Технодом")) == 0:
        Provider.objects.create(name="Технодом")

    provider = Provider.objects.filter(name="Технодом").first()
    item = ItemToBuy.objects.create(name=name, item_type=item_type, provider=provider, price=price, url_name=url_name)
    item.image.save("image_%s.png" % item.id, File(img_temp))
    item.save()

    
    
    
   



# try:
#     print("Получаем урлы...")
#     urls = get_all_urls(5)
#     print(len(urls))
#     for url in urls:
#         parse_one_item(url)
#         break
# except:
#     pass 

print("Получаем урлы...")
urls = get_all_urls(5)
print(len(urls))
for url in urls:
    parse_one_item(url)
    
driver.close()

#urls = get_all_urls()


# print("Парсим порнушку...")
# for url in urls:
#     parse_one_porn(url)
#     print("_____")

# print("Поздравляю!! Вы спиздили порнуху с другого сайта, вы Майк Гавновский!!")
# time.sleep(3)
