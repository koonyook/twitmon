import MySQLdb
import tweepy
import logging
from time import sleep
from cgi import parse_qs

HOST = "158.108.34.12"
DB = "ml"
USER = "ml"
PASS = "E6v8zh7RajsM6p3G"
CHARSET = "utf8"
QUERY = ":) OR :("
LANG = "th"
RPP = 100
DELAY = 10 # Seconds
LOG_FILENAME = 'ml_daemon.log'

# html_unescape snippet taken from
# http://blog.client9.com/2008/10/html-unescape-in-python.html
from htmlentitydefs import name2codepoint 
import re
def replace_entities(match):
    try:
        ent = match.group(1)
        if ent[0] == "#":
            if ent[1] == 'x' or ent[1] == 'X':
                return unichr(int(ent[2:], 16))
            else:
                return unichr(int(ent[1:], 10))
        return unichr(name2codepoint[ent])
    except:
        return match.group()

entity_re = re.compile(r'&(#?[A-Za-z0-9]+?);')
def html_unescape(data):
    return entity_re.sub(replace_entities, data)
# END html_unescape snippet

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

connection = MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=DB)
connection.set_character_set(CHARSET)

since_id = 0
while(True):
    sleep(DELAY)
    
    try:
        results = tweepy.api.search(QUERY, lang=LANG, rpp=RPP, since_id=since_id)
        
        tweets = list()
        for r in results:
            # Filter out retweets
            if r.text[:2].lower() == "rt":
                continue
            tweets.append(r.text)
        
        tweets = [html_unescape(t) for t in tweets]    
        query = u"INSERT INTO `tweets` (`text`) VALUES " + (u"(%s),"*len(tweets))[:-1] + u";"
        
        cursor = connection.cursor()
        cursor.execute(query, tweets)
        cursor.close()
    
        since_id = parse_qs(results.refresh_url[1:])['since_id'][0]
                
    except Exception as e:
        logging.error(unicode(e))

connection.close()
                                                                      