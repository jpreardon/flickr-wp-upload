#!/usr/bin/env python

from PIL import Image
import sys
import os
import pprint
import piexif

pp = pprint.PrettyPrinter(indent=4)

infile = 'test.jpg'
outfile = 'test-rot.jpg'

im = Image.open(infile)

print(im.format, im.size, im.mode)

exif_dict = piexif.load(im.info["exif"]) 
orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)

# pp.pprint(exif_dict)

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
# quality='keep' doens't work here since the format is no longer 'JPEG' after
# rotating. I'm setting to 93 since that seems to get pretty close to the 
# original file size of the image I was testing with. TODO: Must be a better way
im.save(outfile, 'JPEG', exif=exif_bytes, quality=93)

#im.save(outfile)
print(im.format, im.size, im.mode)