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




def write_data_to_csv(file_name, write_data):

       
        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        file_head = ['frame_id', 'phy_x','phy_y']

        targetWriter.writerow(file_head)

        for index, write_data_row in enumerate(write_data):

                out_data = write_data_row
                targetWriter.writerow(out_data)

        outFile.close()

def read_csv(csv_path):

        csv_data_dict = dict()
        with open(csv_path) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):

                        if(i == 0):
                                continue

                        frame_id_str = rows[0]
                        
                        channel_id = rows[1]
                        phy_x = rows[2]
                        phy_y = rows[3]

                        csv_data_dict["{}".format(frame_id_str)] = [frame_id_str, channel_id, phy_x, phy_y]


        csvfile.close()
        return csv_data_dict

def sortedDictValues2(file_name, file_head,dict_data_input):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)

        targetWriter.writerow(file_head)
      
        list_data= sorted(dict_data_input.items(), key=lambda d:d[1], reverse = False)
        for index,value in enumerate(list_data):

                targetWriter.writerow(value[1][:])   
                
        outFile.close()
        return list_data


def filter_y_value(dict_data):

        y_max = 500
        write_data = {}
    
        for key, value in dict_data.items():
                csv_data = dict_data[key]
                if(float(csv_data[-1]) > y_max or float(csv_data[-1])< -y_max):
                       continue
                
                all_data = csv_data
                write_data["{}".format(key)] = all_data 

        return write_data

def filter_frame_id(dict_data):
        is_save = True
        write_data = {}
        frame_id_min = [14662,15170, 15766, 16313, 16729, 17139]
        frame_id_max = [14749,15274, 15878, 16368, 16788, 17192]
        for key, value in dict_data.items():
                csv_data = dict_data[key]
                for i in range(6):
                        if(int(csv_data[0]) > frame_id_min[i] and int(csv_data[0])< frame_id_max[i]):
                                is_save = False
                                break
                if(is_save):
                        all_data = csv_data
                        write_data["{}".format(key)] = all_data 
                is_save = True
  

        return write_data

def filter_zero_point(dict_data):
        write_data_list = []
        list_data= sorted(dict_data_input.items(), key=lambda d:d[1], reverse = False)
        for index,value in enumerate(list_data):
                if(index>1 and index<len(list_data)-2 and float(list_data[index+1][1][2]) == 0. and float(list_data[index-1][1][2])==0. and float(list_data[index][1][2])!=0.):
                        continue

                if(index>1 and index<len(list_data)-2 and float(list_data[index+1][1][2]) != 0. and float(list_data[index-1][1][2])!=0. and float(list_data[index][1][2])==0. and index>1 and index<len(list_data)-2):
                        continue
                write_data_list.append(value[1][:])

        return write_data_list

def write_list_data_to_csv(file_name, file_head,list_data_input):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        targetWriter.writerow(file_head)
        for index,value in enumerate(list_data_input):

                #targetWriter.writerow(value[1]) 
                targetWriter.writerow(value)  
                
        outFile.close()

# def del_duplicate_zero():

#         write_data_list = []
#         list_data= sorted(dict_data_input.items(), key=lambda d:d[1], reverse = False)
#         for index,value in enumerate(list_data):
#                 if(index>1 and index<len(list_data)-2 and float(list_data[index+1][1][2]) == 0. and float(list_data[index-1][1][2])==0. and float(list_data[index][1][2])!=0.):
#                         continue

#                 if(index>1 and index<len(list_data)-2 and float(list_data[index+1][1][2]) != 0. and float(list_data[index-1][1][2])!=0. and float(list_data[index][1][2])==0. and index>1 and index<len(list_data)-2):
#                         continue
#                 write_data_list.append(value[1][:])

#         return write_data_list


               






                     
        
if __name__ == "__main__":
        

        #src_csv_path = '/home/xieyi/save_img/img_12/output_12_260_02.csv'
        #save_csv_path = '/home/xieyi/save_img/img_12/output_12_260_02_del5m_02_01.csv'
        # src_csv_path = '/home/xieyi/save_img/img_12/output_y=10_02.csv'
        # save_csv_path = '/home/xieyi/save_img/img_12/output_y=10_02_filter.csv'

        src_csv_path = '/home/xieyi/save_img/img_12/output_y=260_05_ori.csv'
        save_csv_path = '/home/xieyi/save_img/img_12/output_y=260_05_del5m.csv'


        file_head = ['frame_id',  'channel', 'phy_x','phy_y']
        front_csv_data_dict = read_csv(src_csv_path)
        dict_data_input = filter_y_value(front_csv_data_dict)
        sortedDictValues2(save_csv_path, file_head, dict_data_input)


        # dict_data_filter = filter_frame_id(dict_data_input)
        # dict_data_filter_zero = filter_zero_point(dict_data_filter)
        # write_list_data_to_csv(save_csv_path, file_head,dict_data_filter_zero)
        #sortedDictValues2(save_csv_path, file_head,dict_data_filter)


       


                            

                          

                          


                                




                



        
        
         
