#!/usr/bin/env python

import requests
import sys
import json
import os
from PIL import Image
import piexif
import re

# TODO: Shouldn't run if we don't have a URL and password

url = sys.argv[1]
app_password = sys.argv[2]
photo_directory = sys.argv[3]

# This is the quality of the jpgs that are saved. A value of "93" 
# seems to keep them around the same size as the originals I was testing with.
# I'm setting it low for testing...
jpeg_quality = 1 #93 = close to original quality

# This takes a flickr download filename and returns the flickr and original filename (with extension)
def extractflickerid(filename):
  # File extension
  extension = filename[filename.rfind('.'):]
  # Flickr ID
  flickrid = filename[:filename.rfind('_o.')]
  flickrid = flickrid[flickrid.rfind('_') + 1:]
  # Original filename
  imgfile = filename[:filename.rfind('_o.')]
  imgfile = imgfile[:imgfile.rfind('_')]

  # In some cases, it seems that the pattern is reversed
  # If there is alpha in the flickrid variable (2248328315_058f0b8c35_o.jpg)
  # Then the flickrID came first, probably because the image didn't have a 
  # filename to begin with
  if re.search(r"\D", flickrid) is not None:
    return [imgfile, flickrid  + extension]
  else:
    return [flickrid, imgfile + extension]


# Loop through the given directory and upload every .jpg found
# TODO: Should probably work on other image file types.
for dirname, direnames, filenames in os.walk(photo_directory):
  for filename in filenames:
    if filename.endswith('.jpg'):

      # Rotation code starts here #
      # TODO: This should really be refactored into one or more functions

      tmp_filename = 'tmp-' + filename

      im = Image.open(photo_directory + '/' + filename)

      exif_dict = piexif.load(im.info["exif"]) 

      if piexif.ImageIFD.Orientation in exif_dict["0th"]:

        orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)

        if orientation == 2:
          im = im.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
          im = im.rotate(180)
        elif orientation == 4:
          im = im.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
          im = im.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
          im = im.rotate(-90, expand=True)
        elif orientation == 7:
          im = im.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
          im = im.rotate(90, expand=True)

        # process im and exif_dict...
        w, h = im.size
        exif_dict["0th"][piexif.ImageIFD.XResolution] = (w, 1)
        exif_dict["0th"][piexif.ImageIFD.YResolution] = (h, 1)
        exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
        exif_bytes = piexif.dump(exif_dict)

        # quality='keep' doens't work here since the format is no longer 'JPEG' after rotating. 
        im.save(photo_directory + '/' + tmp_filename, 'JPEG', exif=exif_bytes, quality=jpeg_quality)

        # Rotation code ends here #
    

      file = open(photo_directory + '/' + tmp_filename, 'rb').read()

      # Strip the flickr ID out of the filename when it goes to wordpress
      flickrid = ''
      origfilename = ''
      flickrid, origfilename = extractflickerid(filename)

      headers = {
        'cache-control': 'no-cache',
        'content-disposition': 'attachment; filename=%s' % origfilename,
        'authorization': 'Basic %s' % app_password,
        'content-type': 'image/jpeg'
      }
      res = requests.post(url, data = file, headers = headers)
      if res.status_code != 201:
        print('Error with ' + filename + ': ' + str(res.status_code))
      else:
        # Write a line containing the flickr ID, file name, the uploaded URL, and the image ID
        with open('upload.log', 'a+') as log_file:
          log_file.write(flickrid + '|' + filename + '|' + str(res.json()['link']) + '|' + str(res.json()['id']) + '\n')
        print(filename + ' uploaded!')

      # Delete the temp file
      os.remove(photo_directory + '/' + tmp_filename)


'''
# Everything below is for updating, which we're not working on right now...

# According to someone on the internet, the meta information needs to happen in a different request
# I was unable to get it to work in one either, so we do it in two...
update_headers = {
  'cache-control': 'no-cache',
  'authorization': 'Basic %s' % app_password,
  'content-type': 'application/json'
}

# TODO: Payload, should, of course be dynamic
payload = {
  'description': 'This is the description. Maybe we\'ll put the tags in here too.', 
  'caption': 'This is the caption.',
  'alt_text': 'This is the alt text. Not sure what we can put here.'
}

update_url = url + '/' + str(res.json()['id'])

# Update the meta data
res2 = requests.post(update_url, json = payload, headers = update_headers)

# TODO: The output should be more informative
print(res2.json())

'''

