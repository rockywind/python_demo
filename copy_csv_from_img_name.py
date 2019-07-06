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

     

        # src_img_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190704_rtk_100hz/img_draw_select/'
        # src_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190704_rtk_100hz/out_final.csv'
        # save_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190704_rtk_100hz/img_draw_select.csv'

        src_img_path = '/media/xieyi/Elements/zwk/20190704/rtk_video_det/20190606_capture1_select_01/'
        src_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/img_to_phy_and_rtk.csv'
        save_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/img_to_phy_and_rtk_01.csv'

       

        write_data = list()

        file_suffix = ".bmp"
        first_line_flag = True
        for file_name in os.listdir(src_img_path):

                if len(file_name.split(file_suffix))<=1:
                        continue

                frame_id_tmp = file_name.split(".")
                frame_id = frame_id_tmp[0].split("_")[-1]

               

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
                                        line_ori = line_ori.split(",")
                                        write_data.append(line_ori)
                                     
                                        continue

                                line_del = line_ori[:-1]
                                line = line_del.split(",")
                                img_id_tmp = line[0].split(".")
                                img_id = img_id_tmp[0]

                                if(img_id == frame_id):
                                    
                                        line_ori_tmp = line_ori.split(",")
                                        line_ori = line_ori_tmp
                                        write_data.append(line_ori)
                                        

        write_data_to_csv(save_csv_path, write_data)
        

                                



                            

                          

                          


                                




                



        
        
         
