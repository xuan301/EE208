# -*- coding: utf-8 -*-
import numpy as np
from numpy import linalg as LA

from keras.applications.vgg16 import VGG16
# from keras.applications.resnet50 import ResNet50
# from keras.applications.densenet import DenseNet121
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
# from keras.applications.resnet50 import preprocess_input as preprocess_input_resnet
# from keras.applications.densenet import preprocess_input as preprocess_input_densenet
class VGGNet:
    def __init__(self):
        # weights: 'imagenet'
        # pooling: 'max' or 'avg'
        # input_shape: (width, height, 3), width and height should >= 48
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        # include_top：是否保留頂層的3個全連線網路
        # weights：None代表隨機初始化，即不載入預訓練權重。'imagenet'代表載入預訓練權重
        # input_tensor：可填入Keras tensor作為模型的影象輸出tensor
        # input_shape：可選，僅當include_top=False有效，應為長為3的tuple，指明輸入圖片的shape，圖片的寬高必須大於48，如(200,200,3)
        #pooling：當include_top = False時，該引數指定了池化方式。None代表不池化，最後一個卷積層的輸出為4D張量。‘avg’代表全域性平均池化，‘max’代表全域性最大值池化。
        #classes：可選，圖片分類的類別數，僅當include_top = True並且不載入預訓練權重時可用。
        self.model_vgg = VGG16(weights = self.weight, input_shape = (self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling = self.pooling, include_top = False)
     #    self.model_resnet = ResNet50(weights = self.weight, input_shape = (self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling = self.pooling, include_top = False)
     #   self.model_densenet = DenseNet121(weights = self.weight, input_shape = (self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling = self.pooling, include_top = False)
        self.model_vgg.predict(np.zeros((1, 224, 224 , 3)))
    #    self.model_resnet.predict(np.zeros((1, 224, 224, 3)))
    #    self.model_densenet.predict(np.zeros((1, 224, 224, 3)))
    '''
    Use vgg16/Resnet model to extract features
    Output normalized feature vector
    '''
    #提取vgg16最後一層卷積特徵
    def vgg_extract_feat(self, img_path):
        img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_vgg(img)
        feat = self.model_vgg.predict(img)
        # print(feat.shape)
        norm_feat = feat[0]/LA.norm(feat[0])
        return norm_feat
    #提取resnet50最後一層卷積特徵
    def resnet_extract_feat(self, img_path):
        img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_resnet(img)
        feat = self.model_resnet.predict(img)
        # print(feat.shape)
        norm_feat = feat[0]/LA.norm(feat[0])
        return norm_feat
    #提取densenet121最後一層卷積特徵
    def densenet_extract_feat(self, img_path):
        img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_densenet(img)
        feat = self.model_densenet.predict(img)
        # print(feat.shape)
        norm_feat = feat[0]/LA.norm(feat[0])
        return norm_feat
