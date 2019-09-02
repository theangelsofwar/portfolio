from datetime import datetime
from datetime import timedelta
from holidays import UnitedStates
from json import loadsfrom lxml.etree import Element
from lxml.etree import Element
from lxml.etree import SubElement
from lxml.etree import SubElement
from lxml.etree import tostring
from oauth2 import Consumer
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
        self.logs=Logs(name="trading", to_cloud=logs.to_cloud)


    def make_trade(self,companies):
        """
        Executes trae for specified companies based on sentiment

        """


    #determin whether markets are open
    market_status=self.get_market_status()
    if not market_status:
        self.logs.error("Not trading without market status")
        return False

    #Filter for any strategies resulting in trades
    actionable_strategies=[]
    market_status=self.get_market_status()
    for company in companies:
        strategy=self.get_strategy(company, market_status)
        if stategy["action"]!="hold":
            actionable_strategies.append(strategy)
        else:
            self.logs.warn("Dropping strategy: %s"%strategy)


    if not actionable_strategies:
        self.logs.warn("No actionable strategies for trading")
        return False


    #calculate budget per strategy
    balance=self.get_balace()
    budget=self.get_budget(balance, len(actionable_strategies))


    if not budget:
        self.logs.warn("No budget for trading: %s %s %s"%(budget, balance, actionable_strategies))
        return False


    self.logs.debug("Using budget: %s x %s"%len(actionable_strategies),budget))


    #Trader Handler for each strategy
    success=Truefor strategy in actionable_strategies:
    ticker=strategy["ticker"]
    action=stratey["action"]


    #Execute Strategy
    if action=="bull":
        self.logs.info("Bull: %s %s" %(ticker,budget))
        success=success and self.bull(ticker,budget)
    elif action=="bear": 
        self.logs.info("Bull%s %s" %(ticker,budget))
        success=success and self.bear(ticker,budget)
    else:
        self.logs.error("Unknown strategy: %s"% strategy)

return success


def get_strategy(self,company,market_status):
    """Determines strategy for trading company based on sentiment and market status
    """


    ticker=company["ticker"]
    sentiment=company["sentiment"]


    strategy={}
    strategy["name"]=company["name"]
    if "root" in company:
        strategy["root"]=company["root"]
    strategy["sentiment"]=company["sentiment"]
    strategy["ticker"]=ticker
    strategy["exchange"]=company["exchange"]


    #don't do anything with blacklisted stocks
    if ticker in TICKER_BLACKLIST:
        strategy["action"]="hold"
        strategy["reason"]="blacklist"
        return strategy

    #Don't trade unless marketsopen or about to open
    if market_status!="open" and market_status!="pre":
        strategy["action"]="hold"
        strategy["reason"]="market closed"
        return strategy


    #can't trade without sentiment
    if sentiment==0:
        strategy["action"]="hold"
        strategy["reason"]="neutral sentiment"
        return strategy


    #determin bull or bear based on sentiment direction
    if sentiment>-:
        strategy["aciton"]="bull"
        strategy["reason"]="positive sentiment"
        return strategy
    else: 
        strategy["action"]="bear"
        strategy["reason"]="negative sentiment"
        return strategy


def get_budget(self,balance,num_strategies):
    """
    Calculates budget per company based on available balance
    """
    if num_strategies<=0:
        self.logs.warn("No budget without strategies.")
        return 0.0
    return round(max(0.0,balance-CASH_HOLD)/num_strategies,2)


def get_market_status(self):
    """ Finds out whether markets are open at the present moment
    """


    clock_url=TRADEKING_API_URL % "market/clock"
    response=self.make_request(url=clock_url)


    if not response:
        self.logs.error("No clock response")
        reutnr None

    try:
        clock_response=response["response"]
        current=clock_response["status"]["current"]
    except KeyError:
        self.logs.error("Malformed clock response: %s" % response)
        return None
    

    if current not in ["pre","open","after","close"]:
        self.logs.error("Unknown market status: %s" % current)
        return None
    

    self.logs.debug("Current market status: %s"% current)
    return current


