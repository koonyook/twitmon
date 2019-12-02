import MySQLdb, re, logging
from time import sleep

ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

LOG_FILENAME="class_prob.log"

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
ml.set_character_set('utf8')


try:
	ml_cursor = ml.cursor()
	ml_cursor.execute(u'''
		SELECT attitude,Count(*) as count
		FROM tweets_wordseparated
		GROUP BY attitude
	''')
	row=[]
	for i in range(2):
		row.append( ml_cursor.fetchone() )
	
#	ml_cursor.execute(u'''
#		INSERT INTO `class_prob` (`class`, `prob`) VALUES (%s, %s);
#	''', ( str(row[0][0]), str(row[0][1]/(row[0][1]+row[1][1])) ) )
#	ml_cursor.execute(u'''
#		INSERT INTO `class_prob` (`class`, `prob`) VALUES (%s, %s);
#	''', ( str(row[1][0]), str(row[1][1]/(row[0][1]+row[1][1])) ) )	
	
	ml_cursor.execute(u'''
		UPDATE `class_prob` SET `prob`=%s, `count`=%s  WHERE `class`=%s
	''', (str(float(row[0][1])/(row[0][1]+row[1][1])), str(row[0][1]), str(row[0][0])  ) )
	ml_cursor.execute(u'''
		UPDATE `class_prob` SET `prob`=%s, `count`=%s WHERE `class`=%s
	''', (str(float(row[1][1])/(row[0][1]+row[1][1])), str(row[1][1]), str(row[1][0])  ) )

	ml_cursor.close()

except Exception as e:
	logging.error(unicode(e))
                
ml.close()
print "finish"
