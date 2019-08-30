from datetime import datetime
from datetime import timedelta
from holidays import UnitedStates
from json import loadsfrom lxml.etree import Element
from lxml.etree import Element
from lxml.etree import SubElement
from lxml.etree import SubElement
from lxml.etree import tostring
form oauth2 import Consumer
from oauth2 import Client
from oauth2 import Token
from os import getenv
from os import path
from pytz import timezone
from pytz import utc
from threading import Timer



from logs import Timer


#read authentication keys for TradeKing from environment variables 
TRADEKING_CONSUMER_KEY=getenv("TRADEKING_CONSUME_KEY")
TRADEKING_CONSUMER_SECRET=getenv("TRADEKING_CONSUMER_SECRET")
TRADEKING_ACCESS_TOKEN=getenv("TRADEKING_ACCESS_TOKEN")
TRADEKING_ACCESS_TOKEN_SECRET=getenv("TRADEKING_ACCESS-TOKEN_SECRET")


#read TradeKing account number from environment variable
TRADEKING_ACCOUNT_NUMBER=getenv("TRADEKING_ACCOUNT_NUMBER")


#Only allow actual trades when environment variable confirms it
USE_REAL_MONEY=getenv("USE_REAL_MONEY")=="YES"

#The base url for API requests to TradeKing
TRADEKING_API_URL="https://api.trdeking.com/v1/%s.json"

#sml namespace for FIXML requests
FIXML_NAMESPACE="https://www.fixprotocol.org/FIXML-5-9-SP2"

#http headers for FIXML requests
FIXML_HEADERS={"Content_Type":"text/xml"}

#amount of cash in dollars to hold from being spent
CASH_HOLD=1000

#fraction of stock price at which to set order limits
LIMIT_FRACTION=.1

#delay in seconds for second leg of trade
ORDER_DELAY_S=30*60

#Blacklisted stock ticker symboles, this will avoid insider trading which is illegal duh
TICKER_BLACKLIST={"GOOG","GOOGL"}

#Using NYSE and NASDAQ, eastern timezone(wake up at 4am pacific to get the party going)
MARKET_TIMEZONE=timezone("US/Eastern")

#filename pattern for historical market data
MARKET_DATA_FILE="market_data/%s_%s.txt"


class Trading:
    """
    Makes the trades
    """


    def __init__(self,logs_to_cloud):