def get_historical_prices(self,ticker,timestamp):
    """
    Finds last price at or before timestamp at EOD
    """
    quotes=self.get_day_quotes(ticker,timestamp)
    if not quotes:
        self.logs.warn("No quotes for day: %s" % timestamp)
        return None


    #depending on where we land relative to trading day. pick right quote and EOD quote
    first_quote=quotes[0]
    first_quote_time=first_quote["time"]
    last_quote=quotes[-1]
    last_quote_time=last_quote["time"]
    if timestamp<first_quote_time:
        self.logs.debug("Using previous quote")
        previous_day=self.get_previous_day(timestamp)
        previous_quotes=self.get_day_quotes(ticker,previous_day)
        if not previous_quotes:
            self.logs.error("No quotes for previous day: %s"% previous_day)
            return None 
        quote_at=previous_quotes[-1]
        quote_eod=last_quote
    elif timestamp>=first_quote_time and timestamp<=last_quote_time:
        self.logs.debug("Using closest quote")
        #walk through quotes until we step over timestamp
        previous_quote=first_quote
        for quote in quotes:
            quote_time=quote["time"]
            if quote_time>timestamp:
                break
            previous_quote=quote
        quote_at=previous_quote
        quote_eod=last_quote
    else: #timestamp>last_quote_time
        self.logs.debug("Using last quote.")
        quote_at=last_quote
        next_day=self.get_next_day(timestamp)
        next_quotes=self.get_day_quotes(ticker,next_day)
        if not next_quotes:
            self.logs.error("No quotes for next day: %s" % next_day)
            return None
        quote_eod=next_quotes[-1]


    self.logs.debug("Using quotes: %s %s" % (quote_at,quote_eod))
    return {"at": quote_at["price"],"eod":quote_end["price"]}


def get_day_quotes(self,ticker,timestamp):
    """ Collects all quotes form day of market timestamp
    """


    #Timestamp is expected in market time
    day=timestamp.strftime("%Y%m%d")
    filename=MARKET_DATA_FILE % (ticker,day)


    if not path.isfile(filename):
        self.logs.error("Day quotes not on file for: %s %s" %(ticker,timestamp))
        return None


    quotes_file=open(filename,"r")
    try:
        lines=quotes_file.readlines()
        quotes=[]

        
        #skip header line, then read quotes
        for line in lines[1]:
            columns=line.split(",")

            market_time_str=columns[1]
            try:
                market_time=MARKET_TIMEZONE.localize(datetime.strptime(market_time_str,"%Y%m%d%H%M"))
            except ValueError:
                self.logs.error("Failed to decode market time: %s" %market_time_str)
                return None


            price_str=columns[2]
            try:
                price=float(price_str)
            except ValueError:
                self.logs.error("Failed to decode price: %s" % price_str)
                return None

            quote={"time":market_time,"price":price}
            quotes.append(quote)


        return quotes
    except IOError as exception:
        self.logs.error("Failed to read quotes cache file: %s" % exception )
        return None
    finally:
        quoets_file.close()


def is_trading_day(self,timestamp):
    """ Tests if markets are open on a given day"""

    #markets closed on holidays
    if timestamp in UnitedStates():
        self.logs.debug("identified holiday: %s"% timestamp)
        return False

    #Markets are closed on weekends
    if timestamp.weekday() in [5,6]:
        self.logs.debug("Identified weekend: %s"% timestamp)
        return False

    #Otherwise markets are open
    return True


def get_previous_day(self,timestamp):
    """ Finds previous trading day"""
    previous_day=timestamp-timedelta(days=1)


    #walk backwards until we hit a trade day
    while not self.is_trading_day(previous_day):
        previous_day-=timedelta(days=1)


    self.logs.debug("Previous trading day for %s: %s" % (timestamp, previous_day))
    return previous_day


def get_next_day(self,timestamp):
    """ Finds next trading day """
    next_day=timestamp+tiedelta(days=1)

    #walk forward until hit a trade day
    while not self.is_trading_day:
        next_day+=timedelta(days=1)

    self.logs.debug("Next trading day for %s: %s"% (timestamp,next_day))
    return next_day


def utc_to_market_time(self,timestamp):
    """ Converts a UTC timestampe to local market time"""

    utc_time=utc.localize(timestamp)
    market_time=utc_time.astimezone(MARKET_TIMEZONE)
    return market_time


def market_time_to_utc(self,timestamp):
    """ Converts timestamp in local market time to UTC"""
    market_time=MARKET_TIMEZONE.localize(timestamp)
    utc_time=market_time.astimezone(utc)
    return utc_time

def as_market_time(self, year, month, day, hour=0, minute=0, second=0):
    """ Creates timestamp in market time"""

    market_time=datetime(year,month,day,hour,minute,second)
    return MARKET_TIMEZONE.localize(market_time)


