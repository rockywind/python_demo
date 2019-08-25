
import sys
import os
from PIL import Image, ImageDraw
import argparse
import numpy as np
import random
import cv2
import time
import csv
import random

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'

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
    
    color_list = [[0,255,0],[0,10,255],[205,235,255]]

    return color_list

def draw_lane(image,key):

    car_width = 185
    topview_width_center = 400
    lane_x = 118
    lane_x_min = 115 
    #lane_x_max = 134 
    lane_x_max = 118
    frame_id_interval = 20

    lane_x_right_min = 117
    lane_x_right = 118
    lane_x_right_max = 120


    #lane_x = topview_width_center - car_width*0.5
    key_num = int(key)
    if (key_num%frame_id_interval == 0):
        lane_x = random.randint(lane_x_min, lane_x_max)
        lane_x_right = random.randint(lane_x_right_min,lane_x_right_max)

    lane_x = topview_width_center - lane_x 
    lane_x_right = topview_width_center + lane_x_right
    lane_width = 2

    image[:,lane_x-lane_width:lane_x + lane_width,:] =[0,0,255] # left lane
    image[:,lane_x_right-lane_width:lane_x_right + lane_width,:] =[0,0,255] # left lane

    return image




def draw_topview(img, csv_data_dict, save_img_path,image_width,image_height):

    for key, value in csv_data_dict.items():
        csv_data = csv_data_dict[key]
        channel_id = csv_data[1]
        front_x = csv_data[2]
        front_y = csv_data[3]
        rear_x = csv_data[4]
        rear_y = csv_data[5]

        front_flag_zero = 1
        rear_flag_zero = 1

        if(front_x == 0 and front_y == 0):
            front_flag_zero = 0

        if(rear_x == 0 and rear_y == 0):
            rear_flag_zero = 0

        image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
        img = image
 

        # coordinate transform
        image_front_x = int(front_x + image_width*0.5)
        #image_front_y = int(front_y + image_height*0.5)
        image_front_y = int(image_height - (front_y + 450))
        image_rear_x = int(rear_x + image_width*0.5)
        #image_rear_y = int(rear_y + image_height*0.5)
        image_rear_y = int(image_height - (rear_y + 450))
        
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

            if(front_flag_zero != 0 and rear_flag_zero != 0):
                
                # Draw a diagonal blue line with thickness of 5 px
                line_color = color_table()[2]
                cv2.line(img,point_front,point_rear,line_color,line_thickness)
        
        if(image_front_x > 0 and image_front_x < image_width 
            and image_front_y > 0 and image_front_y < image_height):
            if(front_flag_zero != 0):
                point_color_front = color_table()[0]
                cv2.circle(img, point_front, point_size, point_color_front,thickness)
            
        if(image_rear_x > 0 and image_rear_x<image_width
            and image_rear_y > 0 and image_rear_y < image_height):
            if(rear_flag_zero != 0):
                point_color_rear = color_table()[1]
                cv2.circle(img, point_rear, point_size, point_color_rear,thickness)

        image = draw_lane(image,key)
            
        #save_img_name = save_img_path + key + "_" + channel_id + ".jpg"
        save_img_name = save_img_path + key  + ".bmp"

        cv2.imwrite(save_img_name,img)


def main():

    width_topview = 800
    height_topview = 1150
    image_width = 800
    image_height = 1150

    src_csv_path = '/home/xieyi/save_img/img_12/0822/y=2.6_x=5_y=6_y=4.5_487_699_filter.csv'
    save_img_path = '/home/xieyi/save_img/img_12/0822/topview/'
    csv_data_dict = read_csv(src_csv_path)
    mkdir(save_img_path)
    
    pixel_width, pixel_height = pixel_length(width_topview, height_topview,image_width, image_height)
    img = generate_topview_img(width_topview, height_topview)
    draw_topview(img, csv_data_dict, save_img_path,image_width,image_height)







    
if __name__ == "__main__":
    #width_topview = 400*2
    #height_topview = 700
    main()

    
 

