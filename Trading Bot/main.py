from datetime import datetime
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from threading import Event
from threading import Thread
from time import sleep


from analysis import analysis
from logs import logs
from trading import trading
from twitter import twitter

#send logs to cloud instead of local file
LOGS_TO_CLOUD=True


# duration of smallest backoff step in seconds
BACKOFF_STEP_S=.1


#max number of retry steps, .1*(2^12-1)=409.5
# #seconds of total delay, largest interval a backoff sequence may take
MAX_TRIES=12


#time in seconds after which to reset backoff sequence, 
#smallest interval at which backoff sequences may repeat normally
BACKOFF_RESET_S=30*60


#host for monitor web server
MONITOR_HOST="0.0.0.0"

#PORT FOR THE MONITOR WEB SERVER
MONITOR_POST=80

#MESSAGE RETURNED BY MONITOR WEB SERVER
MONITOR_MESSAGE="OK"


class Monitor:
    """Monitor exposes web server while main loop runs

    """

    def __init__(self):
        self.server=HTTPServer((MONITOR_HOST,MONITOR_PORT),self.MonitorHandler)
        self.thread=Thread(target=self.server.serve_forever)
        self.thread.daemon=True


    def start(self):
        """Starts web server background thread
        """
        self.thread.start()


    def stop(self):
        """
        Stops web server background thread
        """
        self.server.shutdown()
        self.server.server_close()


    def MonitorHandler(BaseHTTPRequestHandler):
        """
        Http request handler with respond with "OK" whilst running
        """


        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type","text/plain")
            self.end_headers()


        def do_GET(self):
            self._set_headers()
            self.wfile.write(MONITOR_MESSAGE.encode("utf-8"))


        def do_HEAD(self):
            self._set_headers()


Class Main:
    """ Wrapper for main application logic and retry loop
    """


    def __init__(self):
        self.logs=Logs(name="main", to_cloud=LOGS_TO_CLOUD)
        self.twitter=Twitter(logs_to_cloud=LOGS_TO_CLOUD)


    def twitter_callback(self,tweet):
        """
        Analyzes Trump tweets, trades stocks, and tweets about it
        """

        #initialize analysis, logs, trading and twitter instances inside callback
        #to create separate httplib2 instances per thread
        analysis=Analysis(logs_to_cloud=LOGS_TO_CLOUD)
        logs=Logs(name="main-callback",to_cloud=LOGS_TO_CLOUD)


        #ANALYZE TWEET
        companies=analysis.find_companies(tweet)
        logs.info("Using companies: %s" % companies)
        if not companies:
            return


        #trade stocks
        trading=Trading(logs_to_cloud=LOGS_TO_CLOUD)
        trading.make_trades(companies)


        #tweet about it 
        twitter=Twitter(logs_to_cloud=LOGS_TO_CLOUD)
        twitter.tweet(companies,tweet)


    def run_session(self):
        """
        Runs single streaming session. Logs and cleans up after exceptions
        """

        self.logs.info("Starting new session")
        try:
            self.twitter.start_streaming(self.twitter_callback)
        except:
            self.logs.catch()
        finally:
            self.twitter.stop_streaming()
            self.logs.info("Ending session")



    def backoff(self,tries):
        """ Sleeps exponential number of seconds based on number of tries
        """

        delay=BACKOGG_STEP_S*pow(2,tries)
        self.logs.warn("Waiting for %.1f seconds."% delay)
        sleep(delay)


    def run(self):
        """
        Runs main retry loop with exponential backoff
        """
        

        tries=0
        while True:

            #session blocks until error happens
            self.run_session()


            #remember first time backoff sequence starts
            now=datetime.now()
            if tries==0:
                self.logs.debug("Starting first backoff sequence")
                backoff_start=now

            #resetbackoff sequence if last error was long ago
            if(now-backoff_start).total_seconds()>BACKOFF_RESET_S:
                self.logs.debug("Starting new backoff sequence")
                tries=0
                backoff_start=now

            #give up after max number of tries
            if tries>=MAX_TRIES:
                self.logs.warn("Exceeded max retry count")
                break

            #wait according to progression of backoff sequence
            self.backoff(tries)

            #increment number of tries for next error
            tries+=1


if __name__=="__main__":
    monitor=Monitor()
    monitor.start()
    try:
        Main().run()
    finally:
        monitor.stop()