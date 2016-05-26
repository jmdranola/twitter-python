"""
*****************PRACTICE 1*****************
*******************SLACKERS*****************
Members:
- Gel Abad
- Jona Marie Ranola
- Gerald Ortega
- Diosa Bianca Biado
- Rohit Jainani
"""
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
import time
from slackclient import SlackClient

#twitter requirements
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "yfH5SdvnhQytoCst4Ej7VUBWp"
CONSUMER_SECRET = "FEzjBEi2zKvJkIyGkpD0szc5JW0mG0xCslDc3eWEy4X2hjboFs"

OAUTH_TOKEN = "1559420730-PIln8fYkhcYFBmyaLHDzakJwZYNgmxHk709p3XF"
OAUTH_TOKEN_SECRET = "YeSkgYh6ijsGLZosqDXetiTGj0D4mIGlZlTDzycRmkoKd"


#for slack bot
token = "xoxp-36519852806-42258330454-45556833778-1315beb58c"  #get this value from slack.
sc = SlackClient(token) #instanciate
sc.api_call("api.test")
sc.api_call("channels.info", channel="1234567890")




def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    print (credentials)
    print

    #gets the oauth token from the credentials and slice it.
    oauthToken = (str(credentials[b'oauth_token']))
    oauthToken = oauthToken[3:len(oauthToken)-2]

    print (oauthToken)

    #gets the oauth secret  from the credentials and slice it.
    oauthSecret = (str(credentials[b'oauth_token_secret']))
    oauthSecret = oauthSecret[3:len(oauthSecret)-2]

    print (oauthSecret)
                                   
    resource_owner_key =  oauthToken
    """credentials.get('oauth_token')"""
    resource_owner_secret = oauthSecret
    """credentials.get('oauth_token_secret')"""

    # Authorize
    authorize_url = AUTHORIZE_URL + str(resource_owner_key)
    print ('Please go here and authorize: ' + authorize_url)

    verifier = input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)
    
    print ("")
    print ("")
    print
    
    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    print (credentials)
    accessToken = (str(credentials[b'oauth_token']))
    accessToken = accessToken[3:len(accessToken)-2]

    print (accessToken)

    #gets the oauth secret  from the credentials and slice it.
    accessSecret = (str(credentials[b'oauth_token_secret']))
    accessSecret = accessSecret[3:len(accessSecret)-2]

    token = accessToken
    secret = accessSecret

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print ("OAUTH_TOKEN: " + token)
        print ("OAUTH_TOKEN_SECRET: " + secret)
        print
    else:
        oauth = get_oauth()
        lst = []
        itr = 0
        trendingURL = "https://api.twitter.com/1.1/trends/place.json?id=1" #23424934  ->>> philippines WOEID
       
        r = requests.get(url=trendingURL, auth=oauth)
        result = ascii(r.json())
        print (type(r.json()))
        if sc.rtm_connect():
                while True:
                    for ctr in range(10): #to get only the top 10. 
                        topNo = ctr + 1;
                        value = r.json()[0]["trends"][ctr]["name"] #gets the "trends" inside a list and access the "name"       
                        lst.append(value)  # appends the result in a list. 
                        
                        
                    for item in lst:
                        str1 = "\n".join(lst) #access the list and convert it to string.
                        print (str1)
                        print (" ")

                        #prints the details in slack using RTM (real time messaging)
                        sc.api_call(
                            "chat.postMessage",
                            channel="#slackers",
                            text = str1,
                            username='twitterbot',
                            icon_emoji=':broken_heart:')
                        sc.rtm_read()
                        time.sleep(3600)
            


    
