#!usr/bin/python2
# -*- coding:utf-8 -*-
import sys
from bs4 import BeautifulSoup
import urllib2
import re

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

def get_page(page):
    try:
        req = urllib2.urlopen(page,timeout=30)
        content = req.read()
        return content
    except:
        return ''

def get_all_links(content, page):
    import urlparse
    links = []
    soup = BeautifulSoup(content, features="html.parser",from_encoding="gbk")
    for i in soup.findAll('a'):
        temp = urlparse.urljoin(page,i.get('href'))
        if re.compile('^http').match(temp):
            links.append(temp)
    return links
        
def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)
            
def union_bfs(a,b):
    for e in b:
        if e not in a:
            a.insert(0,e)
       
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
    
def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0
    
    while tocrawl:
        page = tocrawl.pop()
        if count >= int(max_page):
            return graph, crawled
        if page not in crawled:
            count += 1
            print page
            content = get_page(page)
            add_page_to_folder(page,content)
            outlinks = get_all_links(content, page)
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)
            graph[page] = outlinks


if __name__ == '__main__':

    seed = sys.argv[1]
    method = sys.argv[2]
    max_page = sys.argv[3]
    
    graph, crawled = crawl(seed, method, max_page)
