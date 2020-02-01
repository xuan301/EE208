import os
from my_load import load
from my_dump import dump
for _,__,files in os.walk('data'):
    for f in files:
        data=load(f)
        realimgs=[]
        for i in range(len(data['realimgs'])):
            print data['realimgs'][i][0]
            print data['realimgs'][i][1]
            realimgs.append((data['realimgs'][i][0],f[:-4]+'_'+str(i)+'.jpg'))
        #    print 'pic/'+data['realimgs'][i][1]
        #    print 'pic/'+f[:-4]+'_'+str(i)+'.jpg'
            os.rename('pic/'+data['realimgs'][i][1],'pic/'+f[:-4]+'_'+str(i)+'.jpg')
        print realimgs
        data['realimgs']=realimgs
        dump(f,data)
