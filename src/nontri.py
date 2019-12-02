#!/usr/bin/env python

import httplib, urllib
import random,time
#httplib.HTTPSConnection.debuglevel = 1

uname, upasswd = 'b5105xxx', 'xxxxxxxx'

computer = 'login'+`random.randint(1, 10)`+'.ku.ac.th'
reqURL = '/index.php'
referer = 'www.ku.ac.th'

reqHeaders = {
	'Host' : computer,
	'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3',
	'Content-Type' : 'application/x-www-form-urlencoded',
	'Accept' : '*/*',
}

try:
	conn = httplib.HTTPSConnection(computer)
	conn.request('GET', reqURL)
	resp = conn.getresponse()
	conn.close()
except Exception, e:
	raise e
	exit(1)

data = resp.read()
print resp
print '------------------------------------------------------------'
print data
hiddens = []
import re
reg_field = re.compile("<input name='([^']*)' type='hidden' value='([^']*)'>")
fields = reg_field.findall(data)
if len(fields) == 0:
	print 'cannot find any login info'
	exit(1)
print '------------------------------------------------------------'
print fields

reqHeaders['Referer'] = 'http://' + computer + reqURL
cookie = resp.getheader('Set-Cookie')
print '------------------------------------------------------------'
print cookie
cookie = cookie.split()
reqHeaders['Cookie'] = cookie[0]
params = urllib.urlencode({'content': 'login', 'referer': referer, 'action': 'login',})

post = {'username' : uname, 'password' : upasswd, 'submit' : 'Login', 'zone': '0'}
for name, val in fields:
	post[name] = val
	
try:
	conn = httplib.HTTPSConnection(computer)
	conn.request('POST', reqURL + "?" + params, urllib.urlencode(post), reqHeaders)

	# notify the user
	try:
		print 'logged on'
	except:
		pass
except Exception, e:
	raise e
	exit(1)
