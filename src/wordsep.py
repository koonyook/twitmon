import MySQLdb, re, logging
from time import sleep
from subprocess import Popen, PIPE

ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

WINDOW_SIZE = 1000
PROCESS_FROM = 0
DELAY = 1
LOG_FILENAME = 'wordsep.log'

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
ml.set_character_set('utf8')

while(True):
    sleep(DELAY)
    
    try:
        ml_cursor = ml.cursor()
        # ml_cursor.execute('SELECT `id`, `text` FROM `tweets` LIMIT %s, %s' % (offset, WINDOW_SIZE))
        ml_cursor.execute(u'SELECT `id`, `text`, `attitude`, `processed` FROM `tweets_preprocessed2` WHERE `processed` = %s ORDER BY `id` ASC LIMIT %s', (PROCESS_FROM, WINDOW_SIZE))
        
        tweets = list()
        while (True):
            # tweet[0] == id, tweet[1] == text, tweet[2] == attitude
            tweet = ml_cursor.fetchone()
            if tweet == None:
                break
                
            # DO WORDSEPARATING HERE
            # tweet_sepped[0] = id, tweet_sepped[1] == sepped text, tweet_sepped[2] == attitude
            tweet_sepped = [tweet[0], tweet[1], tweet[2]]
    
            try:        
                text = tweet[1]
                text = text.decode('utf8')
                text = text.encode('cp874')
                        
                process = Popen('swath.exe', stdin=PIPE, stdout=PIPE, stderr=PIPE)
                text = process.communicate(text)[0]
                
                text = text.replace('(|:|username|)', '(:username)')
                text = text.replace('(|:|url|)', '(:url)')
                text = text.replace('(|:|hashtag|)', '(:hashtag)')
                text = re.subn('\| +\|', '|', text)[0]
                text = re.subn('\|\|', '|', text)[0]
                
                text = text.strip()
                
                text = text.decode('cp874')
                
                if text[0] == "|":
                    text = text[1:]
                if text[-1] == "|":
                    text = text[:-1]
                            
                tweet_sepped [1] = text
                tweets.append(tweet_sepped)
            except Exception:
                # Skip text that can't be convert to cp874
                continue
                     
        ml_cursor.close()
        
        for tweet in tweets:
            ml_cursor = ml.cursor()
            ml_cursor.execute(u"UPDATE `tweets_preprocessed2` SET `processed`=1 WHERE `id`=%s;", tweet[0])
            ml_cursor.close()
        
            ml_cursor = ml.cursor()
            ml_cursor.execute(u"INSERT INTO `tweets_wordseparated` (`id`, `text`, `attitude`) VALUES (%s, %s, %s);", (tweet[0], tweet[1], tweet[2]))
            ml_cursor.close()
            
    except Exception as e:
        logging.error(unicode(e))
                                
ml.close()
        
