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

#URL pattern for links to tweets
TWEET_URL="https://twitter.com/%s/status/%s"

#Some emoji
EMOJI_THUMBS_UP="\U0001f44d"
EMOJI_THUMBS_DOWN="\U0001f44e"
EMOJI_SHRUG="¯\\_(\u30c4)_/¯"

#max number of characters in a tweet
MAX_TWEET_SIZE=140

#NUMBER OF WORKER THREADS processing tweets
NUM_THREADS=100

#max time in seconds that workers wait for new task on queue
QUEUE_TIMEOUT_S=5*60

#number of retries to attempt when an error occurs 
API_RETRY_COUNT=60


#number seconds to wait between retries 
API_RETRY_DELAY_S=1

#http status codes for which to retry
API_RETRY_ERRORS=[400,401,500,502,503,504]

class Twitter:
    """ Helper for talking to Twitter APIs"""

    def __init__(self,logs_to_cloud):
        self.logs_to_cloud=logs_to_cloud
        self.logs=Logs(name="twitter",to_cloud=self.logs_to_cloud)
        self.twitter_auth=OAuthHandler(TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET)
        self.twitter_auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.twitter_api=API(auth_handler=self.twitter_auth,retry_count=API_RETRY_COUNT,retry_delay=API_RETRY_DELAY_S,retry_errors=API_RETRY_ERRORS,wait_on_rate_limit="True",wait_on_rate_limit_notify=True)
        self.twitter_listener=None


    def start_streaming(self,callback):
        """ Starts streaming tweets and returning data to callback"""


        self.twitter_listener=TwitterListener(callback=callback,logs_to_cloud=self.logs_to_cloud)
        twitter_stream=Stream(self.twitter_auth,self.twitter_listener)

        self.logs.debug("Starting stream")
        twitter_stream.filter(follow=[TRUMP_USER_ID])
        
        #IF we got here because of API error,raise it
        if self.twitter_listener and self.twitter_listener.get_error_status():
            raise Exception("Twitter API error: %s"% self.twitter_listener.get_error_status())




    def stop_streaming(self):
        """ stops current stream"""


        if not self.twitter_listener:
            self.logs.warn("No stream to stoo")
            return


        self.logs.debug("Stopping stream.")
        self.twitter)listener.stop_queue()
        self.twitter_listener=None


    def tweet(self,companies,tweet):
        """ Posts tweet listing the companies, ticker symbols, and quote of original tweet"""

        link=self.get_tweet_link(tweet)
        text=self.make_tweet_text(companies, link)

        self.logs.info("Tweeting: %s" % text)
        self.twitter_api.update_status(text)


    def make_tweet_text(self,companies,link):
        """Generates text for a tweet"""

        #Find all distinct company names
        names=[]
        for company in companies:
            name=compnay["name"]
            if name not in names:
                names.append(name)




        #collect ticker symbols and sentiment scores for each name
        tickers={}
        sentiments={}
        for name in names:
            tickers[name]=[]
            for company in companies:
                if compnay["name"]==name:
                    ticker=company["ticker"]
                    tickers[name].append(ticker)
                    sentiment=company["sentiment"]
                    #assuming same sentiment for each ticker
                    sentiments[name]=sentiment


        #create lines for each name with sentiment emoji and ticker symbols
        lines=[]
        for name in names:
            sentiment_str=self.get_sentiment_emoji(sentiments[name])
            tickers_str=" ".join(["$%s" % t for t in tickers[name]])
            line="%s %s %s" % (name,sentiment_str,tickers_str)
            lines.append(line)



        #Combine lines and ellipsize if necessary
        lines_str="\n".join(lines)
        size=len(lines_str)+1+len(link)
        if size>MAX_TWEET_SIZE:
            self.logs.warn("Ellipsizing lines: %s" % lines_str)
            lines_size=MAX_TWEET_SIZE-len(link)-2
            lines_str="%\u2026" % lines_str[:lines_size]


        #combine lines with link
        text="%s\n%s" % (lines_str,link)
        return text


    def get_sentiment_emoji(self,sentiment):
        """Returns emojji matching sentiment"""


        if not sentiment:
            return EMOJI_SHRUG


        if sentiment>0:
            return EMOJI_THUMBS_UP

        if sentiment<0:
            return EMOJI_THUMBS_DOWN

        self.logs.warn("Unknown sentiment: %s" % sentiment)
        return EMOJI_SHRUG

    def get_tweet(self,tweet_id):
        """ Looks up metadata for single tweet"""

        # Use tweet_mode=extended so we get the full text
        status=self.twitter_api.get_status(tweet_id,tweet_mode="extended")
        if not status:
            self.logs.error("Bad status response: %s" % status)
            return None


        # Use raw JSON just like streaming API
        return status._json

    def get_tweets(self,since_id):
        """ Looks up metadata for all Trump tweets since the specified ID"""

        tweets=[]

        #Include first ID by passing along an earlier one
        since_id=str(int(since_id)-1)

        #use tweet_mode=extended so we get full text
        for status in Cursor(self.twitter_api.user_timeline,user_id=TRUMP_USER_ID,since_id=since_id,tweet_mode="extended").items();
        #use raw json just like streaming api
            tweets.append(status._json)


        self.logs.debug("Got tweets: %s" % tweets)

        return tweets
    
    def get_tweet_text(self,tweet):
        """Returns full text of a tweet"""

        #forma