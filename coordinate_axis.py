import os
import cv2
import numpy as np
from scipy import misc
import matplotlib.image as mpimg
import matplotlib.pyplot as plt



# 前视
x2 = [3.96765, 5.13094]
y2 = [5.4662, 5.67416]
# 右视
x3 = [5.09047, 8.10554]
y3 = [4.30288, 5.21785]

# 右视中点
x_right = 1
y_right = -0.5

x = np.linspace(-8, 8, 1000)
plt.figure()
# 设置坐标轴的取值范围
plt.xlim((-8, 8))
plt.ylim((-8, 8))
# 设置x坐标轴刻度, 原来为0.25, 修改后为0.5

plt.xticks(np.linspace(-8, 8, 17))
plt.yticks(np.linspace(-8, 8, 17))
y1 = 0.5*x


ax = plt.gca() # get current axis

ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none')         # 将右边 上边的两条边颜色设置为空 其实就相当于抹掉这两条边

ax.xaxis.set_ticks_position('bottom')   
ax.yaxis.set_ticks_position('left')          # 指定下边的边作为 x 轴   指定左边的边为 y 轴

ax.spines['bottom'].set_position(('data', 0))   #指定 data  设置的bottom(也就是指定的x轴)绑定到y轴的0这个点上
ax.spines['left'].set_position(('data', 0))

plt.plot(x, y1, linestyle=' ')
#plt.plot(x2, y2,'ro') # draw point
plt.plot([0,x2[0]],[0,y2[0]],linestyle='-',color = 'green')
plt.plot([0,x2[1]],[0,y2[1]],linestyle='-',color = 'green')
plt.plot(x2,y2,linestyle='-',color = 'green')
#plt.annotate("front", xy = (x2[0], y2[0]), xytext = (x2[0]+1, y2[0]+1), arrowprops = dict(facecolor = 'black', shrink = 0.01))

plt.plot([x_right,x3[0]],[y_right,y3[0]],linestyle='-',color = 'red')
plt.plot([x_right,x3[1]],[y_right,y3[1]],linestyle='-',color = 'red')
plt.plot(x3,y3,linestyle='-',color = 'red')

# get current figure
fig = plt.gcf()
fig.savefig('1.png',dpi=100)
#plt.show()
img = cv2.imread('1.png')
print img.shape
#各参数依次是：照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
#cv2.putText(img, 'lena', (325,35), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 12)
cv2.putText(img, 'y', (323,42), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
cv2.putText(img, 'x', (592,248), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
cv2.imshow("lena", img)
cv2.imwrite("11.png",img)
cv2.waitKey()


