# Flickr to Wordpress Uploadr

These scripts import pictures and data from Flickr to Wordpress. Specifically, they use the photos and JSON files downloaded from Flickr when you request all of your data.

[I downloaded my data from Flickr](https://jpreardon.com/2019/01/13/flickr-download/) in early 2019--ahead of Flickr's retention policy change. These are the scripts I used to [move everything to my existing Wordpress site](https://jpreardon.com/2019/02/18/flickr-download-part-2/).

While **these scripts aren't intended for use by the general public**, I'm putting them here with the hope that they might be a starting point for at least one other person. Here's what they do:

- Upload all photos to a Wordpress site via the REST API
- Photos marked as private on Flickr will get a status of "private" on Wordpress
- Update the photo titles and descriptions with those from Flickr's JSON files (if those fields exist).
- Tags are written in the description of the photo on Wordpress as is the date taken.
- Comments are re-created on the photos in Wordpress, with the original comment date and the Flicker user's name (if they are still a Flickr user)
- A post is created for each album (in draft status) containing a classic Wordpress gallery with the photos from the Flickr album.
- Keeps (a lot) of log files of what happened, both good and bad.
- Leave the photos and data untouched on your local machine.

If you are going to attempt importing a load of stuff into your Wordpress installation, I strongly suggest you do it to a test site first. I followed my own advice here, and I'm glad I did.

## Prerequisites 

- A Wordpress site
- [Application Passwords](https://wordpress.org/plugins/application-passwords/) plugin
- A Flickr API key--only if you want to import the comments for each picture. The JSON file does not include the username.
- An archive of all of your Flickr activity. *You can request this on your Flickr settings page.*
  - Photos come in in several zip files. After unzipping, put all the photos in one directory.
- Python dependencies 
  - [pipenv](https://pipenv.readthedocs.io/en/latest/)
  - [requests](http://docs.python-requests.org/en/master/)
  - [pillow](https://python-pillow.org/)
  - [piexif](https://pypi.org/project/piexif/)

## Running the Scripts

The scripts need to be run in this order. All of the paths and authorization keys are passed as command line arguments. The second two scripts take the upload_DDDDD.log file as input.

```
pipenv run python upload-images.py https://example.com/wp-json/wp/v2/media [authentication key] [/path/to/photos]
```

```
pipenv run python update-meta-data.py http://example.com//wp-json/wp/v2/ [authentication key] [/path/to/flickr/json/files] [upload_.log file from upload-images.py] [flickr API key]
```
```
pipenv run python create-posts.py http://example.com//wp-json/wp/v2/ [authentication key] [/path/to/flickr/albums.json] [upload_.log file from upload-images.py] 
```

The [worklog](worklog.md) documents my somewhat winding path.
