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

        frame_id = "frame_id"
        csv_data_dict = dict()

        x_index = 1
        y_index = 2
        with open(csv_path) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):
                       

                        frame_id_str = rows[0]
                        frame_id = frame_id_str.split('.')[0]
                        north_vx = float(rows[24])
                        north_vy = float(rows[25])

                        north_dist = np.sqrt((north_vx*north_vx + north_vy*north_vy))

                        target_vx = float(rows[26])
                        target_vy = float(rows[27])

                        target_dist = np.sqrt(target_vx*target_vx + target_vy*target_vy)

                        csv_data_dict["{}".format(frame_id)] = [str(north_dist), str(target_dist)]


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

def write_data_to_csv(file_name, write_data,file_head):

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
               




        
if __name__ == "__main__":

    
        src_csv_path = "/home/xieyi/01_python_code/test/0705_bp_save_rand.csv"
        src_txt_path = "/home/xieyi/01_python_code/test/0705_bp_output_CV.txt"
        save_csv_path = "/home/xieyi/01_python_code/test/output.csv"
        file_head = ['frame_id',  '1', '2','3', '4','5','6','7','north_dist','target_dist']
        csv_data_dict = read_csv(src_csv_path)
        txt_data_dict = read_txt(src_txt_path)
        write_data = merge_data(csv_data_dict, txt_data_dict)
        sortedDictValues2(save_csv_path, file_head,write_data)

        # write_data_sort_by_key = sortedDictValues2(write_data)
        # write_data_to_csv(save_csv_path, write_data_sort_by_key,file_head)





        

       



     

        
        
         
