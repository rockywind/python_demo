import cv2

def read_txt(txt_file):

    f = open(txt_file)
    lines = f.readlines()
    i = 0
    x = []
    y = []
    for line in lines:
        error = line.split('error')[1].split('cam_new')[0].split('=')[1][2:-2]
        arr_error = error.split(',')
        x.append(arr_error[0])
        y.append(arr_error[1])
        i = i+1
        for each in x:
            x_float = map(lambda z:float(z),x)
        for each in y:
            y_float = map(lambda z:float(z),y)
    return x_float,y_float



import matplotlib.pyplot as plt
from pylab import *                                 
mpl.rcParams['font.sans-serif'] = ['SimHei']
# save_path = "C:\\Users\\rockywin.wang\\Desktop\\img\\vis\\"
# txt_file_1 = save_path + "tjp_carpoint_all_correct.txt"
# txt_file_2 =  save_path + "tjp_carpoint_all_ori.txt"

save_path = "/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/"
txt_file_1 = save_path + "0001_correct/20190624_rtk_ori_v1_01.txt"
txt_file_2 =  save_path + "20190624_rtk_ori_v1_01.txt"

y1_x,y1_y = read_txt(txt_file_1)
y2_x,y2_y = read_txt(txt_file_2)

names_x = range(0,len(y1_x),20)
x = range(len(y1_x))
plt.figure()

plt.plot(x, y1_x, marker='*', mfc='w',label=u'X_correct')
plt.plot(x, y2_x, marker='v', mfc='w',label=u'X_ori')
plt.xticks(names_x)
plt.legend()
plt.xlabel(u"id") 
plt.ylabel("X") 

# gcf: Get Current Figure
fig = plt.gcf()
plt.show()
fig.savefig(save_path + 'error_x_plot.png', dpi=1000)

plt.figure()

plt.plot(x, y1_y, marker='*', mfc='w',label=u'Y_correct')
plt.plot(x, y2_y, marker='v', mfc='w',label=u'Y_ori')
plt.xticks(names_x)
plt.legend() 
plt.margins(0)
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"id") 
plt.ylabel("Y") 



# gcf: Get Current Figure
fig = plt.gcf()
plt.show()
fig.savefig(save_path + 'error_y_plot.png', dpi=1000)



	

