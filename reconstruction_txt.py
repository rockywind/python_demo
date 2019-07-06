import numpy as np
import os
import scipy.misc as sm
#import cv2

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'

def check_num(phy_x, phy_y, img_x, img_y):

    min_x = 3.
    max_x = 3.6
    min_y = 3. + 1e-8
    max_y = 5.
    second_max_y = 1.5
    
    if(phy_x > -min_x and phy_x < min_x and phy_y < min_y):
        return False

    if(phy_x > max_x or phy_x < -max_x or phy_y > max_y):
        return False

    if(phy_x >= min_x and phy_x < max_x and phy_y < second_max_y):
            return False

    if(phy_x <= -min_x and phy_x > -max_x and phy_y < second_max_y):
            return False

    return True


def num_split(line):
        

    list_num = line.split("_")
    if(len(list_num) <= 1):
            return False

    phy_x = float(list_num[1])
    
    phy_y = float(list_num[-1].split(" ")[0])
    
    img_x_tmp = list_num[-1].split("(")[1]
    img_x = float(img_x_tmp.split(" ")[0])

    img_y_tmp = img_x_tmp.split(" ")[1]

    img_y = float(img_y_tmp.split(")")[0])

    


    return phy_x, phy_y, img_x, img_y


    
src_file_path = '/home/xieyi/pic/projection_error/all_txt/20190616_carpoint/'
save_file_path = '/home/xieyi/pic/projection_error/all_txt/20190619_carpoint_label.txt'
#mkdir(save_image_path)
file_type = '.txt'

file_write = open(save_file_path,"w+")


for files in os.listdir(src_file_path):

        name_list = files.split(file_type)
        if(len(name_list) <= 1):
                continue

        file_path = os.path.join(src_file_path, files)

        with open(file_path, 'r') as file_read:
                while True:

                        line = file_read.readline() 

                        if not line:
                                break

                        phy_x, phy_y, img_x,img_y = num_split(line)
                        flag = check_num(phy_x, phy_y,img_x, img_y)
                        
                        if(flag == False):
                                continue
                        phy_x_str = str(phy_x)
                        phy_y_str = str(phy_y)
                        img_x_str = str(img_x)
                        img_y_str = str(img_y)

                        line_list = "[" + phy_x_str + "," +phy_y_str + "]" + " " + "[" + img_x_str \
                                        + "," + img_y_str + "]" + "\n"
                       
                        file_write.write(line_list)

        
        file_read.close()
        file_write.close()

        
        
         
