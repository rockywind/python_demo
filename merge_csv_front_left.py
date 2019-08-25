#!/usr/bin/python
# -*- coding: <encoding name> -*-
import numpy as np
import os
import scipy.misc as sm
import cv2
import csv

import codecs

import matplotlib.pyplot as plt

x_key = 'pos_FLTire_x'
y_key = 'pos_FLTire_y'

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'

def read_csv(csv_path):

        #frame_id = "frame_id"
        csv_data_dict = dict()

        x_index = 1
        y_index = 2
        with open(csv_path) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):
                       
                        frame_id_str = rows[0]
                        
                        channel_id = rows[1]
                        phy_x = rows[2]
                        phy_y = rows[3]

                 

                        csv_data_dict["{}".format(frame_id_str)] = [frame_id_str, channel_id, phy_x, phy_y]


        csvfile.close()
        return csv_data_dict

def read_txt(file_path_all):
        
        txt_data_dict = dict()
        txt_value = list()

        with open(file_path_all, 'r') as file_read:
                while True:

                        line = file_read.readline() 

                        if not line:
                                break

                        line_ori = line.split(" ")
                        frame_id = line_ori[0]
                        txt_value = list()
                        for index, value in enumerate(line_ori):

                                if(value == '\n'):
                                        continue
                                txt_value.append(value)

                        if(len(line_ori)>=6):

                                vel = (float(line_ori[3]) +float(line_ori[6]))*0.5

                        txt_value.append(vel)
                        txt_data_dict["{}".format(frame_id)] = txt_value

        file_read.close()

        return txt_data_dict

def merge_data(csv_data_dict, txt_data_dict):

        write_data = {}
        write_data_one = {}
        none_data = [',',',',',',',',',',',',',']
        for key, value in txt_data_dict.items():

               if key not in csv_data_dict.keys():
                        continue
               
               csv_data = csv_data_dict[key]
               if(len(value)<=2):
                       value.extend(none_data)
               all_data = value
               all_data.extend(csv_data)

               write_data["{}".format(key)] = all_data     

            
        return write_data

def merge_csv_data(front_csv_data_dict, left_csv_data_dict):
        #y_max = 500
        y_max = 1000
        y_secnd_max = 260
        #y_secnd_max = 10
        x_max = 500
        write_data = {}
        write_data_one = {}
        none_data = [',',',',',',',',',',',',',']
        for key, value in front_csv_data_dict.items():

               #if key not in left_csv_data_dict.keys():
                        #continue
               
               csv_data = front_csv_data_dict[key]
               # 1. y_max> 5m
               if(float(csv_data[-1]) > y_max or float(csv_data[-1])< 0):
                       continue
               # 2. y_max_sec > 2.6 front
               if(float(csv_data[-1]) > y_secnd_max):
                       all_data = csv_data
                       
               # 3. y_max_sec > 2.6 left
               if(float(csv_data[-1]) <= y_secnd_max):
                       if key  in left_csv_data_dict.keys():
                               csv_left_data = left_csv_data_dict[key]
                               if(float(csv_left_data[-1]) <= y_secnd_max):
                                       all_data = csv_left_data

                       else: # left data not exist,assign front data
                                all_data = csv_data

                # 4. -500<x<500
               if(float(all_data[2]) > x_max or float(all_data[2]) < -x_max):
                       continue

                  


               write_data["{}".format(key)] = all_data     
                       
                      
        #        #if(csv_data[])
        #        if(len(value)<=2):
        #                value.extend(none_data)
        #        all_data = value
        #        all_data.extend(csv_data)

        #        write_data["{}".format(key)] = all_data     

            
        return write_data




def sortedDictValues2(file_name, file_head,dict_data_input):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        #file_head = ['rtk_x', 'rtk_y', 'img_phy_x', 'img_phy_y']

        targetWriter.writerow(file_head)
        #txt_data_dict = sorted(write_data.items(), key=lambda d:d[0]) 


        # for key, value in write_data.items():


        #         frame_id = key
        #         value.insert(0, key)
        #         #out_data = [img_x,img_y,phy_x, phy_y]
        #         targetWriter.writerow(value)

      
        list_data= sorted(dict_data_input.items(), key=lambda d:d[1], reverse = False)
        for index,value in enumerate(list_data):

                targetWriter.writerow(value[1][:])   
                
        outFile.close()
        return list_data
        #return [adict[key] for key in keys] 

def write_data_to_csv_ori(file_name, write_data,file_head):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        #file_head = ['rtk_x', 'rtk_y', 'img_phy_x', 'img_phy_y']

        targetWriter.writerow(file_head)
        txt_data_dict = sorted(write_data.items(), key=lambda d:d[0]) 

        #for index, write_data_row in enumerate(write_data):
        #for key, value in txt_data_dict.items():
        for key, value in write_data.items():


                frame_id = key
                value.insert(0, key)
                #out_data = [img_x,img_y,phy_x, phy_y]
                targetWriter.writerow(value)

        outFile.close()

def write_data_to_csv(file_name, write_data,file_head):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        #file_head = ['rtk_x', 'rtk_y', 'img_phy_x', 'img_phy_y']

        targetWriter.writerow(file_head)
        txt_data_dict = sorted(write_data.items(), key=lambda d:d[0]) 

        #for index, write_data_row in enumerate(write_data):
        #for key, value in txt_data_dict.items():
        for key, value in write_data.items():


                #out_data = [img_x,img_y,phy_x, phy_y]
                targetWriter.writerow(value)

        outFile.close()
               




        
if __name__ == "__main__":

    
        # front_csv_path = "/home/xieyi/02_zadas_code/python_demo/01_data/tjp_OBDcar_front_25.csv"
        # left_csv_path = "/home/xieyi/02_zadas_code/python_demo/01_data/tjp_OBDcar_left_25.csv"
        # save_csv_path = "/home/xieyi/02_zadas_code/python_demo/01_data//output.csv"
        front_csv_path = "/home/xieyi/save_img/img_12/tjp_OBDcar_front.csv"
        left_csv_path = "/home/xieyi/save_img/img_12/tjp_OBDcar_left.csv"
        save_csv_path = "/home/xieyi/save_img/img_12/output.csv"
        file_head = ['frame_id',  'channel', 'phy_x','phy_y']
        front_csv_data_dict = read_csv(front_csv_path)
        left_csv_data_dict = read_csv(left_csv_path)
        
        write_data = merge_csv_data(front_csv_data_dict, left_csv_data_dict)
        sortedDictValues2(save_csv_path, file_head,write_data)
        #write_data_to_csv(save_csv_path, write_data,file_head)
        # sortedDictValues2(save_csv_path, file_head,write_data)


        # front_csv_path = "/home/xieyi/01_python_code/test/0705_bp_save_rand.csv"
        # src_txt_path = "/home/xieyi/01_python_code/test/0705_bp_output_CV.txt"
        # save_csv_path = "/home/xieyi/01_python_code/test/output.csv"
        # file_head = ['frame_id',  '1', '2','3', '4','5','6','7','north_dist','target_dist']
        # csv_data_dict = read_csv(src_csv_path)
        # txt_data_dict = read_txt(src_txt_path)
        # write_data = merge_data(csv_data_dict, txt_data_dict)
        # sortedDictValues2(save_csv_path, file_head,write_data)

        # write_data_sort_by_key = sortedDictValues2(write_data)
        # write_data_to_csv(save_csv_path, write_data_sort_by_key,file_head)





        

       



     

        
        
         
