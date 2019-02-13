#!/usr/bin/env python

import requests
import sys
import json

# TODO - There're almost more lines of TODO than code at this point, this is far from done.

# TODO: Shouldn't run if we don't have a URL and password

url = sys.argv[1]
app_password = sys.argv[2]

# TODO: File should be dynamic and come from a certain directory or something
filename = 'test.jpg'
file = open(filename, 'rb').read()

headers = {
  'cache-control': 'no-cache',
  'content-disposition': 'attachment; filename=%s' % filename,
  'authorization': 'Basic %s' % app_password,
  'content-type': 'image/jpeg'
}

# Send the image
res = requests.post(url, data = file, headers = headers)

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