# -*- coding: utf-8 -*-
from extract_cnn_vgg16_keras import VGGNet
import numpy as np
import matplotlib.image as mpimg
import hnswlib
import h5py
from keras.backend import clear_session
index = 'vgg_featureCNN.h5'
h5f = h5py.File(index,'r')
imgNames = h5f['dataset_2'][:]
h5f.close()

def query(filename,k):
    clear_session()
    model = VGGNet()
    queryVec = model.vgg_extract_feat(filename)
    p=hnswlib.Index('l2',512)
    p.load_index('hnswindex.bin')
    p.set_ef(50) #p>k
    return p.knn_query(queryVec,k)
if __name__ =='__main__':
    q = 'pic/wangyi7_2.jpg'
    x=query(q,10)[0]
    for i in x:
        print imgNames[i]
