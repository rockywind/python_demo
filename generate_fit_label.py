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

                # phy_coordinate = write_data_row[0]
                # img_coordinate = write_data_row[-1]


                # phy_x = phy_coordinate[0]
                # phy_y = phy_coordinate[1]
                # img_x = img_coordinate[0]
                # img_y = img_coordinate[1]

                
                # out_data = [phy_x, phy_y,img_x,img_y]
                out_data = write_data_row
                targetWriter.writerow(out_data)

        outFile.close()

                        


        
if __name__ == "__main__":
        
        # x_key = 'pos_FRTire_x'
        # y_key = 'pos_FRTire_y'

        x_key = 'pos_FLTire_x'
        y_key = 'pos_FLTire_y'

        # src_img_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/img_select/'
        # src_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/out_final.csv'
        # save_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/img_select.csv'

        src_img_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/0002_rtk_50hz/output/'
        src_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190704_rtk_100hz/img_draw_select.csv'
        src_txt_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190704_rtk_100hz/tjp_img_select_label.txt'

        save_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/img_select.csv'
        #mkdir(src_csv_path)

        write_data = list()

        file_suffix = ".bmp"
        for file_name in os.listdir(src_img_path):

                if len(file_name.split(file_suffix))<=1:
                        continue

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
                                        line_ori_tmp = line_ori.split(",")
                                        for index, value in enumerate(line_ori_tmp):
                                                if x_key == value:
                                                        x_index = index
                                                if y_key == value:
                                                        y_index = index
                
                                        continue

                                line_del = line_ori[:-1]
                                line = line_del.split(",")
                                img_id_tmp = line[0].split(".")
                                img_id = img_id_tmp[0]

                                if(img_id == frame_id):
                                        # x_coordinate_str = line[16]
                                        # y_coordinate_str = line[17]

                                        x_coordinate_str = line[x_index]
                                        y_coordinate_str = line[y_index]

                                        x_coordinate = float(x_coordinate_str)*100
                                        y_coordinate = float(y_coordinate_str)*100

                                        write_data_row = [frame_id, x_coordinate, y_coordinate]
                                        write_data.append(write_data_row)

        write_data_to_csv(save_csv_path, write_data)
        

                                



                            

                          

                          


                                




                



        
        
         
