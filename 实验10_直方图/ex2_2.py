#!/usr/bin/env python
import cv2
import numpy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

img = cv2.imread("img1.png",0)

list = []

H = len(img)
W = len(img[0])

for j in range(1, H - 1):
    for k in range(1, W - 1):
        Ix = (img[j][k + 1]) - (img[j][k - 1])
        Iy = (img[j + 1][k]) - (img[j - 1][k])
        I = (Ix ** 2 + Iy ** 2) ** 0.5
        list.append(I)

number = 360

plt.hist(list,360,density=1)

plt.legend()

plt.xlabel("Gradient")
plt.title("GrayGrad")

plt.show()
