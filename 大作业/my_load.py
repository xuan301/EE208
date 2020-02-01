#!/usr/bin/python
import pickle
import sys
def load(filename):
    f=open('data/'+filename,'rb')
    return pickle.load(f)
    f.close()
if __name__=='__main__':
    data=load(sys.argv[1])
    print 'url:'+data['url']
    print 'title:'+data['title']
    print 'time:'+data['time']
    print 'ctime:'+str(data['ctime'])
    print 'content:'+data['content']
    print 'imgs:'
    for i in data['realimgs']:
        print i
