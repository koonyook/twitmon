# -*- coding: utf8 -*-
import re
from subprocess import Popen, PIPE

username_matcher = re.compile("@\w+", re.UNICODE)
hashtag_matcher = re.compile("#\w+", re.UNICODE)
url_matcher = re.compile("https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?", re.UNICODE)

positive_emoticons = ['=)', ':)', ': )', ':-)', '(;', '( ;', '(-;', ':D', ';D', '^_^', '^^', '<3']
negative_emoticons = [':(', ': (', ':-(', 'TT', 'T_T', '- -"', "- -'"]
neutral_emoticons = [':p', ':P', '>^<', '>_<', '>__<',  '>3<', '-3-', ':3', '= =', '-_-', '- -a']

icons_1 = ['=)', ':)', ': )', ':-)', '(;', '( ;', '(-;', ':D', ';D', '^_^', '^^', '<3',
':(', ': (', ':-(', 'TT', 'T_T', '- -"', "- -'",
':p', ':P', '>^<', '>_<', '>__<',  '>3<', '-3-', ':3', '= =', '-_-', '- -a',
'~', '"', "'", '!', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|',
':', '<', '>', '?', ',', '.', '/', ';', '[', ']', '\\', '=', '-',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '“', '”', '\r', '\n']

icons_2 = ['#', '@']
    
def preprocess(text):
    """docstring for preprocess"""
    text = text.decode('utf8')
    
    text = url_matcher.subn("(:url)", text)[0]
    
    for icon in icons_1:
        text = re.subn(re.escape(icon), "", text)[0]
        
    text = re.subn(r'((.)\2\2+)', r'\2', text)[0]
    
    text = username_matcher.subn("(:username)", text)[0]
    text = hashtag_matcher.subn("(:hashtag)", text)[0]
    
    for icon in icons_2:
        text = re.subn(re.escape(icon), "", text)[0]
    
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
        
    return text
