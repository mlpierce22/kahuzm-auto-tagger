import requests
import sys
from bs4 import BeautifulSoup
import urllib.request
import os
import tempfile
import time

#### Setup #####

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v3.0/analyze"
##### Functions ######
def retrieveURL(index):
  image_path = 'temp' + '/' + str(index) + '.jpg'
  print("the src=" + image_src)
  try:
    urllib.request.urlretrieve(image_src, image_path)
    #computerVision(image_path)
  except ValueError:
    print("couldn't grab this url: %s" % image_src)
    return

def computerVision(image_path):
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()
    with open("temp/visionInfo.json", 'a+') as f:
      print(analysis, file=f)

##### End Functions ######

if len(sys.argv) != 2:
  print("please enter 2 arguments")
  sys.exit(1)
else:
  with tempfile.TemporaryDirectory() as directory:
    print("the directory is: %s" % directory)
    #sys.argv[1]
    requestUrl = "https://www.shophomework.com/outdoor" #"https://www.allthingstall.co/"
    webpage = requests.get(requestUrl)
    parsedPage = BeautifulSoup(webpage.content, 'html.parser')
    images = parsedPage.findAll('img')
    for index, image in enumerate(images):
      print("analyzing image %d" % index)
      # print(image.attrs)
      image_src=""
      # if hasattr(image, 'srcset'):
      #   allImages = image['srcset']
      try:
        image_src = image['src']
        if image_src.startswith('//'):
          image_src = image_src[2:]
        retrieveURL(index)
        continue
      except KeyError:
          print("src didn't work, trying something else.")
      try:
        image_src = image['data-src']
        retrieveURL(index)
        continue
      except KeyError:
          print("data-src didn't work, trying something else.")
      try:
        image_src = image['data-image']
        retrieveURL(index)
        continue
      except KeyError:
          print("data-image didn't work, giving up")
          continue
      #time.sleep(1)
    image_path = 'temp' + '/' + str(10) + '.jpg'
    computerVision(image_path)