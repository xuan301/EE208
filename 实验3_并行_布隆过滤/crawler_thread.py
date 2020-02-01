#!usr/bin/python2
# -*- coding:utf-8 -*-
import sys
from bs4 import BeautifulSoup
import urllib2
import re
import threading
import Queue
import time

count = 0
max_page = 100

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    try:
        req = urllib2.urlopen(page, timeout=30)
        content = req.read()
        return content
    except:
        return ''


def get_all_links(content, page):
    import urlparse
    links = []
    soup = BeautifulSoup(content, features="html.parser", from_encoding="gbk")
    for i in soup.findAll('a'):
        temp = urlparse.urljoin(page, i.get('href'))
        if re.compile('^http.*html$').match(temp):
            links.append(temp)
    return links



def add_page_to_folder(page, content):
    import os
    index_filename = 'index.txt'
    folder = 'html'
    filename = valid_filename(page)
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)
    f.close()


def working():
    global count,max_page,crawled,q
    while count<max_page and q.qsize > 0:
        page = q.get()
        if page not in crawled:
            try:
                content = get_page(page)
                add_page_to_folder(page, content)
                crawled.append(page)
                outlinks = get_all_links(content, page)
                for link in outlinks:
                    q.put(link)
                print page
                if varLock.acquire():
                    count += 1
                    varLock.release()
                q.task_done()
            except:
                continue

    while q.unfinished_tasks:
        if varLock.acquire():
            q.task_done()
            varLock.release()


start = time.clock()
NUM = 8
crawled = []
varLock = threading.Lock()
q = Queue.Queue()

for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    t.start()
q.put('http://news.sjtu.edu.cn')
q.join()
end = time.clock()
print end-start
print count

