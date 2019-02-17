#!/usr/bin/env python

import requests
import sys
import json
import os
import pprint
import re

pp = pprint.PrettyPrinter(indent=4)

filename = 'flickr-test-data/data/photo_9079456535.json'
#filename = 'flickr-test-data/data/photo_9079476429.json'

file = open(filename, 'r')
photo_info = json.load(file)

if photo_info['name']:
  print(photo_info['name'])
# Create Description
description = ''

if photo_info['description']:
  description = photo_info['description'] + '\n'

if photo_info['tags']:
  description += 'Tags:'
  for tag in photo_info['tags']:
    description += ' #' + tag['tag']
  description += '\n'

if photo_info['date_taken']:
  description += 'Date taken: ' + photo_info['date_taken']

print(description)
print(photo_info['privacy'])

# Let's strip the flickr ID out of the filename when it goes to wordpress
# graf_5214959221_o.jpg It will be the part from the right between the "." and the last "_", inclusive 

# This doesn't really work because some filenames include underscores
# orig = 'graf_5214959221_o.jpg'
# # Number of undersscores
# print(orig.count('_'))
# orig = orig.split('_')
# # Flickr ID
# print(orig[1])
# # File name + Extension
# print(orig[0] + orig[2][orig[2].rfind('.'):])

# Crap, there are some weird ones that have no filename so the the pattern is reversed :(
# They have alpha where only numeric should be, like this:
# 2248328315_058f0b8c35_o.jpg

# def extractflickerid(filename):

#   # This is the file extension
#   extension = filename[filename.rfind('.'):]
#   # This is the flickr ID
#   flickrid = filename[:filename.rfind('_o.')]
#   flickrid = flickrid[flickrid.rfind('_') + 1:]
#   # This is the filename
#   imgfile = filename[:filename.rfind('_o.')]
#   imgfile = imgfile[:imgfile.rfind('_')]

#   if re.search(r"\D", flickrid) is not None:
#     return [imgfile, flickrid  + extension]
#   else:
#     return [flickrid, imgfile + extension]

# #flickrid, origname = extractflickerid('_dsc7328_147_jpg_1908369723_o.jpg')
# flickrid, origname = extractflickerid('2248328315_058f0b8c35_o.jpg')

# print(flickrid)
# print(origname)

#orig = 'graf_5214959221_o.jpg'
# orig = '_dsc7328_147_jpg_1908369723_o.jpg'
# print(orig)
# # This is the file extension
# extension = orig[orig.rfind('.'):]
# # This is the flickr ID
# flickrid = orig[:orig.rfind('_o.')]
# flickrid = flickrid[flickrid.rfind('_') + 1:]
# # This is the filename
# filename = orig[:orig.rfind('_o.')]
# filename = filename[:filename.rfind('_')]

# print(flickrid)
# print(filename + extension)
# Number of undersscores
# print(orig.count('_'))
# orig = orig.split('_')
# # Flickr ID
# print(orig[1])
# # File name + Extension
# print(orig[0] + orig[2][orig[2].rfind('.'):])

# photo_directory = '/Users/jpreardon/Photos/flickr/photos'

# for dirname, direnames, filenames in os.walk(photo_directory):
#   for filename in filenames:
#     if filename.count('_') != 2:
#       print(filename)
