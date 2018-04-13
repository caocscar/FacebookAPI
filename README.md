# Facebook Graph API
This repository has some sample code from helping CSCAR clients for extracting data from the Facebook Graph API. This uses the `requests` library to make GET requests to the API. I then take the JSON response and extract some subset of the response.

Example code is provided in `sample_code.py`. You need to provide your **User Access Token** in `facebook_api_functions.py` before starting.

`facebook_api_functions.py` contains functions to do the following:
- Get user id for username.
- Get posts, feed or comments for a node (i.e. user, comment).
- Get reactions from posts.
- Get reactions from comments.

## Node/Edge Relation Table

Node|Edge|Use Cases
---|---|---
User|Posts|Get posts from a user; Get reactions from a post
User|Feed|Get user's feed
Posts|Comments|Get comments from a post
Comments|Reactions|Get reactions from a comment

## User Access Token
Get one at https://developers.facebook.com/tools/explorer/.  You need to login to use it.
