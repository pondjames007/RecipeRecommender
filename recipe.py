from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import requests
import os
import time
import random

def download_file(url, local_filename=None):

    if local_filename is None:
        local_filename = url.split('/')[-1]

    # if os.path.exists(local_filename):
    #     return local_filename

    # NOTE the stram=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    return local_filename


parser = argparse.ArgumentParser(description="Look for a recipe image")

parser.add_argument("-i", "--input", dest="input", help="Input images", default='')

args = parser.parse_args()

inputImgName = args.input.split(',')[0:-1]


app = ClarifaiApp(api_key='9295b11b259b45dbbfc7df8159745e74')


model = app.models.get('general-v1.3')

# images = []
keywords = []
for imgName in inputImgName:
    print(imgName)
    image = ClImage(file_obj=open('public/images/'+imgName, 'rb'))
    data = model.predict([image])
    keywords += [name['name'] for name in data['outputs'][0]['data']['concepts']][:3]
    
print(keywords)
keyword_string = " ".join(keywords)
with open('public/keywords.txt', 'w') as txt_file:
    txt_file.write(keyword_string)

keyword_string += ' food recipe'
print(keyword_string)
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.Chrome()
driver.get('https://images.google.com/')
searcher = driver.find_element_by_name('q')
searcher.send_keys(keyword_string)
searcher.send_keys(Keys.RETURN)
time.sleep(3)


# imageURL = driver.find_element_by_css_selector('.rg_bx.rg_di.rg_el.ivg-i a').get_attribute('href')
# imageURL = driver.find_element_by_css_selector('.rg_bx.rg_di.rg_el.ivg-i a')

# imageURL.get_attribute('href')

# print()
# print(driver.execute_script("document.querySelector('.rg_bx.rg_di.rg_el.ivg-i a')"))
# print(imageURL)
image = driver.find_elements_by_css_selector('img.rg_ic.rg_i')
print(len(image))
image = random.choice(image)
# driver.get(imageURL)
url = image.get_attribute('data-src')

savedname = 'public/images/output.jpg'
download_file(url, savedname)
# image.click()
# time.sleep(5)

driver.quit()
