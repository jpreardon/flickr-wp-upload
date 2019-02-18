import requests
import sys
import json
import os
import datetime

try:
  sys.argv[4]
except IndexError:
  argverrormsg = 'Error, wrong number of arguments!\n'
  argverrormsg += 'Usage: $ update-meta-data.py [WP REST endpoint URL] [application password] [album json file path] [upload log file]'
  sys.exit(argverrormsg)
else:
  url = sys.argv[1]
  app_password = sys.argv[2]
  album_file = sys.argv[3]
  logfile = sys.argv[4]

# This is the ID of the wordpress category for the new posts, if zero, they will be uncategorized
category_id = 0 #93

# Get the start time, we'll use this for the output files
starttimestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Log file subdirectory
log_dir = 'logs/'

# Create a log file directory, if it doesn't exist
if not os.path.isdir(log_dir):
  os.makedirs(log_dir)

# Get the wpids for all of the photos
photo_ids = {}
upload_log = open(logfile, 'r')
for line in upload_log:
  photo_ids[line.split('|')[0]] = line.split('|')[3].rstrip()

# Headers for REST calls to wordpress
headers = {
  'cache-control': 'no-cache',
  'authorization': 'Basic %s' % app_password,
  'content-type': 'application/json'
}

# Open the albums json file
with open(album_file, 'r') as file:
  album_info = json.load(file)

# For each album...
for album in album_info['albums']:
  # create a post (using the title as the title, description as description, bonus: insert the featured photo)

  # Create the gallery content
  # adding link="file" will link directly to the image files, I'm opting for the attachment pages instead
  # adding columns="2", or whatever will change the number of columns in the gallery
  gallery_content = '<p>[gallery columns="3" ids="'
  for photo in album['photos']:
    # If there was an error uploading a photo, it won't be in this list
    # skip it (silently) rather than getting an error.
    if photo in photo_ids:
      gallery_content += photo_ids[photo] + ","
  # Remove the last comma
  gallery_content = gallery_content[:len(gallery_content) - 1]
  gallery_content += '"]</p>'

  if album['description']:
    post_content = '<p>' + album['description'] + '</p>\n' + gallery_content
  else:
    post_content = gallery_content

  # Build the payload
  payload = {}
  payload['status'] = 'draft'
  payload['title'] = album['title']
  payload['content'] = post_content
  if category_id > 0:
    payload['categories'] = [category_id] 

  res = requests.post(url + 'posts', json = payload, headers = headers)

  if res.status_code != 201:
    errlogname = 'post_create_error_' + starttimestamp + '.log'
    with open(log_dir + errlogname, 'a+') as log_file:
      # Write a line with the album title and HTTP status
      log_file.write('write to wordpress' + '|' + album['title'] + '|' + str(res.status_code) + '\n')
      print('Error creating post ' + album['title'] + ': ' + str(res.status_code))
  else:
    post_id = res.json()['id']
    logfilename = 'post_create_' + starttimestamp + '.log'
    with open(log_dir + logfilename, 'a+') as log_file:
      # Write a line containing the album title, post id, and the HTTP status
      log_file.write('write to wordpress' + '|' + album['title'] + '|' + str(post_id) + '|' + str(res.status_code) + '\n')
      print('Post created for ' + album['title'] + ': ' + str(res.status_code))

    # Build the payload
    payload = {'post': post_id}

    for photo in album['photos']:

      # If there was an error uploading a photo, it won't be in this list
      # skip it (silently) rather than getting an error.
      if photo in photo_ids:

        # Attach photos to posts by updating each photo with the post ID
        res = requests.post(url + 'media/' + photo_ids[photo], json = payload, headers = headers)
        if res.status_code != 200:
          errlogname = 'media_attach_error_' + starttimestamp + '.log'
          with open(log_dir + errlogname, 'a+') as log_file:
            # Write a line with the album title, wp photo id and HTTP status
            log_file.write('attach media' + '|' + album['title'] + '|' + photo_ids[photo] + '|' + str(res.status_code) + '\n')
            print('Error attaching ' + photo_ids[photo] + ' to ' + album['title'] + ': ' + str(res.status_code))
        else:
          post_id = res.json()['id']
          logfilename = 'media_attach__' + starttimestamp + '.log'
          with open(log_dir + logfilename, 'a+') as log_file:
            # Write a line with the album title, wp photo id and HTTP status
            log_file.write('attach media' + '|' + album['title'] + '|' + photo_ids[photo] + '|' + str(res.status_code) + '\n')
            print('Attached ' + photo_ids[photo] + ' to ' + album['title'] + ': ' + str(res.status_code))

