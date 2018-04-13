# -*- coding: utf-8 -*-
"""
This script contains functions to do the following:
    Get user id for username.
    Get posts, feed or comments for a node (i.e. user, comment).
	Get reactions from posts.
	Get reactions from comments.
    
IMPORTANT:
You will need your own access_token from 
https://developers.facebook.com/tools/explorer
as it expires in 1-2 hrs at the top of the hour
"""

import requests
import pandas as pd

access_token = 'EAACEdEose0cBAAEj1huezW8iulXOSNJ0rCZBeRzJ8VTruA1jZCTgZBZCY7G66q6QGATKpv9c1ZBbMD3yxuMKPbf2XjTlWOBikvZC3EhUEavGVmHpd3xVFxGIruy1DS9RjCvdv2xIbIdO2n5uXdRKh00MRCD5edZAYNkV8eC0VYPbsZBVPkTBEstttoG7J7u1G3HBmbRYKLUVSLlCBnpaSURC'

version = '2.12'
baseurl = 'https://graph.facebook.com/v{}'.format(version)

#%% get user id
def get_user_id(username):
    """
    Get user id for username.
    
    Parameters
    ----------
    username: str
        username
  
    Returns
    -------
    string
        user id
    """
    params = {'access_token': access_token,
              'fields': 'id,name'}
    url = '{}/{}'.format(baseurl,username)
    R = requests.get(url, params=params)
    R.raise_for_status()
    return R.json()['id']
    
#%% get user posts or feed
def get_posts_feed_comments(nodeid, edge, count=100):
    """    
    Get posts, feed or comments for a node (i.e. user, comment).
    
    Parameters
    ----------
    nodeid: str
        id of the node in question
    edge: str
        edge type you are looking for
    count: int
        max number of results to return per page
  
    Returns
    -------
    DataFrame
        Columns: ['timestamp','parentid','id','message']   
    """
    assert edge in ['posts','feed','comments']
    params = {'access_token': access_token,
              'limit': count}
    if edge in ['posts','feed']:
        params['fields'] = 'from,message,picture,link,name,type,created_time,shares,likes.summary(total_count)'
    else: # comments
        params['fields'] = 'message,created_time,like_count'
        if any(c.isalpha() for c in nodeid):
            print('Looks like the comment_id has alphabet characters which is incorrect')
            return pd.DataFrame()
    url = '{}/{}/{}'.format(baseurl,nodeid,edge)   
    counter = 0
    list_posts = []
    while True:
        counter += 1
        print('{0} {1} Page {2}'.format(nodeid, edge, counter))
        R = requests.get(url, params=params)
        R.raise_for_status()
        response = R.json()
        for i, post in enumerate(response['data']):
            timestamp = post['created_time']
            postid = post['id']
            message = post.get('message','')
            list_posts.append((timestamp,postid,message))
        flag = response['paging'].get('next', False)
        if flag:
            params['after'] = response['paging']['cursors']['after']
        else:
            break
        
    columns = ['timestamp','id','message']
    df = pd.DataFrame(list_posts, columns=columns)
    df.insert(0, 'parentid', nodeid)
    return df

#%%
def get_posts_reactions(nodeid, *, count=100, reactions=[]):
    """
    Get reactions from posts.
    
    Parameters
    ----------
    nodeid: str
        id of the node in question
    count: int
        max number of results to return per page
	reactions: list
		list of reactions interested in
    Returns
    -------
    DataFrame
        Columns: ['parentid','id','reaction1','reaction2','reaction3', etc...]   
    """    
    reaction_set = set(['NONE','LIKE','LOVE','WOW','HAHA','SAD','ANGRY','THANKFUL'])
    R = set(reactions)
    nomatch = R.difference(reaction_set)
    if nomatch:
        print('{} is invalid reaction. Choose from {}'.format(nomatch, reaction_set))
        return pd.DataFrame()
    list_reactions = []
    url = '{0}/{1}/posts'.format(baseurl,nodeid)
    for reaction in reactions:
        params = {'access_token': access_token,
                  'limit': count}
        pg = 0
        while True:
            pg += 1
            print('{0} posts reaction {1} Page {2}'.format(nodeid, reaction, pg))
            params['fields'] = 'reactions.type({}).summary(total_count)'.format(reaction)
            R = requests.get(url, params=params)
            R.raise_for_status()
            response = R.json()
            for i, post in enumerate(response['data']):
                postid = post['id']
                reaction_count = post['reactions']['summary']['total_count']
                list_reactions.append((postid,reaction,reaction_count))
            flag = response['paging'].get('next', False)
            if flag:
                params['after'] = response['paging']['cursors']['after']
            else:
                break
    columns = ['id','reaction','count']
    df = pd.DataFrame(list_reactions, columns=columns)
    df = df.pivot(index='id', columns='reaction', values='count').reset_index()
    df.insert(0, 'parentid', nodeid)
    return df    

#%%
def get_comment_reactions(nodeid, *, count=100, reactions=[]):
    """
    Get reactions from comment.
    
    Parameters
    ----------
    nodeid: str
        id of the node in question
    count: int
        max number of results to return per page
	reactions: list
		list of reactions interested in
    Returns
    -------
    DataFrame
        Columns: ['parentid','id','reaction1','reaction2','reaction3', etc...]   
    """
    reaction_set = set(['NONE','LIKE','LOVE','WOW','HAHA','SAD','ANGRY','THANKFUL'])
    R = set(reactions)
    nomatch = R.difference(reaction_set)
    if nomatch:
        print('{} is invalid reaction. Choose from {}'.format(nomatch, reaction_set))
        return pd.DataFrame()
    if any(c.isalpha() for c in nodeid):
        print('Looks like the comment_id has alphabet characters which is incorrect')
        return pd.DataFrame()
    list_reactions = []
    url = '{0}/{1}/reactions'.format(baseurl,nodeid)   
    for reaction in reactions:
        params = {'access_token': access_token,
                  'limit': count,
                  'summary': 'total_count',
                  'type': reaction}
        print('{0} comment reaction {1} Page 1'.format(nodeid, reaction))
        R = requests.get(url, params=params)
        R.raise_for_status()
        response = R.json()
        reaction_count = response['summary']['total_count']
        list_reactions.append(reaction_count)              
    df = pd.DataFrame(list_reactions).transpose()
    df.columns = reactions
    df.insert(0, 'parentid', nodeid)
    return df
    