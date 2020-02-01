#!usr/bin/python2
# -*- coding:utf-8 -*-
import sys
def bbs_set(id, pw, text):
    import urllib2, cookielib, urllib
    from bs4 import BeautifulSoup
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(open())
    postdata = urllib.urlencode({
        'id':id,
        'pw':pw,
        'submit':'login'
    })
    req = urllib2.Request(url = 'https://bbs.sjtu.edu.cn/bbslogin',data = postdata)
    response = urllib2.urlopen(req)
    postdata2 = urllib.urlencode({'text':text})
    req2 = urllib2.Request(url = 'https://bbs.sjtu.edu.cn/bbsplan',data = postdata2)
    response = urllib2.urlopen(req2)
    content = urllib2.urlopen('https://bbs.sjtu.edu.cn/bbsplan').read()
    soup = BeautifulSoup(content)
    print str(soup.find('textarea').string).strip().decode('utf8')

if __name__ == '__main__':
	
    id = sys.argv[1]
    pw = sys.argv[2]
    text = sys.argv[3].decode('utf-8').encode('gbk')

    bbs_set(id, pw, text)
