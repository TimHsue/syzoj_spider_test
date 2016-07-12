
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import hashlib

session_id = ''
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             'Chrome/49.0.2623.87 Safari/537.36',
page_url = 'http://syzoj.com/problem/1'
problem_url = 'http://syzoj.com/problem/'


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

    # 由于特殊设定...需要手动载入cookie
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


class Data(object):
    ref = {
        'tittle':   re.compile(ur'<div\s+class="am-u-sm-12\s+problem-header">\s+<h1>(.*?)</h1>'),
        'memory':   re.compile(ur'<span\s+class="am-badge\s+am-badge-success\s+am-text-sm">.+?(\d+).+?</span>'),
        'time':     re.compile(ur' <span\s+class="am-badge\s+am-badge-warning\s+am-text-sm">.+?(\d+).+?</span>'),
        'describe': re.compile(ur'<div\s+class="am-panel-bd"\s+id="description">(.*?)</div>', re.S),
        'input':    re.compile(ur'<div class="am-panel-bd" id="input">(.*?)</div>', re.S),
        'output':   re.compile(ur'<div class="am-panel-bd" id="output">(.*?)</div>', re.S),
        'example':  re.compile(ur'<div class="am-panel-bd" id="example">(.*?)</div>', re.S),
        'hint':     re.compile(ur'<div class="am-panel-bd" id="hint">(.*?)</div>', re.S)
    }


def download_pages(dl_url):
    opener = urllib2.build_opener()
    opener.addheader = [('User_Agent', user_agent)]
    opener.addheader = [('Cookie', 'session_id' + session_id)]

    try:
        response = opener.open(dl_url)
    except urllib2.HTTPError, e:
        print e.code
        print e.reason
        return False
    else:
        print 'Download succeed'
        return response.read()


def test():
    files = open('page.txt')
    try:
        page = files.read()
    finally:
        files.close()
    pattern = re.compile(ur'<div class="am-panel-bd" id="hint">(.*?)</div>', re.S)
    items = re.findall(pattern, page)

    for item in items:
        print item


def get_data(dl_url, num):
    page = download_pages(dl_url)
    if not page:
        return False

    out = {}
    for item in Data.ref:
        pattern = Data.ref[item]
        tmp = re.findall(pattern, page)
        if not tmp:
            out[item] = 'none'
        else:
            out[item] = tmp[0]

    files = open('save/problem' + str(num) + '.txt', 'w')
    files.write('问题编号:%d\n\n\n' % num)
    files.write('问题标题:%s\n\n\n' % out['tittle'])
    files.write('问题描述:\n%s\n\n\n' % out['describe'])
    files.write('输入格式:\n%s\n\n\n' % out['input'])
    files.write('输出格式:\n%s\n\n\n' % out['output'])
    files.write('测试样例:\n%s\n\n\n' % out['example'])
    files.write('数据范围与提示\n%s\n\n\n' % out['hint'])
    files.close()

    return True


if __name__ == '__main__':
    '''
    test()
    '''
    if login():
        i = 1
        while True:
            # 我也不知道为啥少一道题。。而且是没有这道题而不是未审核。。
            if i == 36:
                i += 1
                continue
            if not get_data(problem_url + str(i), i):
                print 'Access denied'
                break
            else:
                print 'problem ' + str(i) + ' done'
                i += 1
