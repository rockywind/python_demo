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
                    
def read_csv(csv_path):

        frame_id = "frame_id"
        csv_data_dict = dict()
        #x_key = 'pos_FRTire_x'
        #y_key = 'pos_FRTire_y'
        #with open(file_path_all,encoding='utf-8') as csvfile:
        x_index = 1
        y_index = 2
        with open(csv_path) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):
                        # skip first row and get the index
                        if(i < 1):
                                # for index, value in enumerate(rows):
                                #         if x_key == value:
                                #                 x_index = index
                                #         if y_key == value:
                                #                 y_index = index
                                continue

                        frame_id_str = rows[0]
                        frame_id = frame_id_str.split('.')[0]
                       
                        # real_x = float(rows[x_index])
                        # real_y = float(rows[y_index])

                        real_x = float(rows[x_index])
                        real_y = float(rows[y_index])

                        csv_data_dict["{}".format(frame_id)] = [real_x, real_y]
       
        return csv_data_dict

def read_csv_acroding_key(csv_path,x_key,y_key):

        frame_id = "img_id"
        csv_data_dict = dict()
        #x_key = 'pos_FRTire_x'
        #y_key = 'pos_FRTire_y'
        #with open(file_path_all,encoding='utf-8') as csvfile:
        # front right
        # x_index = 16
        # y_index = 17

        # # front right
   
        with open(csv_path) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):
                        # skip first row and get the index
                        if(i < 1):
                                for index, value in enumerate(rows):
                                        if x_key == value:
                                                x_index = index
                                        if y_key == value:
                                                y_index = index
                                continue

                        frame_id_str = rows[0]
                        frame_id = frame_id_str.split('.')[0]
                       
                        # real_x = float(rows[x_index])
                        # real_y = float(rows[y_index])

                        real_x = float(rows[x_index])*100
                        real_y = float(rows[y_index])*100

                        csv_data_dict["{}".format(frame_id)] = [real_x, real_y]
       
        return csv_data_dict

def write_data_to_csv(file_name, write_data, file_head):

       
        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        
        targetWriter.writerow(file_head)

        #for index, write_data_row in enumerate(write_data):
        for key, value in write_data.items():


                out_data = [key, value[0],value[1],value[2],value[3]]
                targetWriter.writerow(out_data)

        outFile.close()

def filter_roi(phy_rtk_x, phy_rtk_y):
        y_max = 500.0
        if(phy_rtk_y> y_max):
                return False
        else:
                return True

def generate_write_data(phy_img_dict, phy_rtk_dict):

        write_data_dict = {}

        for key, value in phy_img_dict.items():

                #check key in 2 data
                if key not in phy_rtk_dict.keys():
                        continue

                [img_to_phy_x, img_to_phy_y] = phy_img_dict[key]
                [phy_rtk_x, phy_rtk_y] = phy_rtk_dict[key]

                # roi filter
                flag = filter_roi(phy_rtk_x, phy_rtk_y)
                if(flag == False):
                        continue

                write_data_dict["{}".format(key)] = [phy_rtk_x, phy_rtk_y, img_to_phy_x, img_to_phy_y]

        return write_data_dict


      
if __name__ == "__main__":
        
        # x_key = 'pos_FRTire_x'
        # y_key = 'pos_FRTire_y'

        x_key = 'pos_RRTire_x'
        y_key = 'pos_RRTire_y'

        #img_id = 'img_id'

        phy_rtk_dict = {}
        phy_img_dict = {}
        write_data_dict = {}

        # src_phy_img_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_phy.csv'
        # src_rtk_csv_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/out_final_utm.csv'

        # save_file_name = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/img_to_phy_and_rtk.csv'

        
        # src_phy_img_csv_path =  '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_front_phy.csv'
        # src_rtk_csv_path =  '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/capture_01_front_phy.csv'

        # save_file_name = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/img_to_phy_and_label_front.csv'

        
        src_phy_img_csv_path =  '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_front_phy.csv'
        src_rtk_csv_path =  '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/capture_01_front_phy.csv'

        save_file_name = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/img_to_phy_and_label_front.csv'
        #mkdir(save_save_path)

        phy_img_dict = read_csv(src_phy_img_csv_path)
     
        phy_rtk_dict = read_csv_acroding_key(src_rtk_csv_path, x_key,y_key)


        write_data_dict = generate_write_data(phy_img_dict, phy_rtk_dict)

        #write_data_head = ['frame_id', 'phy_rtk_x', 'phy_rtk_y', 'img_to_phy_x', 'img_to_phy_y']
        write_data_head = ['frame_id', 'phy_rtk_x', 'phy_rtk_y', 'img_to_phy_x', 'img_to_phy_y']

        write_data_to_csv(save_file_name, write_data_dict, write_data_head)
        

                

        


       

 
        

                                



                            

                          

                          


                                




                



        
        
         
