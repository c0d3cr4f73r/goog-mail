#!/usr/bin/python3

import re
import sys
import urllib.request
from sys import stdout

def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

if len(sys.argv) != 2:
    print("\nExtracts emails from Google results.\n")
    print("\nUsage: ./goog-mail.py <domain>\n")
    sys.exit(1)

domain_name = sys.argv[1]
d = {}
page_counter = 0

try:
    while page_counter < 50:
        results = 'http://groups.google.com/groups?q='+str(domain_name)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
        request = urllib.request.Request(results)
        request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        opener = urllib.request.build_opener()
        text = opener.open(request).read().decode('utf-8')
        emails = (re.findall('([\w\.\-]+@'+domain_name+')',StripTags(text)))
        for email in emails:
            d[email]=1
            uniq_emails=d.keys()
        page_counter += 10
except IOError:
    print("Cannot connect to Google Groups."+"")
    
page_counter_web=0

try:
    while page_counter_web < 50:
        results_web = 'http://www.google.com/search?q=%40'+str(domain_name)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter_web) + '&sa=N'
        request_web = urllib.request.Request(results_web)
        request_web.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
        opener_web = urllib.request.build_opener()
        text = opener_web.open(request_web).read().decode('utf-8')
        emails_web = (re.findall('([\w\.\-]+@'+domain_name+')',StripTags(text)))
        for email_web in emails_web:
            d[email_web]=1
            uniq_emails_web=d.keys()
        page_counter_web += 10
except IOError:
    print("Cannot connect to Google Web."+"") 

stdout.write('''    
  ________                                  _____         .__.__                     
 /  _____/  ____   ____   ____             /     \ _____  |__|  |      ______ ___.__.
/   \  ___ /  _ \ /  _ \ / ___\   ______  /  \ /  \\__   \ |  |  |      \____ <   |  |
\    \_\  (  <_> |  <_> ) /_/  > /_____/ /    Y    \/ __ \|  |  |__    |  |_> >___  |
 \______  /\____/ \____/\___  /          \____|__  (____  /__|____/ /\ |   __// ____|
        \/             /_____/                   \/     \/          \/ |__|   \/     


Emails associated with the domain will appear below: 
''')

for uniq_emails_web in d.keys():
    print(uniq_emails_web+"")
 
