#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, jieba

import web
from web import form
import urllib2
import os

import Search_front,my_load_front,query_front

urls = (
    '/', 'index',
    '/t', 's'
)


render = web.template.render('templates',cache=False) # your templates

class index:
    def GET(self):
        return render.index()

class s:
    def GET(self):
        user_data = web.input()
        command = user_data.keyword
        if command =='':
            return render.index()
        flag = user_data.flag
        a=func_text(command,flag)
        return render.result_text2(a)
            
    def POST(self):
        x = web.input(myfile={})
        if(x['myfile'].value==''):
            return render.index()
        # web.debug(x['myfile'].filename) 
        # web.debug(x['myfile'].value) 
        # print x['myfile'].value
        with open('/home/bigzuoye/News/News/img_tmp/tmp.jpg','wb') as f:
            f.write(x['myfile'].value)
        return render.result_img1(func_img(query_front.Search_img()))

def func_text(command, flag):
    return [command,my_load_front.search(Search_front.Search_text(command), flag)]
def func_img(res):
    result=[]
    for i in res:
        result.append([i,my_load_front.load_img(i)])
    return result



if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
