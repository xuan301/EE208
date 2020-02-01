import sys
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup


def parseURL(content,url):
    urlset = set()
    soup = BeautifulSoup(content,features="html.parser")
    for i in soup.findAll('a'):
        link = i.get('href','')
        if len(link) <= 1 :
            continue
        match = re.match(r'^javascript.*',link)
        if match:
            continue
        match2 = re.match(r'^https?.*',link)
        if match2:
            urlset.add(match2.group(0))
            continue
        match3 = re.match(r'^/?\w.*',link)
        if match3:
            link = urllib.parse.urljoin(url, match3.group(0))
        match4 = re.match(r'^//w{3}.*',link)
        if match4:
            link = urllib.parse.urljoin('http:', match4.group(0))
        urlset.add(link)
    return urlset


def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')


def main():
    url = 'http://www.baidu.com'
    # url = 'http://www.sjtu.edu.cn'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        content = r.content
        urls = parseURL(content,url)
        write_outputs(urls, 'res1.txt')
    except:
        print("产生异常")



if __name__ == '__main__':
    main()
