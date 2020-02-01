import web
from web import form
import urllib2
import os
import Search_7

urls = (
    '/', 'index',
    '/s', 's',
    '/im', 'index_img',
    '/i', 'image'
)


render = web.template.render('templates',cache=False) # your templates

login = form.Form(
    form.Textbox('Searching'),
    form.Button('Search'),
)

def func_txt(command):
    return Search_7.lab7txtSearch(command)

def func_pic(command):
    return Search_7.lab7picSearch(command)

class index:
    def GET(self):
        f = login()
        return render.formtest(f)

class index_img:
    def GET(self):
        f = login()
        return render.formimg(f)

class s:
    def GET(self):
        user_data = web.input()
        reuslt_txt = func_txt(user_data.Searching)
        return render.result_search_txt(user_data.Searching,reuslt_txt)

class image:
    def GET(self):
        user_data = web.input()
        result_pic = func_pic(user_data.Searching)
        return render.result_search_pic(user_data.Searching, result_pic)

if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()
