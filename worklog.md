# Worklog

## TODO

- Update images with metadata
- Set "private" photos to private?
- Create albums
- Keep error log when uploading/updating?
- Refactor rotation code
- Move files to a subdirectory after load (as an option)?
- Stream photos instead of straight post?

## Overall Notes

### Dependencies 

- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- [requests](http://docs.python-requests.org/en/master/)
- [pillow](https://python-pillow.org/)
- [piexif](https://pypi.org/project/piexif/)

## 2019-02-17

- Working on updating meta data

- Tags: It seems that any tags added by me, or another user are in the json file. The ones added by flickr's bots are not.
- Some photos don't have names (titles). By default, they are getting the filename as the title on upload. 
- I'm striping the flicker ID from those filenames now when they get uploaded
- Add the flickr ID to the upload.log
-  In some cases, the flickr ID was not where I expected it to be in the file name. It seems that the pattern is reversed (2248328315_058f0b8c35_o.jpg). I have a feeling these images never had a file name, so flickr assigned something, not sure why they would reverse the order in the filename though.

## 2019-02-16

- Checking the HTTP status after the upload to make sure it was successful (201)
- The image rotation issue is bugging me. Should try to solve that before moving on, otherwise, the media library will be a huge mess.
- Automatically rotating the images in Wordpress doesn't seem to be an option. I tried this [plug-in](https://wordpress.org/plugins/fix-image-rotation/), but it caused the API calls to fail. Rotating it within Wordpress also seems to remove a fair amount of the EXIF data. That's not a huge deal, but it's slow and manual.
- Installed [pillow](https://python-pillow.org/) in the virtual env.
- [This post](https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image) helped me read the EXIF information from the image, I am most interested in ["Orientation"](http://sylvana.net/jpegcrop/exif_orientation.html) at this point.
- Things I learned about rotating images with pillow
  - Image.rotate(270) rotated the image, but kept the original dimensions, resulting in some clipping. [This article](https://dzone.com/articles/image-processing-in-python-with-pillow) explains this pretty clearly and talks about the "expand" option. 
  - Image.transpose(Image.ROTATE_270) did what I expected it to do.
  - EXIF data does not get preserved in the new image. [piexif](https://pypi.org/project/piexif/) seems to be the answer! There's an example [here](https://piexif.readthedocs.io/en/latest/sample.html#with-pil-pillow) of rotating an image based on the EXIF orientation value (and removing that value). I'm tried the same, but changed the value to "1" and it seemed to work fine both locally and after upload to Wordpress.
  - Rotated images were smaller than the original. That was due to the quality setting when saved. I set it at 93 rather than the default 75.
- upload-images.py is not uploading properly rotated images to wordpress! The code could use some refactoring though.
- Some of the photos in my library are massive. I've been testing with one that is about 8MB. I added a variable for the save quality.


## 2019-02-15

Before I go much further, I want to set up a test environment rather than subjecting my personal site to the abuse repeatedly uploading and deleting images...

- Create a copy of my site
  - Database
  - Files
- Create a test set of images and JSON files (instead of trying to upload 2000 pictures every time)
- Modify script to take a directory name and attempt to upload everything in it.
- Log file name, the uploaded URL, and (wordpress) image ID to upload.log file.
- **Problem**: Many images are not rotated properly. I have a feeling this might require manual intervention. :(


## 2019-02-12

- Spent time trying to install python packages (I want requests). I tried just putting the requests directory here, but there are a lot of dependencies.
- I stopped avoiding the inevitable and [installed python 3](https://docs.python-guide.org/starting/install3/osx/#install3-osx)
- Also installed [pipenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref)
- Successfully sent an image to wordpress, [thanks stackoverflow](https://stackoverflow.com/questions/14365027/python-post-binary-data)! Also updated the meta data on the image.
- Here's how I'm thinking this will work:
  - Part 1, upload all the images. 
    - Just point a script at a directory with a bunch of images, upload every one of them
    - Keep a log file with a line for each file containing the file name, the uploaded URL, and maybe the image ID
    - Maybe keep a separate error log
    - Maybe convert the "success log" to a JSON file
  - Part 2, update all the meta data for the uploaded files from the photo_...json files (meta data is sparse on a lot of photos). This could be driven off of the log file created above.
    - Title = name
    - Description = description + date_taken + tag list?
    - Comments? Can I get the comments in there somehow? 
  - Part 3, create albums from the albums.json file.
    - Each album will be a new post with a gallery?
    - Category = flickr
    - Title = title
    - Description = description
    - There is a cover photo in the json file, maybe that can be the featured photo?
  - Things I'm going to lose
    - Tags?
    - Notes: Some photos have notes, I'm just going to ignore them
    - Sets & galleries. I never had any of these on flickr, so no loss for me.
    - Testimonials... meh.
    - Privacy settings. I know I have a bunch of photos that were friends & family or private. I'm thinking I'm OK opening it up now. However, I might want to make note of which ones were not public in the log files I'm producing so I can go back and look at them.

## 2019-02-10

- Started to get API call for image upload working in Python
- Looks like the [requests](http://docs.python-requests.org/en/master/) library might be the one to use for accessing the API

## 2019-02-09

*The journey of a thousand miles begins with one step.*

- Initialize a repository with the requisite README, LICENSE and worklog.
- Did some analysis of how this might work:
  - There's a [flickr-to-wp plugin](https://github.com/bradt/flickr-to-wp). It hasn't been updated since 2011 though. This takes photos directly from Flickr, so not exactly what I want to do.
  - I think things should map out like this:
    - Photos get [uploaded](https://developer.wordpress.org/rest-api/reference/media/#create-a-media-item) as media. 
    - There is no native tag support for media, but there is a [plugin](https://wordpress.org/plugins/enhanced-media-library/), an alternative might be to create albums for each tag, or just put in tag as hash tags in the descriptions.
    - Albums are represented by posts with galleries
    - Comments, not sure what to do here. Could attempt to add as actual comments
      - The author names would require a call to Flickr since they don't seem to be included in the data
      - Does anyone care about these comments?
  - Managed to upload an image file to my WP instance with CURL
    - Thanks to [this post](https://stackoverflow.com/questions/37432114/wp-rest-api-upload-image)
    - Also had to install the [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin.
    - Here's the command I used
    ```
    curl --request POST \
    --url https://jpreardon.com/wp-json/wp/v2/media \
    --header "cache-control: no-cache" \
    --header "content-disposition: attachment; filename=test1.jpg" \
    --header "authorization: Basic [Base 64 encoded application password]" \
    --header "content-type: image/jpeg" --data-binary "@test.jpg" \
    --location
    ```
    - Not exactly sure how to add descriptions and such, that might need to get done with a subsequent post (someone on the internet said that)