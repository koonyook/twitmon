import MySQLdb, re

ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

WINDOW_SIZE = 1000
PROCESS_FROM = 0
# MAX = 674160

username_matcher = re.compile("@\w+", re.UNICODE)
hashtag_matcher = re.compile("#\w+", re.UNICODE)

ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
ml.set_character_set('utf8')

offset = 0

ml_cursor = ml.cursor()
# ml_cursor.execute('SELECT `id`, `text` FROM `tweets` LIMIT %s, %s' % (offset, WINDOW_SIZE))
ml_cursor.execute(u'SELECT `id`, `text`, `processed` FROM `tweets` WHERE `processed` = %s ORDER BY `id` DESC LIMIT %s', (PROCESS_FROM, WINDOW_SIZE))

tweets = list()
while (True):
    # tweet[0] == id, tweet[1] == text
    tweet = ml_cursor.fetchone()
    if tweet == None:
        break
        
    # DO PREPROCESS HERE
    tweet_processed = [tweet[0], tweet[1]]
    tweet_processed[1] = username_matcher.subn("(:username)", tweet_processed[1])[0]
    tweet_processed[1] = hashtag_matcher.subn("(:hashtag)", tweet_processed[1])[0]
        
    tweets.append(tweet_processed)
            
ml_cursor.close()

for tweet in tweets:
    ml_cursor = ml.cursor()
    ml_cursor.execute(u"UPDATE `tweets` SET `processed`=1 WHERE `id`=%s;", tweet[0])
    ml_cursor.close()

    ml_cursor = ml.cursor()
    ml_cursor.execute(u"INSERT INTO `tweets_preprocessed` (`id`, `text`) VALUES (%s, %s);", (tweet[0], tweet[1]))
    ml_cursor.close()

ml.close()
        
