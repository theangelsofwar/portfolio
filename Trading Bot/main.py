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


