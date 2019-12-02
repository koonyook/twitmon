# -*- coding: utf-8 -*-
import MySQLdb, re, logging
from time import sleep
from subprocess import Popen, PIPE
from preprocessor import preprocess

ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

WINDOW_SIZE = 1000
PROCESS_FROM = 0
DELAY = 1
LOG_FILENAME = 'wordsep.log'

# ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
# ml.set_character_set('utf8')

# ml_cursor = ml.cursor()
# 
# ml_cursor.execute("INSERT INTO `features_probability` (`given`, `first_word`, `second_word`, `prob`) VALUES (1, 'foobar', 'barfoo', '3.14');")
# 
# ml_cursor.close()

print preprocess("สวัสดีครับ สบายดีหรือ")
