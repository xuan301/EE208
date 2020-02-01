# -*- coding: utf-8 -*-
from extract_cnn_vgg16_keras import VGGNet
import numpy as np
import h5py
import matplotlib.image as mpimg
import argparse

query = 'pic/wangyi2682_0.jpg'
index = 'vgg_featureCNN.h5'
result = 'pic/'
# read in indexed images' feature vectors and corresponding image names
h5f = h5py.File(index,'r')
# feats = h5f['dataset_1'][:]
feats = h5f['dataset_1'][:]
print(feats)
imgNames = h5f['dataset_2'][...]
h5f.close()
        
print("--------------------------------------------------")
print("               searching starts")
print("--------------------------------------------------")
    
# read and show query image
# queryDir = args["query"]

# init VGGNet16 model
model = VGGNet()

# extract query image's feature, compute simlarity score and sort
queryVec = model.vgg_extract_feat(query)    #修改此處改變提取特徵的網路
print(queryVec.shape)
print(feats.shape)
scores = np.dot(queryVec, feats.T)
rank_ID = np.argsort(scores)[::-1]
rank_score = scores[rank_ID]
# print (rank_ID)
print (rank_score)


# number of top retrieved images to show
maxres = 3          #檢索出三張相似度最高的圖片
imlist = []
for i,index in enumerate(rank_ID[0:maxres]):
    imlist.append(imgNames[index])
    # print(type(imgNames[index]))
    print("image names: "+str(imgNames[index]) + " scores: %f"%rank_score[i])
print("top %d images in order are: " %maxres, imlist)
# show top #maxres retrieved result one by one
for i,im in enumerate(imlist):
    print result+"/"+str(im)
