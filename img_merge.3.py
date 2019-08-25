   
import sys
import os
from PIL import Image, ImageDraw
import argparse
import numpy as np
import random
import cv2
import time
import csv

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'


def read_csv(csv_path):

        csv_data_dict = dict()

        x_index = 1
        y_index = 2
        with open(csv_path) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):

                        if(i == 0):
                                continue
                       
                        frame_id_str = rows[0]
                        
                        channel_id = rows[1]
                        phy_x = float(rows[2])
                        phy_y = float(rows[3])
                        phy_x_rear = float(rows[4])
                        phy_y_rear = float(rows[5])

                 

                        csv_data_dict["{}".format(frame_id_str)] = [frame_id_str, channel_id, phy_x, phy_y,phy_x_rear,phy_y_rear]


        csvfile.close()
        return csv_data_dict


def generate_topview_img(width_topview, height_topview):

    # img = Image.new("RGB", (width_topview, height_topview))
    # return img

    image = np.zeros((height_topview, width_topview, 3), dtype=np.uint8)

    return image

def pixel_length(width_topview, height_topview,image_width, image_height):
    ep = 1e-15
    pixel_width = width_topview/(image_width+ep)
    pixel_height = height_topview/(image_height+ep)

    return pixel_width, pixel_height

def color_table():
    #color_list = [[0,255,0],[255,10,0],[255,235,205]]
    color_list = [[0,255,0],[0,10,255],[205,235,255],[238,245,255],]

    return color_list


def draw_topview(img, csv_data_dict, save_img_path,image_width,image_height):

    for key, value in csv_data_dict.items():
        csv_data = csv_data_dict[key]
        channel_id = csv_data[1]
        front_x = csv_data[2]
        front_y = csv_data[3]
        rear_x = csv_data[4]
        rear_y = csv_data[5]

        image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
        img = image

        # coordinate transform
        image_front_x = int(front_x + image_width*0.5)
        image_front_y = int(front_y + image_height*0.5)
        image_rear_x = int(rear_x + image_width*0.5)
        image_rear_y = int(rear_y + image_height*0.5)
        
        # point_front = (int(front_x+image_width*0.5), int(image_height - front_y))
        # point_rear = (int(rear_x+image_width*0.5), int(image_height -rear_y))

        point_front = (image_front_x, image_front_y)
        point_rear = (image_rear_x, image_rear_y)
        point_size =5
        thickness = 5
        line_thickness = 3

        if(image_front_x > 0 and image_front_x < image_width 
            and image_front_y > 0 and image_front_y < image_height 
            and image_rear_x > 0 and image_rear_x<image_width
            and image_rear_y > 0 and image_rear_y < image_height):
            # Draw a diagonal blue line with thickness of 5 px
            line_color = color_table()[2]
            cv2.line(img,point_front,point_rear,line_color,line_thickness)
        
        if(image_front_x > 0 and image_front_x < image_width 
            and image_front_y > 0 and image_front_y < image_height):
            point_color_front = color_table()[0]
            cv2.circle(img, point_front, point_size, point_color_front,thickness)
            
        if(image_rear_x > 0 and image_rear_x<image_width
            and image_rear_y > 0 and image_rear_y < image_height):
            point_color_rear = color_table()[1]
            cv2.circle(img, point_rear, point_size, point_color_rear,thickness)

  

        save_img_name = save_img_path + key + "_" + channel_id + ".jpg"

        cv2.imwrite(save_img_name,img)



