
import sys
import os
from PIL import Image, ImageDraw
import argparse
import numpy as np
import random
import cv2
import time

def draw_arc(draw,horizontal_distance,vertical_distance_end,vertical_distance_start,distance,fill):
    vertical_distance = vertical_distance_end-vertical_distance_start     
    draw.arc((int(horizontal_distance/2)-distance,int(vertical_distance)-distance,int(horizontal_distance/2)+distance,int(vertical_distance)+distance), 0, -1, fill = fill)

    return draw
# parse look up tablekk

def draw_circle_in_image(width_topview, height_topview, stride = 100):
    
    im = Image.new("RGB", (width_topview, height_topview))
 
    horizontal_distance = width_topview
    vertical_distance_end = height_topview
    vertical_distance_start = 0
    draw = ImageDraw.Draw(im)
    #for distance in range(100,2100,100):
    for distance in range(stride,height_topview + stride,stride):
        draw = draw_arc(draw,horizontal_distance,vertical_distance_end,vertical_distance_start,distance,(255,255,255))
   
    #im.show()
    im.save('2.jpg')
    return im

def get_look_up_table(look_up_table_path):
    #look_up_table_path = 'LookUpTable_20_10_old.txt'
    t0 = time.clock()
    look_up_table_dict = dict()
    with open(look_up_table_path, "r") as file_look_up_table:
        str_look_up_table = file_look_up_table.read()
        for line in str_look_up_table.split("#"):
                line_temp = line.split(" ")
                if len(line_temp) <= 2:
                    continue
                image_axis_list = line_temp[2].split("/")
                if len(image_axis_list) < 2:
                    continue
                
                look_up_table_dict["{}/{}".format(line_temp[0], line_temp[1])] = [int(float(image_axis_list[0])), int(float(image_axis_list[1]))]
    print 'get_look_up time++++', time.clock() - t0
    return look_up_table_dict

#def print_to_txt():
    
def get_look_up_table_xy(look_up_table_path, image_x, image_y):
    x_distance = image_x
    y_distance = image_y
    #print '-----image_x-----', image_x
    #print '-----image_y-----', image_y
    #x_distance = 1280
    #y_distance = 720
    look_up_table_x = np.zeros((x_distance , y_distance ))
    look_up_table_y = np.zeros((x_distance , y_distance ))
    print '-----look_up_table_x.shape-----', np.shape(look_up_table_x)
    with open(look_up_table_path, "r") as file_look_up_table:
        str_look_up_table = file_look_up_table.read()
        for line in str_look_up_table.split("#"):
                line_temp = line.split(" ")
                if len(line_temp) <= 2:
                    continue
                image_phy_axis_list = line_temp[2].split("/")
                if len(image_phy_axis_list) < 2:
                    continue
                
           
                look_up_table_x[int(line_temp[0])][int(line_temp[1])] = int(float(image_phy_axis_list[0]))
               
                look_up_table_y[int(line_temp[0])][int(line_temp[1])] = int(float(image_phy_axis_list[1]))
    f = open(".//look_up_table_x.txt", 'w+') 
    print >> f, look_up_table_x    
    print 'look_up_table_x=====' , look_up_table_x      
           

    return look_up_table_x, look_up_table_y

