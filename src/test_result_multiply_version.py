#just modify code, never run ever.
import math
import MySQLdb, re, logging
from time import sleep
from preprocessor import preprocess

ML_HOST = "158.108.34.12"
ML_DB = "ml"
ML_USER = "ml"
ML_PASS = "E6v8zh7RajsM6p3G"

LOG_FILENAME="test_result.log"

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

ml = MySQLdb.connect(host=ML_HOST, user=ML_USER, passwd=ML_PASS, db=ML_DB)
ml.set_character_set('utf8')


ml_cursor = ml.cursor()
test_cursor = ml.cursor()

#get P(-) and P(+) from class_prob
ml_cursor.execute(u'''
	SELECT class,prob,count
	FROM class_prob
''')
att_prob=[0,0]
att_count=[0,0]
for i in range(2):
	tmp=ml_cursor.fetchone()
	if tmp[0]==-1:
		att_prob[0]=tmp[1]		#-1
		att_count[0]=tmp[2]
	elif tmp[0]==1:
		att_prob[1]=tmp[1]		#+1
		att_count[1]=tmp[2]
print 'att_prob=',att_prob
print 'att_count=',att_count

#get test_data and true_answer <<<<<<<<<<<<<<<<<<<<<must change name here do not change order
test_cursor.execute(u'''
	SELECT id,text,attitude
	FROM tweets_testdata
''')

r=0
result=[0,0]	      #result[0]=true , result[1]=false
num_of_false=[0,0]    #false in negative case , false in positive case
while(True):
	#print r,
	r+=1
	instance=test_cursor.fetchone()
	if instance==None:
		break
	#print instance #it's ok
	words=preprocess(instance[1]).split('|')		#<<<<<<<<<<<<<<<<<<<<change preprocess function name here

	true_answer=instance[2]

	#init value of - and + at 0
	sum=[att_prob[0],att_prob[1]]
	count_feature=[0,0]
	#unigram
	for word in words:
		ml_cursor.execute(u'''
			SELECT `given`,`prob`
			FROM `features_probability`
			WHERE `first_word`=%s AND `second_word` IS NULL
		''',(word,) )
		for i in range(2):
			tmp=ml_cursor.fetchone()
			if tmp==None:
				break
			if tmp[0]==-1:
				sum[0]*=tmp[1]
				count_feature[0]+=1
			elif tmp[0]==1:
				sum[1]*=tmp[1]
				count_feature[1]+=1
		
		for i in range(2):
			if count_feature[i]<count_feature[(i+1)%2]:
				count_feature[i]+=1
				sum[i]*=1.0/att_count[i]		#add-one smoothing

	#bigram
	for i in range(0,len(words)-1):
		ml_cursor.execute(u'''
			SELECT `given`,`prob`
			FROM `features_probability`
			WHERE `first_word`=%s AND `second_word`=%s
		''',(words[i],words[i+1]) )
		for i in range(2):
			tmp=ml_cursor.fetchone()
			if tmp==None:
				break
			if tmp[0]==-1:
				sum[0]*=tmp[1]
				count_feature[0]+=1
			elif tmp[0]==1:
				sum[1]*=tmp[1]
				count_feature[1]+=1
		
		for i in range(2):
			if count_feature[i]<count_feature[(i+1)%2]:
				count_feature[i]+=1
				sum[i]*=1.0/att_count[i]		#add-one smoothing

	#print sum
	#print 'diff',sum[1] - sum[0]
	test_answer=0
	if sum[0]>sum[1]:
		test_answer=-1
	else:
		test_answer=1
	#print 'test_answer',test_answer,'true_answer',instance[2]
	#is_true is a boolean
	if test_answer==instance[2]:
		result[0]+=1		#ture answer
		is_true=True
		#print 'true'
	else:
		result[1]+=1		#false answer
		is_true=False
		#print 'false'
		if instance[2]==-1:
			num_of_false[0]+=1
		else:
			num_of_false[1]+=1
	
	print 'id:',instance[0],'\tans:',int((sum[1]-sum[0])/abs(sum[1]-sum[0])),'\tresult:',is_true,'\t',instance[1]

	#ml_cursor.execute(u'''
	#	UPDATE `tweets_testdata` SET `result`=%s WHERE `id`=%s
	#''',(str(is_true),str(instance[0]))
	#)

test_cursor.close()

ml_cursor.close()

print 'percentage=',float(result[0]*100)/(result[0]+result[1]),'%'
print 'false in negative case =',num_of_false[0],'cases'
print 'false in positive case =',num_of_false[1],'cases'
'''
except Exception as e:
	print unicode(e)
	print d
	logging.error(unicode(e))
'''               
ml.close()
print "finish"
