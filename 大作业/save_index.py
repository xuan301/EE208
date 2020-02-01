# -*- coding: utf-8 -*-
import hnswlib
import numpy as np
import h5py
dim = 512
index = 'vgg_featureCNN.h5'
h5f = h5py.File(index,'r')
feats = h5f['dataset_1'][:]
imgNames = h5f['dataset_2'][:]
h5f.close()
p = hnswlib.Index(space = 'l2', dim = dim)
p.init_index(max_elements = feats.shape[0], ef_construction = 200, M = 16)
p.add_items(feats,np.arange(feats.shape[0]))
p.save_index('hnswindex.bin')
