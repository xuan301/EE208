#!/usr/bin/python
import pickle
import sys
def load(filename):
    f=open('data/'+filename,'rb')
    return pickle.load(f)
    f.close()
def search(res, flag):
    result=[]
    for i in res:
        result.append(load(i))
    if flag == '1':
        result.sort(key = lambda x:x['ctime'] , reverse = True)
    return result
def load_img(name):
    if name.rfind('_')!=-1:
        name=name[:name.rfind('_')]
    else:
        name=name[:-4]
    name+='.pkl'
    return load(name)
def searchImg(res):
    result=[]
    for i in res:
        result.append(load_img(i))
    return result
