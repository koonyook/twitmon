import MySQLdb, re, logging
from time import sleep

threshold=1    #number of repeation of that word must larger than threshole to be in feature

ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

LOG_FILENAME="get_features_probability.log"

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
ml.set_character_set('utf8')

d={}
r=0
#try:
ml_cursor = ml.cursor()

ml_cursor.execute(u'''
	SELECT text,attitude
	FROM tweets_wordseparated
''')
while(True):
	#print r,
	r+=1
	row=ml_cursor.fetchone()
	if row==None:
		break

	words=row[0].split('|')
	attitude=row[1]
	#unigram
	for word in words:
		gram=(word,None)
		if d.has_key(gram):
			if attitude==-1:
				d[gram][0]+=1
			elif attitude==1:
				d[gram][1]+=1
		else:
			if attitude==-1:
				d[gram]=[1,0]
			elif attitude==1:
				d[gram]=[0,1]
	#bigram
	for i in range(0,len(words)-1):
		gram=(words[i],words[i+1])
		if d.has_key(gram):
			if attitude==-1:
				d[gram][0]+=1
			elif attitude==1:
				d[gram][1]+=1
		else:
			if attitude==-1:
				d[gram]=[1,0]
			elif attitude==1:
				d[gram]=[0,1]

print 'lend=', len(d)	

ml_cursor.execute(u'''
	SELECT count
	FROM class_prob
''')
att_count=[0,0]
att_count[0]=ml_cursor.fetchone()[0]		#-1
att_count[1]=ml_cursor.fetchone()[0]		#+1
print att_count

ml_cursor.execute(u'''
	DELETE
	FROM features_probability
''')	
#print d.keys()[1:5]


r=0
for key in d.keys():
	#print r,
	r+=1
	#print key
	if key[1]!=None and len(key[0])*len(key[1])>0:	#bigram
		if d[key][0]>threshold:
			ml_cursor.execute(u'''
				INSERT INTO `features_probability` (`given`, `first_word`, `second_word`, `prob`) VALUES (-1, %s, %s, %s);
			''', (
			key[0],key[1],float(d[key][0])/att_count[0]
			) )
		if d[key][1]>threshold:
			ml_cursor.execute(u'''
				INSERT INTO `features_probability` (`given`, `first_word`, `second_word`, `prob`) VALUES ( 1, %s, %s, %s);
			''', (
			key[0],key[1],float(d[key][1])/att_count[1]
			) )
	elif key[1]==None and len(key[0])>0:	#unigram
		if d[key][0]>threshold:
			ml_cursor.execute(u'''
				INSERT INTO `features_probability` (`given`, `first_word`, `prob`) VALUES (-1, %s, %s);
			''', (
			key[0],float(d[key][0])/att_count[0]
			) )
		if d[key][0]>threshold:
			ml_cursor.execute(u'''
				INSERT INTO `features_probability` (`given`, `first_word`, `prob`) VALUES ( 1, %s, %s);
			''', (
			key[0],float(d[key][1])/att_count[1]
			) )
	if r%1000==0:
		print r


#	ml_cursor.execute(u'''
#		INSERT INTO `class_prob` (`class`, `prob`) VALUES (%s, %s);
#	''', ( str(row[1][0]), str(row[1][1]/(row[0][1]+row[1][1])) ) )	
	
#	ml_cursor.execute(u'''
#		UPDATE `class_prob` SET `prob`=%s, `count`=%s  WHERE `class`=%s
#	''', (str(float(row[0][1])/(row[0][1]+row[1][1])), str(row[0][1]), str(row[0][0])  ) )
#	ml_cursor.execute(u'''
#		UPDATE `class_prob` SET `prob`=%s, `count`=%s WHERE `class`=%s
#	''', (str(float(row[1][1])/(row[0][1]+row[1][1])), str(row[1][1]), str(row[1][0])  ) )

ml_cursor.close()
'''
except Exception as e:
	print unicode(e)
	print d
	logging.error(unicode(e))
'''               
ml.close()
print "finish"
