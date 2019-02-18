#!/usr/bin/env python

import requests
import sys
import json
import os
from PIL import Image
import piexif
import re
import datetime

try:
  sys.argv[3]
except IndexError:
  argverrormsg = 'Error, wrong number of arguments!\n'
  argverrormsg += 'Usage: $ upload-images.py [WP REST endpoint URL] [application password] [photo directory]'
  sys.exit(argverrormsg)
else:
  url = sys.argv[1]
  app_password = sys.argv[2]
  photo_directory = sys.argv[3]

# Get the start time, we'll use this for the output files
starttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Log file subdirectory
log_dir = 'logs/'

# Create a log file directory, if it doesn't exist
if not os.path.isdir(log_dir):
  os.makedirs(log_dir)

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

      tmp_filename = 'tmp-' + filename

      try:
        im = Image.open(photo_directory + '/' + filename)
      except:
        errlogname = 'upload_error_' + starttimestamp + '.log'
        with open(log_dir + errlogname, 'a+') as log_file:
          # Write a line containing the flickr ID, file name, and the HTTP status
          log_file.write(flickrid + '|' + filename + '|Error opening file\n')
        print('Error opening ' + filename )
      else:

        # Rotation code starts here #
        # TODO: This should really be refactored into one or more functions
        # Some images don't have exif data, make sure they do before proceeding
        if 'exif' in im.info:
          exif_dict = piexif.load(im.info['exif']) 

          # Only try to rotate if the orientation parameter exists
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
            try:
              exif_bytes = piexif.dump(exif_dict)
            except:
              print('Error writing exif data to: ' + filename)

            # Rotation code ends here #

        # quality='keep' doens't work here since the format is no longer 'JPEG' after rotating. 
        im.save(photo_directory + '/' + tmp_filename, 'JPEG', exif=exif_bytes, quality=jpeg_quality)
      

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
          errlogname = 'upload_error_' + starttimestamp + '.log'
          with open(log_dir + errlogname, 'a+') as log_file:
            # Write a line containing the flickr ID, file name, and the HTTP status
            log_file.write(flickrid + '|' + filename + '|' + str(res.status_code) + '\n')
          print('Error with ' + filename + ': ' + str(res.status_code))
        else:
          logfilename = 'upload_' + starttimestamp + '.log'
          with open(log_dir + logfilename, 'a+') as log_file:
            # Write a line containing the flickr ID, file name, the uploaded URL, image ID, and the HTTP status
            log_file.write(flickrid + '|' + filename + '|' + str(res.json()['link']) + '|' + str(res.json()['id']) + '|' + str(res.status_code) + '\n')
          print(filename + ' uploaded!')

        # Delete the temp file if it exists
        if os.path.isfile(photo_directory + '/' + tmp_filename):
          os.remove(photo_directory + '/' + tmp_filename)

if 'errlogname' in locals():
  print('Completed with errors, check the error log file: ' + log_dir + errlogname)
else:
  print('Completed, no errors.')

print('Congrats! You\'re done with the upload part. The log file is ' + log_dir + logfilename)
print('Try the update-meta-data.py script next! Copy/paste this:')
print('update-meta-data.py ' + url + ' ' + app_password + ' [json data directory] ' + log_dir + logfilename)
