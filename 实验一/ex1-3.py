import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def parseIMG(content):
    urlset = []
    soup = BeautifulSoup(content,features="html.parser")
    for i in soup.findAll('a',{'href':re.compile('^/story')}):
        dic = dict()
        pic = i.contents[0]
        picurl = pic.get('src', '')
        dic['picurl'] = picurl
        dic['content'] = i.contents[1].string
        link = i.get('href','')
        url = urllib.parse.urljoin('http://daily.zhihu.com/', link)
        dic['url'] = url
        urlset.append(dic)
    return urlset


def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url['picurl'])
            f.write('\n')
            f.write(url['content'])
            f.write('\n')
            f.write(url['url'])
            f.write('\n')


def main():
    url = 'http://daily.zhihu.com'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        content = r.content
        urls = parseIMG(content)
        write_outputs(urls, 'res3.txt')
    except:
        print("产生异常")



if __name__ == '__main__':
    main()