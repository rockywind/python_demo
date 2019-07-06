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

def num_split(line):
        
    min_x = 2.
    max_x = 3.6
    min_y = 3.
    max_y = 5.


    list_num = line.split(",")
    if(len(list_num) <= 1):
            return False

    phy_x = float(list_num[0].split("[")[1])
    phy_y = float(list_num[1].split("]")[0])
    
    if(phy_x > -min_x and phy_x < min_x and phy_y < min_y):
        return False

    if(phy_x > max_x or phy_x < -max_x or phy_y > max_y):
        return False

    return True



src_file_path = '/home/xieyi/pic/projection_error/all_txt/chessbox_data/'
save_file_path = '/home/xieyi/pic/projection_error/all_txt/20190617_chessbox_label_02.txt'
#mkdir(save_image_path)
file_type = '.txt'

file_write = open(save_file_path,"w+")


for root, dirs,files in os.walk(src_file_path, topdown=False):
     
        
        for name in files:

                name_list = name.split(file_type)
                if(len(name_list) <= 1):
                        continue
                file_path = os.path.join(root, name)
                
                file_write.write(file_path)
                file_write.write("\n")
                with open(file_path, 'r') as file_read:
                        while True:

                                line = file_read.readline() 

                                if not line:
                                        break

                                flag = num_split(line)
                                if(flag == False):
                                        continue

                                line_str = str(line)
                                file_write.write(line_str)
                               

                file_read.close()
                file_write.write("\n")

file_write.close()

         
