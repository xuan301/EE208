import pickle
def dump(filename,data):
    f=open('data/'+filename,'wb')
    pickle.dump(data,f)
    f.close()
