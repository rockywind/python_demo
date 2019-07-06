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
        file_head = ['rtk_x', 'rtk_y', 'img_phy_x', 'img_phy_y']

        targetWriter.writerow(file_head)

        for index, write_data_row in enumerate(write_data):

                phy_coordinate = write_data_row[0]
                img_coordinate = write_data_row[-1]


                phy_x = phy_coordinate[0]
                phy_y = phy_coordinate[1]
                img_x = img_coordinate[0]
                img_y = img_coordinate[1]

                
                out_data = [phy_x, phy_y,img_x,img_y]
                targetWriter.writerow(out_data)

        outFile.close()

                        
def parse_data(phy_img_data):

         label_data_ori = np.array(phy_img_data)[:,0,:]
         label_data = label_data_ori * 100
         img_phy_data = np.array(phy_img_data)[:,1,:]

         return label_data, img_phy_data




        
if __name__ == "__main__":
        
        src_txt_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label5/'

        src_det_path = '/home/xieyi/pic/zadas_tjp_01_data/rtk_100hz_0629/tjp_front/'
        src_output_path = '/home/xieyi/pic/zadas_tjp_01_data/rtk_100hz_0629/tjp_frontoutput/'

        save_output_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label5/output/'
        mkdir(save_output_path)
        save_det_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label5/det/'
        mkdir(save_det_path)

        file_suffix = "id.txt"
        for file_name in os.listdir(src_txt_path):

                if len(file_name.split(file_suffix)) <= 1:
                        continue

                src_txt_name = src_txt_path + file_name

                with open(src_txt_name, 'r') as file_read:
                        while True:

                                line_ori = file_read.readline() 
                                line = line_ori[:-1]
                                if not line:
                                        break
                                # det
                                det_img_name = src_det_path + 'tjp_' + str(line) + '.bmp'
                                det_save_img_name = save_det_path + 'tjp_' + str(line) + '.bmp'
                                img = cv2.imread(det_img_name)
                                cv2.imwrite(det_save_img_name, img)
                                # output point
                                output_img_name = src_output_path + 'tjp_' + str(line) + '.bmp'
                                output_save_img_name = save_output_path + 'tjp_' + str(line) + '.bmp'
                                img = cv2.imread(output_img_name)
                                cv2.imwrite(output_save_img_name, img)




                    

   
    


        
        
         
