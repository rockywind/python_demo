#!/usr/bin/python
# -*- coding: <encoding name> -*-
import numpy as np
import os
import scipy.misc as sm
import cv2
import csv

import codecs


import matplotlib.pyplot as plt

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'

def write_data_to_txt(file_name, write_data):

        file_write = open(file_name,"w+")

        for index, value in enumerate(write_data):

                phy_coordinate = value[0]
                img_coordinate = value[-1]

                #roi filter
                flag = phy_coordinate_filter(phy_coordinate)
                if(flag == False):
                        continue

                phy_x = str(phy_coordinate[0])
                phy_y = str(phy_coordinate[1])
                img_x = str(img_coordinate[0])
                img_y = str(img_coordinate[1])
                write_line = '[' + phy_x + ',' + phy_y + ']' + ' ' \
                        '[' + img_x + ',' + img_y + ']' + '\n'
               
                file_write.write(write_line)

        file_write.close()


def write_data_to_csv(file_name, write_data):

       
        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        file_head = ['frame_id', 'phy_x','phy_y']

        targetWriter.writerow(file_head)

        for index, write_data_row in enumerate(write_data):

                out_data = write_data_row
                targetWriter.writerow(out_data)

        outFile.close()

                     


        
if __name__ == "__main__":
        
        x_key = 'pos_FRTire_x'
        y_key = 'pos_FRTire_y'
        #img_id = 'img_id'

        # src_img_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/0002_rtk_50hz/output/'
        # src_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/rtk_phy_to_cam.csv'
        # save_save_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/img_draw/'

        #src_img_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/output/'

        # src_img_path = '/media/xieyi/Elements/zwk/20190704/rtk_video_det/20190706_capture1_select_01/'

        # src_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/rtk_phy_to_cam_real.csv'
        # save_save_path = '/media/xieyi/Elements/zwk/20190704/rtk_video_det/capture_1_frontoutput/capture1_img_draw_real/'

        src_img_path = '/media/xieyi/Elements/zwk/changan_0712/cutin_img_select/'

        src_csv_path = '/media/xieyi/Elements/zwk/changan_0712/rtk_phy_to_cam_real.csv'
        save_save_path = '/media/xieyi/Elements/zwk/changan_0712/cutin_img_select_rtk_draw/'

        mkdir(save_save_path)

        write_data = list()

        file_suffix = ".bmp"
        for file_name in os.listdir(src_img_path):

                if len(file_name.split(file_suffix))<=1:
                        continue

                img = cv2.imread(src_img_path + file_name)

                frame_id_tmp = file_name.split(".")
                frame_id = frame_id_tmp[0].split("_")[-1]

                first_line_flag = True

                

                phy_dict = {}
                #save_csv_path = src_txt_path + file_name
                with open(src_csv_path, 'r') as file_read:
                        while True:

                                line_ori = file_read.readline() 
                                
                                if not line_ori:
                                        break
                                # skip first line
                                if first_line_flag:
                                        
                                        first_line_flag = False
                                        continue

                                line_del = line_ori[:-1]
                                line = line_del.split(",")
                                img_id_tmp = line[0].split(".")
                                img_id = img_id_tmp[0]

                                if(img_id == frame_id):
                                        # if(img_id == '2085'):
                                        #         print("-----")
                                        x_coordinate_str = line[1]
                                        y_coordinate_str = line[2]

                                        x_coordinate_tmp = float(x_coordinate_str)
                                        y_coordinate_tmp = float(y_coordinate_str)

                                        x_coordinate = int(x_coordinate_tmp)
                                        y_coordinate = int(y_coordinate_tmp)

                                        point_size = 1
                                        #point_color = (0, 255, 0) # BGR
                                        point_color = (255, 255, 0) # BGR rear

                                        thickness = 8 # 

                                       
                                        cv2.circle(img, (x_coordinate, y_coordinate), point_size, point_color, thickness)
                                        save_save_path_last = save_save_path + file_name
                                        cv2.imwrite(save_save_path_last, img)
                          

 
        

                                



                            

                          

                          


                                




                



        
        
         
