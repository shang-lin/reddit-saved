"""
reddit_save.py

Connects to a reddit user account and downloads saved posts into a mongodb database.
"""

import pymongo
import requests
import json
from pprint import pprint

username = ''
password = ''

def setup_session():
    """
    Create and return a Requests session.
    """
    # Create a new session.                  
    client = requests.session()
    return client

def get_credentials():
    """
    Obtain Reddit login credentials from the file .reddit.
    """
    with open('.reddit', 'r') as f:
        if not f:
            print "Could not open .reddit."
        lines = f.readlines()
        username = lines[0]
        password = lines[1]
        
def login(client, username, passwordd):
    """
    Login to a Reddit account and set the modhash.
    """
    # Create dictionary of login info.
    user_pass_dict = {'user': username,
                      'passwd': password,
                      'api_type': 'json'}
                  
    # Send the login info to the API and store the response.
    r = client.post(r'http://www.reddit.com/api/login', data=user_pass_dict)
    #pprint(r.text)
    # Convert the response JSON to a Python dict.
    j = json.loads(r.text)
    client.modhash = j['json']['data']['modhash']
    #print '{USER}\'s modhash is {mh}'.format(USER=username, mh=client.modhash)

def get_saved(client, username):
    """
    Return a dictionary of json documents containing a user's saved links.
    args: client -- a requests session
          username
            
    """
    url = 'http://www.reddit.com/user/{USER}/saved/.json?limit=100'.format(USER=username)
    print url
    resp = client.get(url)
    json_docs = json.loads(resp.text)
    return json_docs['data']['children']

    
if __name__ == '__main__':
    client = setup_session()
    
    #pprint(resp.text)
    get_credentials()
    login(client, username, password)
    
    # Get list of links.
    saved = get_saved(client, username)
    pprint(saved)
    n = 0
    for doc in saved:
        n += 1
        pprint(doc)

    print '{NUM} documents found'.format(NUM=n)    