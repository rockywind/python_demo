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
        file_head = ['cam_x','cam_y', 'phy_x','phy_y','real_x','real_y', 'error_phy_x','error_phy_y','error_phy_dist',\
                     'cam_new_x','cam_new_y','error_pix_x','error_pix_y','frame_id']

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
        
        #src_txt_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0001_ori_new/'
        #save_csv_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0001_ori_new/new.csv'
        src_txt_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0703/'
        save_csv_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0703/0001.csv'
        #mkdir(src_csv_path)

        write_data = list()

        file_suffix = ".txt"
        for file_name in os.listdir(src_txt_path):

                if len(file_name.split(file_suffix))<=1:
                        continue

                src_txt_name = src_txt_path + file_name
                #save_csv_path = src_txt_path + file_name
                with open(src_txt_name, 'r') as file_read:
                        while True:

                                line_ori = file_read.readline() 
                                
                                if not line_ori:
                                        break

                                line_del = line_ori[:-1]
                                line = line_del.split(", ")

                                cam_data_tmp = line[0]
                                cam_data = cam_data_tmp.split(",")
                                cam_x = cam_data[0].split("[")[-1]
                                cam_y = cam_data[-1][:-1]

                                phy_data_tmp = line[1]
                                phy_data = phy_data_tmp.split(",")
                                phy_x = phy_data[0].split("[")[-1]
                                phy_y = phy_data[-1][:-1]

                                real_data_tmp = line[2]
                                real_data = real_data_tmp.split(",")
                                real_x = real_data[0].split("[")[-1]
                                real_y = real_data[-1][:-1]

                                error_phy_tmp = line[3]
                                error_phy_data = error_phy_tmp.split(",")
                                error_phy_x = error_phy_data[0].split("[")[-1]
                                error_phy_y = error_phy_data[1]
                                error_phy_dist = error_phy_data[-1][:-1]

                                cam_new_tmp = line[4]
                                cam_new_data = cam_new_tmp.split(",")
                                cam_new_x = cam_new_data[0].split("[")[-1]
                                cam_new_y = cam_new_data[-1][:-1]

                                error_pix_tmp = line[5]
                                error_pix_data = error_pix_tmp.split(",")
                                error_pix_x = error_pix_data[0].split("[")[-1]
                                error_pix_y = error_pix_data[-1][:-1]

                                frame_id_tmp = line[-1]
                                frame_id = frame_id_tmp.split("[")[-1][:-1]

                                write_data_row = [cam_x,cam_y, phy_x,phy_y, real_x,real_y, error_phy_x,error_phy_y,error_phy_dist, cam_new_x,cam_new_y, \
                                        error_pix_x, error_pix_y,frame_id]

                                write_data.append(write_data_row)




                
        #write_data_to_txt(save_phy_file_path, phy_img_phy_data)
        write_data_to_csv(save_csv_path, write_data)

        #label_data, img_phy_data = parse_data(phy_img_data)
        #plot_data(label_data, img_phy_data, save_file_path)


        
        
         
