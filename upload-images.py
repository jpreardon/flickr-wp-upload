#!/usr/bin/env python

import requests
import sys
import json
import os

# TODO - There're almost more lines of TODO than code at this point, this is far from done.

# TODO: Shouldn't run if we don't have a URL and password

url = sys.argv[1]
app_password = sys.argv[2]
photo_directory = sys.argv[3]

# Loop through the given directory and upload every .jpg found
for dirname, direnames, filenames in os.walk(photo_directory):
  for filename in filenames:
    if filename.endswith('.jpg'):
      file = open(photo_directory + '/' + filename, 'rb').read()
      headers = {
        'cache-control': 'no-cache',
        'content-disposition': 'attachment; filename=%s' % filename,
        'authorization': 'Basic %s' % app_password,
        'content-type': 'image/jpeg'
      }
      res = requests.post(url, data = file, headers = headers)
      if res.status_code != 201:
        print('Error with ' + filename + ': ' + str(res.status_code))
      else:
        # Write a line containing the file name, the uploaded URL, and maybe the image ID
        with open('upload.log', 'a+') as log_file:
          log_file.write(filename + '|' + str(res.json()['link']) + '|' + str(res.json()['id']) + '\n')
        print(filename + ' uploaded!')


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