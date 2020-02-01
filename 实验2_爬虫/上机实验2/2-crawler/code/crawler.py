#!usr/bin/python2
# -*- coding:utf-8 -*-
import sys
from bs4 import BeautifulSoup
import urllib2
import urllib

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
        print "ERROR!"
        return ''

def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for i in soup.findAll('a'):
        link = i.get('href', '')
        if len(link) <= 1:
            continue
        match = re.match(r'^javascript.*', link)
        if match:
            continue
        match2 = re.match(r'^https?.*', link)
        if match2:
            links.append(match2.group(0))
            continue
        match3 = re.match(r'^/?\w.*', link)
        if match3:
            link = urllib.parse.urljoin(page, match3.group(0))
        match4 = re.match(r'^//w{3}.*', link)
        if match4:
            link = urllib.parse.urljoin('http:', match4.group(0))
        links.append(link)
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
    
    while tocrawl and count < max_page:
        page = tocrawl.pop()
        if page not in crawled:
            count += 1
            print page
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)
            graph[page] = outlinks
    return graph, crawled

if __name__ == '__main__':

    seed = sys.argv[1]
    method = sys.argv[2]
    max_page = sys.argv[3]
    
    graph, crawled = crawl(seed, method, max_page)
