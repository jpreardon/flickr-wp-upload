#!/usr/bin/env python

import requests
import sys
import json
import os
import pprint
import re

url = sys.argv[1]
app_password = sys.argv[2]
json_dir = sys.argv[3]
logfile = sys.argv[4]

pp = pprint.PrettyPrinter(indent=4)


'''
What needs to happen here?

1) Open log file
2) Find associated json file based on ID
3) Open json file
4) Bulid description from description, tags, date taken
5) Update wordpress based on ID in log file
'''

# Open log file
log = open(logfile, 'r')
for line in log:
  fileid = line.split('|')[0]
  wpid = line.split('|')[3].rstrip()

  # Find associated json file based on ID

  # Load the files in the directory
  jsonfiles = os.listdir(json_dir)

  # find the file we care about
  # This seems inefficient, but whatever
  for file in jsonfiles:
    if file.find(fileid) > 0:
      jsonfile = file

      filename = json_dir + '/' + jsonfile

      # Open json file
      file = open(filename, 'r')
      photo_info = json.load(file)

      # Bulid description from description, tags, date taken
      description = ''
      if photo_info['description']:
        description = photo_info['description'] + '\n'

      if photo_info['tags']:
        description += 'Tags:'
        for tag in photo_info['tags']:
          description += ' #' + tag['tag']
        description += '\n'

      if photo_info['date_taken']:
        description += 'Date taken: ' + photo_info['date_taken'] + '\n'

      description += 'Imported from flickr'


      # Update wordpress based on ID in log file

      update_headers = {
        'cache-control': 'no-cache',
        'authorization': 'Basic %s' % app_password,
        'content-type': 'application/json'
      }

      # Build the payload
      payload = {}

      if photo_info['name']:
        payload['title'] = photo_info['name']

      if description:
        payload['description'] = description

      if photo_info['privacy'] == 'private':
        payload['status'] = 'private'

      update_url = url + '/' + wpid

      res = requests.post(update_url, json = payload, headers = update_headers)


      print(fileid + ': ' + str(res.status_code))

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
