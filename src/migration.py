import MySQLdb

TWITMON_HOST = "203.150.230.19"
TWITMON_DB = "thothmedia_twmon"
TWITMON_USER = "knightbaron"
TWITMON_PASS = "XXX"
ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

WINDOW_SIZE = 100
MAX = 674160
# MAX = 100

# E = lambda x: x.encode('utf-8')

twitmon = MySQLdb.connect(host=TWITMON_HOST, user=TWITMON_USER, passwd=TWITMON_PASS, db=TWITMON_DB)
twitmon.set_character_set('utf8')
ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
ml.set_character_set('utf8')

offset = 0

while offset <= MAX:
    twitmon_cursor = twitmon.cursor()
    twitmon_cursor.execute('SELECT `text` FROM `tweets` WHERE LOWER(iso_language_code)="th" AND LOWER(LEFT(text, 2)) != "rt" LIMIT %s, %s' % (offset, WINDOW_SIZE))
    
    tweets = list()
    while (True):
        row = twitmon_cursor.fetchone()
        if row == None:
            break
        tweets.append(row[0])
        
    ml_cursor = ml.cursor()
    ml_cursor.execute("INSERT INTO `tweets` (`text`) VALUES %s;" % ",".join(["('%s')" % twitmon.escape_string(a) for a in tweets]))
    ml_cursor.close()
        
    twitmon_cursor.close()
    offset += WINDOW_SIZE

twitmon.close()
ml.close()


