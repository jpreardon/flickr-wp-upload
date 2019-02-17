#!/usr/bin/env python

import requests
import sys
import json
import os
import datetime


try:
  sys.argv[4]
except IndexError:
  argverrormsg = 'Error, wrong number of arguments!\n'
  argverrormsg += 'Usage: $ update-meta-data.py [WP REST endpoint URL] [application password] [data directory] [upload log file]'
  sys.exit(argverrormsg)
else:
  url = sys.argv[1]
  app_password = sys.argv[2]
  json_dir = sys.argv[3]
  logfile = sys.argv[4]

# Get the start time, we'll use this for the output files
starttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Open log file
log = open(logfile, 'r')
for line in log:
  fileid = line.split('|')[0]
  filelink = line.split('|')[2]
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
        payload['caption'] = photo_info['name']

      if description:
        payload['description'] = description

      if photo_info['privacy'] == 'private':
        payload['status'] = 'private'

      update_url = url + '/' + wpid

      res = requests.post(update_url, json = payload, headers = update_headers)
      if res.status_code != 200:
        errlogname = 'update_error_' + starttimestamp + '.log'
        with open(errlogname, 'a+') as log_file:
          # Write a line containing the flickr ID, file link, wordpress id, and the HTTP status
          log_file.write(fileid + '|' + filelink + '|' + wpid + '|' + str(res.status_code) + '\n')
          print('Error with ' + filelink + ': ' + str(res.status_code))
      else:
        logfilename = 'update' + starttimestamp + '.log'
        with open(logfilename, 'a+') as log_file:
          # Write a line containing the flickr ID, file link, wordpress id, and the HTTP status
          log_file.write(fileid + '|' + filelink + '|' + wpid + '|' + str(res.status_code) + '\n')
          print(filelink + ' updated!')
      
