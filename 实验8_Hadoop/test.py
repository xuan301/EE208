import sys
import requests
import re
from bs4 import BeautifulSoup
import urllib.parse

def parseIMG(content):
    urlset = []
    soup = BeautifulSoup(content,features="html.parser")
    for i in soup.findAll('a',{'href':re.compile('^/story')}):
        dic = dict()
        pic = i.contents[0]
        picurl = pic.get('src','')
        dic['picurl'] = picurl
        dic['content'] = i.string
        link = i.findAll('href')
        url = urllib.parse.urljoin('http://daily.zhihu.com/',link)
        dic['url'] = url
        urlset.append(dic)
    return urlset

def main():
    url = 'http://daily.zhihu.com/'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    kv = {'user-agent': 'Mozilla/5.0'}
    r = requests.get(url, timeout=30, headers=kv)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    content = r.content
    urls = parseIMG(content)




if __name__ == '__main__':
    main()