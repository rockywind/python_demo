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
        #file_head = ['frame_id', 'phy_x','phy_y']

        #targetWriter.writerow(file_head)
        first_line_flag = True
        for index, write_data_row in enumerate(write_data):

               
                out_data = write_data_row
                targetWriter.writerow(out_data)

        outFile.close()

                        


        
if __name__ == "__main__":
        
        # x_key = 'pos_FRTire_x'
        # y_key = 'pos_FRTire_y'
        frame_id = 'frame_id'

     

        src_img_path = '/media/xieyi/Elements/zwk/20190704/rtk_video_det/capture_1_frontoutput/capture1_img_draw/'
        src_txt_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_0-9100.txt'
        save_image_path = '/media/xieyi/Elements/zwk/20190704/rtk_video_det/capure_1_draw_img_select/'
        
        mkdir(save_image_path)


        with open(src_txt_path, 'r') as file_read:
                while True:

                        line_ori = file_read.readline() 
                        
                        if not line_ori:
                                break
                        line_tmp = line_ori.split(" ")

                        line_del = line_tmp[0][1:-1]
                        
                        img_name = 'tjp' + '_' + str(line_del) + '.bmp'
                        #img_name = 'tjp' + '_' + str(7571) + '.bmp'
                        img_path = src_img_path + img_name

                        if(os.path.isfile(img_path) == False):
                                continue

                        save_img_path = save_image_path + img_name
                        img = cv2.imread(img_path)
                        # if(img.() == None):
                        #         print("----img error---")
                        #         continue
                        cv2.imwrite(save_img_path, img)

                                
       

        

                                



                            

                          

                          


                                




                



        
        
         
