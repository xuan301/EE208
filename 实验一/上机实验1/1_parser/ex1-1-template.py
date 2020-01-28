import sys
import requests
from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    soup = BeautifulSoup(content,features="html.parser")
    for i in soup.findAll('a'):
        url = i.get('href','')
        urlset.add(url)
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
    content=requests.get(url).content
    urls = parseURL(content)
    write_outputs(urls, 'res1.txt')


if __name__ == '__main__':
    main()
