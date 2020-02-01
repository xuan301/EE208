#!/home/bigzuoye/miniconda2/bin/python
import requests
import os
from my_load import load
from my_dump import dump
Njpeg=0
Npng=0
d=dict()
lajipic=[
"img5.cache.netease.com/sports/2012/12/27/20121227170948f48de.jpg",
"img1.cache.netease.com/catchpic/9/9B/9B40AEA8B68C4183B877D77FBDCDBC23.png",
"i3.sinaimg.cn/ty/temp/up/2014-06-30/U9380P6T64D96275F1091DT20140630130235.jpg",
"k.sinaimg.cn/n/sports/transform/20151203/qFYh-fxmcnkr7796015.jpg/w570b97.jpg",
"i3.sinaimg.cn/ty/2014/0724/U10623P6DT20140724172907.jpg",
"static.ws.126.net/cnews/css13/img/end_sports.png",
"n.sinaimg.cn/default/7772e5f8/20160324/sports_qrcode.png",
"k.sinaimg.cn/n/transform/20151022/3-iJ-fxizwsi5491750.jpg/w570a1f.jpg",
"img1.cache.netease.com/cnews/img/gallery13/wz/img/yuetu_logo_btm.png",
"static.ws.126.net/sports/2009/3/2/20090302064016a5da9.jpg",
"cms-bucket.nosdn.127.net/2019/01/04/4661e219fca94186a823c89358d523f7.jpeg?",
"k.sinaimg.cn/n/sports/transform/20151128/PhG4-fxmcnkr7643065.jpg/w570af5.jpg",
"img1.cache.netease.com/cnews/img/gallery11/bg06.png",
"img1.cache.netease.com/sports/2013/5/21/20130521081354bfd5e.png",
"i3.sinaimg.cn/ty/2015/0324/U9380P6DT20150324192358.jpg"
]
for _,__,files in os.walk('data'):
    for f in files:
        data=load(f)
        realimgs=[]
        for i in data['imgs']:
            try:
                laji=False
                for pic in lajipic:
                    if pic in i:
                        laji=True
                        break
                if laji:
                    continue
                r=requests.get(i,stream=True)
                print Njpeg,Npng
                filename=""
                if 'jpeg' in r.headers['content-type']:
                    Njpeg+=1
                    filename=str(Njpeg)+'.jpg'
                elif 'png' in r.headers['content-type']:
                    Npng+=1
                    filename=str(Npng)+'.png'
                if filename:
                    with open("pic/"+filename, "wb") as pic:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                pic.write(chunk)
                    realimgs.append((i,filename))
            except:
                continue
        print realimgs    
        data['realimgs']=realimgs
        dump(f,data)
