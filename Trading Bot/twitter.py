from json import loads
from os import getenv
from queue import Empty
from queue import Queue
from threading import Thread
from threading import Event
from time import time 
from tweepy import API
from tweepy import Cursor
from tweepy import QAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


from logs import Logs


#The keyso for the Twitter account for API request and tweeting
#alerts@Trump2Cash) Read from environment variables
TWITTER_ACCESS_TOKEN=getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET=getenv("TWITTER_ACCESS_TOKEN_SECRET")

#KEYS FOR THE TWITTER APP WE'RE USING FOR API REQUESTS
#HTTPS://APPS.TWITTER.CON/APP/13239588 READ FROM ENVIRONMENT VARIABLES
#TODO TWITTER API
TWITTER_CONSUMER_KEY=getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET=getenv("TWITTER_CONSUMER_SECRET")

#user ID of @realDonaldTrump
TRUMP_USER_ID="25073877"


