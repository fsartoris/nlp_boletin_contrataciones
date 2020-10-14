import os
import datetime
import tweepy as tw

consumer_key= os.environ.get('TW_CONSUMER_KEY', None)
consumer_secret= os.environ.get('TW_CONSUMER_SECRET', None)
access_token= os.environ.get('TW_ACCESS_TOKEN', None)
access_token_secret= os.environ.get('TW_ACCESS_SECRET', None)

def compose_tweet(razon, money, url):    
    tweet = "Empresa: %s\nImporte: %s\nFuente: %s\nHora: %s" % \
            (razon.upper(), money, url, datetime.datetime.now().strftime("%X"))

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    api.update_status(tweet)