import web
from web import form
import urllib2
import os
import Search_6

urls = (
    '/', 'index',
    '/s', 's'
)


render = web.template.render('templates',cache=False) # your templates

login = form.Form(
    form.Textbox('Searching'),
    form.Button('Search'),
)

def func_txt(command):
    return Search_6.lab7txtSearch(command)

class index:
    def GET(self):
        f = login()
        return render.formtest(f)

class s:
    def GET(self):
        user_data = web.input()
        reuslt_txt = func_txt(user_data.Searching)
        return render.result_search_txt(user_data.Searching,reuslt_txt)

if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()
