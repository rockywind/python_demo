import os
import cv2
import numpy as np
from scipy import misc
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def scope_adjust(X, axis='X', scale=0.1):
    xmin, xmax = X.min(), X.max()

    dx = (xmax - xmin) * scale
    if axis == 'X':
        plt.xlim(xmin - dx, xmax + dx)
    else:
        plt.ylim(xmin - dx, xmax + dx)

# 扩展 x 轴边界 10%
def xscope_adjust(X):
    scope_adjust(X, 'X')

# 扩展 y 轴边界 10%
def yscope_adjust(Y):
    scope_adjust(Y, 'Y')

def draw_coordinate():

    width = 800
    height = 1150

    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C,S = np.cos(X), np.sin(X)

    # 创建一个宽10，高8 英寸（inches，1inch = 2.54cm）的图，并设置分辨率为72 (每英寸像素点数)
    plt.figure(figsize=(23, 16), dpi=50)
    #plt.subplot(1,1,1)
    fig, ax = plt.subplots() 
    # 绘制正弦曲线，使用绿色的、连续的、宽度为 1 （像素）的线条
    plt.plot(X, S, color="orange", linewidth=10.0, linestyle=" ")

    fig.set_size_inches(width/50.0, height/50.0) 
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)
    
    # 设置 x轴的上下限
    plt.xlim(-4, 4,)

    # 设置 x轴记号
    plt.xticks(np.linspace(-4, 4, 9, endpoint=True))

    # 设置 y轴的上下限
    plt.ylim(-5, 7)

    # 设置 y轴记号
    plt.yticks(np.linspace(-5, 7, 13, endpoint=True))

    # translation coordination
    ax = plt.gca()
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('right')
    ax.spines['right'].set_position(('data', 0))
    # end



    # 在屏幕上显示
    #plt.show()
    fig = plt.gcf()
    fig.savefig('1.png',dpi=50)

def main():
    image_path ="/home/xieyi/save_img/img_12/0822/topview/14841.bmp"
    im = cv2.imread(image_path)
    fig, ax = plt.subplots() 
    im = im[:, :, (2, 1, 0)] 
    ax.imshow(im, aspect='equal') 
  

    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C,S = np.cos(X), np.sin(X)
    plt.plot(X, S, color="orange", linewidth=10.0, linestyle=" ")
    # 设置 x轴的上下限
    plt.xlim(-4, 4,)

    # 设置 x轴记号
    plt.xticks(np.linspace(-4, 4, 9, endpoint=True))

    # 设置 y轴的上下限
    plt.ylim(-5, 7)

    # 设置 y轴记号
    plt.yticks(np.linspace(-5, 7, 13, endpoint=True))

    # translation coordination
    ax = plt.gca()
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('right')
    ax.spines['right'].set_position(('data', 0))

    plt.show()

    plt.axis('off') 
    # 去除图像周围的白边 
    height, width, channels = im.shape 
    # 如果dpi=300，那么图像大小=height*width 
    fig.set_size_inches(width/100.0/3.0, height/100.0/3.0) 
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)

    plt.savefig('result.png',dpi=300)


if __name__ == "__main__":

    #main()
    draw_coordinate()



