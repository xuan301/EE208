#encoding:utf-8
import cv2  
import numpy as np
import matplotlib.pyplot as plt

src = cv2.imread('img2.png')
'''
cv2.imshow("src", src)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

B = np.sum(src[:,:,0])
G = np.sum(src[:,:,1])
R = np.sum(src[:,:,2])
total = float(B+G+R)
print B/total
percent_B = round(B/total,3)
percent_G = round(G/total,3)
percent_R = round(R/total,3)
print (percent_B,percent_G,percent_R)
X = ['Blue','Green','Red']
Y = [percent_B,percent_G,percent_R]


plt.title("Color Histogram")#图像的标题
plt.xlabel("Color")#X轴标签
plt.ylabel("Percent")#Y轴标签
plt.bar(X,Y,width=1,color=['b','g','r'])
for xx,yy in zip(X,Y):
    plt.text(xx,yy+0.005,str(yy),ha='center')
plt.show()