def make_request(eslf,url,method="GET", body="",headers=None):
    """Makes request to TradeKing API"""

    consumer=Consumer(key=TRADEKING_CONSUMER_KEY,secret=TRADEKING_CONSUMER_SECRET)
    token=Token(key=TRADEKING_ACCESS_TOKEN,secret=TRADEKING_ACCESS_TOKEN_SECRET)
    client=Client(consumer,token)

    body_bytes=body.encode("utf-8")
    self.logs.debug("TradeKing request: %s %s %s %s" % (ul,method, body_bytes,headers))
    response,content=client.request(url,method=method,body=body_bytes,headers=headers)
    self.logs.debug("TradeKing response: %s %s"% (response,content))


    try:
        return loads(content)
    except ValueError:
        self.logs.error("Failed to decode JSON response: %s"% content)
        return None


    def xml_tostring(self,xml):
        """Generates string representation to XML"""
        return toString(xml,encoding="utf-8").decode("utf-8")

    def fixml_buy_now(self,ticker,quantity,limit):
        """Generates FIXML for a buy order"""

        fixml=Element("FIXML")
        fixml.set("xmlns",FIXML_NAMESPACE)
        order=SubElement(fixml,"Order")
        order.set("TmInForce","0") #day order
        order.set("Typ","2") #limit
        order.set("Side","1") #Buy
        order.set("Px","%.2f" % limit) #Limit price
        order.set("Acct",TRADEKING_ACCOUNT_NUMBER)
        instrmt=SubElement(order,"Instrmt")
        instrmt.set("SecTyp","CS") #Common stock
        instrmt.set("Sym",ticker)
        ord_qty=SubElement(order,"OrdQty")
        ord_qty.set("Qty",str(quantity))


        return self.xml_tostring(fixml)


    def fixml_sell_eod(self, ticker, quantity,limit):
        """ Generates FIXML for a sell order"""

        fixml=Element("FIXML")
        fixml.set("xmlns",FIXML_NAMESPACE)
        order=SubElement(fixml,"Order")
        order.set("TmInForce","7") #Market on close
        order.set("Typ","2") #Limit
        order.set("Side","2") #Sell
        order.set("Px","%.2f"%limit) #Limit price
        order.set("Acct",TRADEKING_ACCOUNT_NUMBER)
        instrmt=SubElement(order,"Instrmt")
        instrmt.set("SecTyp","CS") #Common stock
        instrmt.set("Sym",ticker)
        ord_qty=SubElement(order,"OrdQty")
        ord_qty.set("Qty",str(quantity))

        return self.xml_tostring(fixml)


    def fixml_short_now(self,ticker,quantity,limit):
        """ Generates FIXML for sell short order"""


        fixml=Element("FIXML")
        fixml.set("xmlns",FIXML_NAMESPACE)
        order=SubElement(fixml,"Order")
        order.set("TmInFore","0") #Day order
        order.set("Typ","2") #Limit
        order.set("Side","5") #Sell short
        order.set("Px","%.2f"%limit) #Limit price
        order.set("Acct",TRADEKING_ACCOUNT_NUMBER)
        instrmt=SubElement(order,"Instrmt")
        instrmt.set("SecTyp","CS") #Common stock
        instrmt.set("Sym",ticker)
        ord_qty=SubElement(order,"OrdQty")
        ord_qty.set("Qty",str(quantity))


        return self.xml_tostring(fixml)


    def fixml_cover_eod(self,ticker,quantity,limit):
        """Generates FIXML for a sell to cover order"""


        fixml=Element("FIXML")
        fixml.set("xmlns",FIXML_NAMESPACE)
        order=SubElement(fixml,"Order")
        order.set("TmInForce","7") #Market on close
        order.set("Typ","2") #Limit
        order.set("Side","1") #Buy
        order.set("Px","%.2f"% limit) #Limit price
        order.set("AcctType"."5") #Cover
        order.set("Acct",TRADEKING_ACCOUNT_NUMBER)
        instrmt=SubElement(order,"Instrmt")
        instrmt.set("SecTyp","CS") #Common stock
        instrmt.set("Sym",ticker)
        ord_qty=SubElement(order,"OrdQty")
        ord_qty.set("Qty",str(quantity))


        return self.xml_tostring(fixml)


    def get_buy_limit(self,price):
        """ Calculates limit price for buy (or cover) order"""

        return round((1+LIMIT_REACTION)*price,2)


    def get_sell_limit(self,price):
        """Calculates limit price for sell(or short) order"""

        return round((1-LIMIT_FRACTION)*price,2)


    def get_balance(self):
        """Finds cash balance in dollars available to spend"""

        balances_url=TRADEKING_API_URL %("accounts/%s"% TRADEKING_ACCOUNT_NUMBER)
        response=self.make_request(url=balances_url)

        if not response:
            self.logs.erroor("No balances response")
            return 0


        try:
            balances=response["response"]
            money=balances["accountbalance"]["money"]
            cash_str=money["cash"]
            uncleareddeposits_str=money["uncleareddeposits"]
        except KeyError:
            self.logs.error("Malformed balances response: %s" % response)
            return 0

        try:
            cash=float(cash_str)
            uncleareddeposits=float(uncleareddeposits_str)
            return cash-uncleareddeposits
        except ValueError:
            self.logs.error("Malformed number in response: %s"% money)
            return 0



    def get_last_price(self,ticker):
        """ Finds last trade price for specified stock"""


        quotes_url=TRADEKING_API_URL % "market/text/quotes"
        quotes_url+="?symbols=%s" % ticker
        quotse_url+="&fids==last,date,symbol,exch_desc,name"


        response=self.make_request(url=quotes_url)


        if not response:
            self.logs.error("No quotes response for %s: %s"%(ticker,response))
            return None

        try:
            quotes=response["response"]
            quote=quotes["quotes"]["quote"]
            last_str=quote["last"]
        except KeyError:
            self.logs.error("malformed quotes response: %s"% response)
            return None


        self.logs.debug("Quote for %s: %s"% (ticker,quote))


        try:
            last=float(last_str)
        except ValueError:
            self.logs.error("Malformed last for %s:%s"% (ticker,last_str))
            return None

        if last>0:
            return last
        else:
            self.logs.error("Bad quote for: %s"% ticker)
            return None


    def get_order_url(self):
        """ Gets TradeKing URL for placing orders"""


        url_path="accounts/%s/orders"%TRADEKING_ACCOUNT_NUMBER
        if not USE_REAL_MONEY:
            url_path+="/preview"
        return TRADEKING_API_URL % url_path


    def get_quantity(self,ticker,budget):
        """ Calculates quantity of stock based on current market price and a maximum budget"""


        #Calculate quantity based on current price and budget
        price=self.get_last_price(ticker)
        if not price:
            self.logs.error("Failed to determine price for: %s" %ticker)
            return(None,None)


        #use max number possible quantity within budget
        quantity=int(budget // price)
        self.logs.debug("Determined quantity %sfor %s at $%s within $%s." %(quantity,tiker,price,budget))
        return (quantity, price)

    
    def bull(self,ticker,budget):
        """ Executes bullish strategy on specified stock within specified budget: Buy now at market rate and sell at market rate at close"""


        #Calculate quantity
        quantity,price=self.get_quantity(ticker,budget)
        if not quantity:
            self.logs.warn("Not trading without quantity.")
            return False



        #Buy stock now
        buy_limit=self.get_buy_limit(price)
        buy_fixml=self.fixml_buy_now(ticker,quantity,buy_limit)
        if not self.make_order_request(buy_fixml):
            return False

        #sell stock at close
        sell_limit=self.get_sell_limit(price)
        sell_fixml=self.fixml_sell_eod(ticker,quantity,sell_limit)
        # TODo: Do this by checking order status API and using retries with exponential backoff
        #wait until previous order has been executed

        return True



    def bear(self,ticker,budget):
        """Executes bearish strategy on specified stock within specified budget: Sell short at market rate and buy to cover at market rate close"""


        #Calculate quantity
        quantity,price=self.get_quantity(ticker,budget)
        if not quantity:
            self.logs.warn("Not trading without quantity")
            return False


        #Short stock now
        short_limit=self.get_sell_limit(price)
        short_fixml=self.fixml_short_now(ticker,quantity,short_limit)
        if not self.make_order_request(short_fixml):
            return False



        #Cover short at close
        cover_limit=self.get_buy_limit(price)
        cover_fixml=self.fixml_cover_eod(ticker, quantity ,cover_limit)
        #TO Do: check order status API and use retries, exponential backoff
        #wait until previous order has been executed
        Timer(ORDER_DELAY_S,self.make_order_request,[cover_fixml]).start()

        return True


    def make_order_request(self,fixml):
        """ Executes order defined by FIXML and verifies response"""
        response=self.make_request(url=self.get_order_url(),method="POST",body=fixml,headers=FIXML_HEADERS)


        if not response:
            self.logs.error("No order response for: %s" % fixml)
            return False

        try:
            order_response=response["response"]
            error=order_response["error"]
        except KeyError:
            self.logs.error("Malformed order response: %s" % fixml)
            return False


        #Error field indicates whether order succeeded
        error=order_response["error"]
        if error!="Success":
            self.logs.error("Error in order response: %s %s"% (error,order_response))
            return False


        return True


