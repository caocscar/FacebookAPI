# -*- coding: utf-8 -*-
import facebook_api_functions as FB

#%% Example Usage
username = 'mukurudotcom'
userid = FB.get_user_id(username)

# get posts for a username
posts = FB.get_posts_feed_comments(username, 'posts')

# get feed for a username
feed = FB.get_posts_feed_comments(username, 'feed')

# get comments for a single post
comments = FB.get_posts_feed_comments(posts.at[0,'id'], 'comments')

# get reactions from posts
emotions = FB.get_posts_reactions(username, reactions=['LIKE','LOVE'])

# get reactions from comments
emotions = FB.get_comment_reactions(posts.at[0,'id'], reactions=['WOW','HAHA'])
