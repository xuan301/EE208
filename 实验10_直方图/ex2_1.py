#encoding:utf-8
import cv2  
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread('img2.png',0)


plt.title("Grayscale Histogram")#图像的标题
plt.xlabel("Bins")#X轴标签
plt.ylabel("# of Pixels")#Y轴标签
plt.hist(src.ravel(), 256,range=[0, 256],density=1)
plt.show()