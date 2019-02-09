# Worklog

## 2019-02-09

*The journey of a thousand miles begins with one step.*

- Initialize a repository with the requisite README, LICENCE and worklog.
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
    --header "content-disposition: attachment; filename=test.jpg" \
    --header "authorization: Basic [Base 64 encoded application password]" \
    --header "content-type: image/jpeg" --data-binary "@test.jpg" \
    --location
    ```
    - Not exactly sure how to add descriptions and such, that might need to get done with a subsequent post (someone on the internet said that)