def main():

    front_path_base = "/home/xieyi/save_img/img_12/0822/front_select/"
    left_path_base = "/home/xieyi/save_img/img_12/0822/left_select/"
    right_path_base = "/home/xieyi/save_img/img_12/0822/right_select/"
    topview_path_base = "/home/xieyi/save_img/img_12/0822/image_coordinate/"
    save_3pic = "/home/xieyi/save_img/img_12/0822/3pic_merge/"

    save_all = "/home/xieyi/save_img/img_12/0822/save_all/"
    mkdir(save_3pic)
    mkdir(save_all)
    # topview_width = 400*2
    # topview_height = 1150
    topview_width = int(720*(1150/800))
    topview_height = 720
    # img_resize_h = 320
    # img_resize_w = 640
    for value in os.listdir(front_path_base):

        suffix = value.split(".bmp")
        if(len(suffix)<=1):
            continue

        front_path = front_path_base + value
        left_path = left_path_base + value
        

        front_img = cv2.imread(front_path)
        
        large_img = np.zeros((front_img.shape[0], front_img.shape[1], 3), dtype=np.uint8)
        large_img_topview = np.zeros((topview_height, int(front_img.shape[1]*0.5+topview_width), 3), dtype=np.uint8)

        front_resize_pic = cv2.resize(src=front_img, 
                            dsize=(int(front_img.shape[1] * 0.5), 
                                int(front_img.shape[0] * 0.5))
        )

        #front_resize_pic = cv2.resize(src=front_img, (int(front_img.shape[1] * 0.5),int(front_img.shape[0] * 0.5)))

        left_img = cv2.imread(left_path)
        left_resize_pic = cv2.resize(src=left_img,
                            dsize=(int(left_img.shape[1] * 0.25),
                                int(left_img.shape[0] * 0.5))
        )
        frame_id = suffix[0].split("_")[-1]
        frame_img = frame_id + ".bmp"
        right_path = right_path_base +frame_img

        right_img = cv2.imread(right_path)
        right_resize_pic = cv2.resize(src=right_img,
                            dsize=(int(right_img.shape[1] * 0.25),
                                int(right_img.shape[0] * 0.5))
        )

        # crop_h_min = int(topview_height -front_img.shape[0])
        # crop_h_max = int(topview_height -front_img.shape[0] + front_img.shape[0]*0.5)
        # crop_w_min = int(front_img.shape[1]*0.25)
        # crop_w_max = int(crop_w_min + front_img.shape[1]*0.5)

        crop_h_min = int(0)
        crop_h_max = int( front_img.shape[0]*0.5)
        crop_w_min = int(0)
        crop_w_max = int(front_img.shape[1]*0.5)


        large_img_topview[crop_h_min :crop_h_max,crop_w_min:crop_w_max,:] = front_resize_pic
      
        crop_h_min_left = 360
        crop_w_min_left = 0
        crop_w_max_left = 320
        large_img_topview[crop_h_min_left:,0:crop_w_max_left,:] = left_resize_pic

        crop_h_min_right = 360
        crop_w_min_righ = 320
        crop_w_max_righ = crop_w_min_righ*2
        
        large_img_topview[crop_h_min_right:,crop_w_min_righ:crop_w_max_righ, :] = right_resize_pic
        save_img_name = save_3pic + frame_img
        #cv2.imwrite(save_img_name, large_img)
        
        topview = cv2.imread(topview_path_base + frame_img)
        topview = cv2.resize(src=topview,
                            dsize=(int(topview_width),
                                int(topview_height)))
        topview_w_min = 0
        large_img_topview[:,int(front_img.shape[1]*0.5):,:] = topview

        #large_img_topview[:,1281,:] = color_table()[2] # border

        # point_center = (400, 700)
        # point_size = 5
        # point_color = [96,164,244]
        # #point_color = [0,0,255]
        # point_thickness = 5
        # cv2.circle(large_img_topview-, point_center, point_size, point_color,point_thickness)




        # large_img_topview[0:720,0:1280,:] = large_img
        # #large_img_topview[20:720, 1280:,] = topview
        # large_img_topview[20:720, 1280:,:] = topview

        # large_img_topview[:,1281,:] = [0,0,255]  # border

        # point_center = (715, 1680)
        # point_size = 5
        # point_color = [96,164,244]
        # #point_color = [0,0,255]
        # point_thickness = 5
        # large_img_topview[point_center[0],point_center[1],:] = [0,0,255]  # center
        # cv2.circle(large_img_topview, point_center, point_size, point_color,point_thickness)
        

        #large_img_topview[1280:,20:720, :] = topview
        save_topview = save_all + frame_img
        cv2.imwrite(save_topview, large_img_topview)



    
if __name__ == "__main__":

    main()

    
 

