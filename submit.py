
# -*- coding: utf-8 -*-

import urllib
import urllib2
import hashlib
import re

session_id = ''
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             'Chrome/49.0.2623.87 Safari/537.36',
page_url = 'http://syzoj.com/problem/1'
submit_url = 'http://syzoj.com/submit/1'


def login():
    login_url = 'http://syzoj.com/api/login'
    tmp = hashlib.md5()
    tmp.update('xuetianyang' + 'syzoj2_xxx')
    password = tmp.hexdigest()
    data = {'username': 'xtt_tmp', 'password': password}
    data = urllib.urlencode(data)

    opener = urllib2.build_opener()
    opener.addheader = [('User-Agent', user_agent)]

    try:
        response = opener.open(login_url, data)
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return
    else:
        print 'Access succeed'

    tmp = response.read()
    pattern = re.compile(r'\d+')
    num = re.findall(pattern, tmp)

    global session_id
    if num[0] != '1':
        print 'Login false'
        return False
    else:
        print 'Login succeed'
        session_id = num[1]
        return True


def submit(local_add):
    opener = urllib2.build_opener()
    opener.addheaders = [('User_Agent', user_agent), ]
    opener.addheaders = [('Cookie', 'session_id=' + session_id)]
    #这里需要用headers而不是header
    files = open(local_add, 'r')
    code = files.read()
    data = {"code": code}
    data = urllib.urlencode(data)

    try:
        opener.open(submit_url, data)
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return False
    else:
        print 'Submit succeed'


if __name__ == '__main__':
    if login():
        submit('aplusb.cpp')