def get_top_view_img_from_fish_gray_xy(source_image, vertical_distance_start, vertical_distance_end, horizontal_distance, look_up_table_x, look_up_table_y, save_image_array):
    #t0 = time.clock()
    #fish_image_array =np.zeros((720, 1280), dtype = np.int)
    fish_image_array = cv2.imread('.//000086.jpg')
    source_image_array = np.array(source_image)
    #source_image_array = source_image_array[:,:,1]
    offset = int(horizontal_distance / 2)
    
    offset = 2*offset

    
    # look up physic coordinate
    img_h = 720 - 2
    img_w = 1280 -2
    
    phy_img_w = 1000
    phy_img_h = 1000
    img = np.zeros((phy_img_w,phy_img_h,3), np.uint8)
    img = source_image_array
    
    col_1 = 661
    row_1 = 296
    
    col_phy = int(look_up_table_x[col_1][row_1]) 
    row_phy = int(look_up_table_y[col_1][row_1])
    
    # coordinate transform
    col_phy = int(col_phy + phy_img_w * 0.5)
    row_phy = phy_img_h - row_phy
    
      
    cv2.circle(img, (col_phy, row_phy), radius = 5,color = (0,255,255), thickness = -1)
    
    col_1 = 929
    row_1 = 384
    
    col_phy = int(look_up_table_x[col_1][row_1]) 
    row_phy = int(look_up_table_y[col_1][row_1])
    
    # coordinate transform
    col_phy = int(col_phy + phy_img_w * 0.5)
    row_phy = phy_img_h - row_phy
    
    
    cv2.circle(img, (col_phy, row_phy), radius = 5,color = (0,255,255), thickness = -1)
    
    
    
    '''
    img = source_image_array
    # iteration image pixel
    for row in range(0, img_h, 1):
        #for col in range(-offset, offset, 1):
        for col in range(0, img_w, 1):
            col_phy = int(look_up_table_x[col][row])
            row_phy = int(look_up_table_y[col][row])
           
            # coordinate transform
            col_phy = int(col_phy + phy_img_w * 0.5)
            row_phy = phy_img_h - row_phy
            
            if col_phy <= 0 or row_phy <= 0 :
                print '----col_phy---', col_phy
                print '----row_phy---', row_phy
                continue 
            
            if col_phy >= phy_img_w or row_phy >= phy_img_h :
                continue
            #source_image_array[int(row_phy )][int(col_phy)][:] = fish_image_array[row][col][:]
            img[int(row_phy )][int(col_phy)][:] = fish_image_array[row][col][:]
    
            
    '''
           
    cv2.imwrite('3.jpg',img)
    
    '''
    img = Image.fromarray(source_image_array)
    #img.show()
    cv2.imwrite('3.jpg',fish_image_array)
    img.save('4.bmp')
    '''
    return img

def get_top_view_img_from_fish_gray(source_image, vertical_distance_start, vertical_distance_end, horizontal_distance, look_up_table_dict, save_image_array):
    
    t0 = time.clock()
    image = Image.new("RGB", (1280,720))
    image = np.array(image)
    fish_image_array = np.array(image)

    source_image_array = np.array(source_image)

    offset = int(horizontal_distance / 2)

    for row in range(vertical_distance_end, vertical_distance_start, -1):
        for col in range(-int(horizontal_distance / 2), int(horizontal_distance / 2), 1):
            col_ori = int(look_up_table_dict["{}/{}".format(col, row)][0])
            row_ori = int(look_up_table_dict["{}/{}".format(col, row)][1])
              
            if source_image_array[vertical_distance_end-row][col + offset][1] >= 255:
                    fish_image_array[row_ori][col_ori] = source_image_array[vertical_distance_end-row][col+offset][1]

                
    img = Image.fromarray(fish_image_array)
    print 'get_top_view_img_from_fish++++', time.clock() - t0
    #img.show()
    
    cv2.imwrite('3.jpg',fish_image_array)
    img.save('4.bmp')
    return img


    
if __name__ == "__main__":
    look_up_table_path = 'C:\\Users\\rockywin.wang\\Desktop\\01_src\\tjp\\front_cam_to_phy.txt'
 
    
    vertical_distance_start = 0
    vertical_distance_end = 1000
    horizontal_distance = 1000
    img_x = 1280
    img_y = 720
    look_up_table_x, look_up_tapible_y = get_look_up_table_xy(look_up_table_path, img_x, img_y)
    
    source_image = draw_circle_in_image(horizontal_distance, vertical_distance_end - vertical_distance_start)
    #source_image.show()
    save_image_array = 'reproject.jpg'
    #get_top_view_img_from_fish_gray(source_image, vertical_distance_start, vertical_distance_end, horizontal_distance, look_up_table_dict, save_image_array)
    #source_image = 1
    get_top_view_img_from_fish_gray_xy(source_image, vertical_distance_start, vertical_distance_end, horizontal_distance, look_up_table_x, look_up_table_y, save_image_array)


    
 

