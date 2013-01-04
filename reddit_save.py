"""
reddit_save.py

Manages a user's reddit saved links in a mongodb database.

author: Shang-Lin Chen
created: Nov. 26, 2012
"""

import pymongo
import requests
import json
from pprint import pprint

def setup_session():
    """
    Creates and returns a Requests session.
    """
    # Create a new session.                  
    client = requests.session()
    return client

def get_credentials():
    """
    Extracts Reddit login credentials from the file .reddit.
    Returns a tuple of the format (username, password).
    """
    with open('.reddit', 'r') as f:
        if not f:
            print "Could not open .reddit."
        (username, password) = f.readline().split(':')
        username.rstrip('\r\n')
        password.rstrip('\r\n')
        return (username, password)
        
def login(client, username, password):
    """
    Logs in to a Reddit account and sets the modhash.
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
    Returns a dictionary of json documents containing a user's saved links.
    The reddit API can only return a maximum of 100 links.
    args: client -- a requests session
          username
            
    """
    url = 'http://www.reddit.com/user/{USER}/saved/.json?limit=100'.format(USER=username)
    print url
    resp = client.get(url)
    json_docs = json.loads(resp.text)
    pprint(json_docs)
    return json_docs['data']['children']

def add_to_db():
    pass
    
if __name__ == '__main__':
    client = setup_session()
    
    #pprint(resp.text)
    (username, password) = get_credentials()
    print username
    print password
    login(client, username, password)
    
    # Get list of links.
    saved = get_saved(client, username)
    pprint(saved)
    n = 0
    for doc in saved:
        n += 1
        pprint(doc)

    print '{NUM} documents found'.format(NUM=n)    
    
    connection = pymongo.Connection("mongodb://localhost", safe=True)
    db = connection.reddit
    collection = db[username]