#!/usr/bin/env python

#import requests
import sys

url = sys.argv[1]
app_password = sys.argv[2]
filename = "test.jpg"

headers = {
  "cache-control: no-cache",
  "content-disposition: attachment; filename=%s" % filename,
  "authorization: Basic %s" % app_password,
  "content-type: image/jpeg"
}

# r = requests.post(url, headers = headers)

print headers