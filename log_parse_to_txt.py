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

def check_num(phy_x, phy_y, img_x, img_y):

    min_x = 3.
    max_x = 3.6
    min_y = 3. + 1e-8
    max_y = 5.
    second_max_y = 1.5
    
    if(phy_x > -min_x and phy_x < min_x and phy_y < min_y):
        return False

    if(phy_x > max_x or phy_x < -max_x or phy_y > max_y):
        return False

    if(phy_x >= min_x and phy_x < max_x and phy_y < second_max_y):
            return False

    if(phy_x <= -min_x and phy_x > -max_x and phy_y < second_max_y):
            return False

    return True


def num_split_log(line):
        

    list_num = line.split(" ")
    if(len(list_num) <= 1):
            return False
    frame_id = list_num[0][1: -1]
    phy_x = float(list_num[2][1:]) # delete [
    phy_y = float(list_num[3][:-1])

    img_x = float(list_num[8][1:]) # delete [
    img_y = float(list_num[9][:-1])

  
    return frame_id, phy_x, phy_y, img_x, img_y

def front_rear_img_log(line):
        
    front_rear_list = list()
    list_num = line.split(" ")
    if(len(list_num) <= 1):
            return False
    frame_id = list_num[0][1: -1]

    front_phy_x = float(list_num[2][1:]) # delete [
    front_phy_y = float(list_num[3][:-1])
    rear_phy_x = float(list_num[4][1:]) # delete [
    rear_phy_y = float(list_num[5][:-1])

    front_img_x = float(list_num[8][1:]) # delete [
    front_img_y = float(list_num[9][:-1])

    rear_img_x = float(list_num[10][1:]) # delete [
    rear_img_y = float(list_num[11][:-1])

  
    return frame_id, front_img_x, front_img_y, rear_img_x, rear_img_y 

def front_rear_phy_log(line):
        
    front_rear_list = list()
    list_num = line.split(" ")
    if(len(list_num) <= 1):
            return False
    frame_id = list_num[0][1: -1]

    front_phy_x = float(list_num[2][1:]) # delete [
    front_phy_y = float(list_num[3][:-1])
    rear_phy_x = float(list_num[4][1:]) # delete [
    rear_phy_y = float(list_num[5][:-1])

    front_img_x = float(list_num[8][1:]) # delete [
    front_img_y = float(list_num[9][:-1])

    rear_img_x = float(list_num[10][1:]) # delete [
    rear_img_y = float(list_num[11][:-1])
  
    return frame_id, front_phy_x, front_phy_y, rear_phy_x, rear_phy_y

def judge_front_rear_log(line):
        
    front_rear_list = list()
    list_num = line.split(" ")
    if(len(list_num) <= 1):
            return False
    frame_id = list_num[0][1: -1]
    front_phy_x = float(list_num[2][1:]) # delete [
    front_phy_y = float(list_num[3][:-1])

    rear_phy_x = float(list_num[4][1:]) # delete [
    rear_phy_y = float(list_num[5][:-1])

    #front_rear_list = [front_phy_x, front_phy_y, rear_phy_x,rear_phy_y]
    front_rear_list = [rear_phy_x,rear_phy_y]

    return front_rear_list
  

def num_split_csv(line):
        

    list_num = line.split(" ")
    if(len(list_num) <= 1):
            return False
    frame_id = list_num[0][1: -1]
    phy_x = float(list_num[2][1:]) # delete [
    phy_y = float(list_num[3][:-1])

    img_x = float(list_num[8][1:]) # delete [
    img_y = float(list_num[9][:-1])

  
    #return frame_id, phy_x, phy_y, img_x, img_y
    return frame_id, img_x, img_y

def check_channel(line, channel):
        list_num = line.split(" ")
        if(len(list_num) <= 1):
            return False
        # delete []
        channel_id = str(list_num[1][1: -1])
        if(channel == channel_id):
                return True
        else:
                return False


def get_frame_id(log_data_dict,csv_data_dict):

        frame_id_dict = {}
        for key, value in csv_data_dict.items():
                #check key in 2 data
                if key not in log_data_dict.keys():
                        continue

                [real_x,real_y] = csv_data_dict[key]
                frame_id_dict["{}".format(key)] = [real_x, real_y]

        return frame_id_dict

def get_frame_id_and_phy(log_data_dict,csv_data_dict):


        frame_id_dict = {}
        for key, value in log_data_dict.items():
                #check key in 2 data
                if key not in csv_data_dict.keys():
                        continue

                [real_x,real_y] = csv_data_dict[key]
                frame_id_dict["{}".format(key)] = [real_x, real_y]      

        return frame_id_dict

def get_frame_id_and_img(log_data_dict,csv_data_dict):


        frame_id_img_dict = {}
        frame_id_phy_dict = {}
        for key, value in log_data_dict.items():
                #check key in 2 data
                if key not in csv_data_dict.keys():
                        continue

                [img_x,img_y] = log_data_dict[key]
                frame_id_img_dict["{}".format(key)] = [img_x,img_y]   

                [real_x,real_y] = csv_data_dict[key]
                frame_id_phy_dict["{}".format(key)] = [real_x,real_y]      

        return frame_id_img_dict, frame_id_phy_dict


def phy_coordinate_filter(phy_data):
        
    min_x = 3.
    max_x = 3.6
    min_y = 3. + 1e-8
    max_y = 5.
    second_max_y = 1.5

    phy_x = phy_data[0]
    phy_y = phy_data[1]
    
    if(phy_x > -min_x and phy_x < min_x and phy_y < min_y):
        return False

    if(phy_x > max_x or phy_x < -max_x or phy_y > max_y):
        return False

    if(phy_x >= min_x and phy_x < max_x and phy_y < second_max_y):
            return False

    if(phy_x <= -min_x and phy_x > -max_x and phy_y < second_max_y):
            return False

    return True

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

def write_data_to_txt_add_frame_id(save_img_file_path, save_frame_id_file_path, write_data): # (save_img_file_path, save_frame_id_file_path,phy_img_data

        file_write = open(save_img_file_path,"w+")
        frame_id_file_write = open(save_frame_id_file_path,"w+")

        for index, value in enumerate(write_data):

                phy_coordinate = value[0]
                img_coordinate = value[1]
                frame_id = str(value[-1])

                #roi filter
                flag = phy_coordinate_filter(phy_coordinate)
                if(flag == False):
                        continue

                phy_x = str(phy_coordinate[0])
                phy_y = str(phy_coordinate[1])
                img_x = str(img_coordinate[0])
                img_y = str(img_coordinate[1])
                write_line = '[' + phy_x + ',' + phy_y + ']' + ' ' \
                        '[' + img_x + ',' + img_y + ']' +  '\n'

                write_line_frame_id =  frame_id + '\n'
               
                file_write.write(write_line)
                frame_id_file_write.write(write_line_frame_id)

        file_write.close()
        frame_id_file_write.close()

def write_data_to_csv(file_name, write_data,file_head):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        #file_head = ['rtk_x', 'rtk_y', 'img_phy_x', 'img_phy_y']

        targetWriter.writerow(file_head)

        for index, write_data_row in enumerate(write_data):

                phy_coordinate = write_data_row[0]
                img_coordinate = write_data_row[-1]

                #roi filter
                # flag = phy_coordinate_filter(phy_coordinate)
                # if(flag == False):
                #         continue

                phy_x = phy_coordinate[0]
                phy_y = phy_coordinate[1]
                img_x = img_coordinate[0]
                img_y = img_coordinate[1]

                
                out_data = [img_x,img_y,phy_x, phy_y]
                targetWriter.writerow(out_data)

        outFile.close()

def write_data_to_csv_short(file_name, write_data,file_head):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)

        targetWriter.writerow(file_head)

        #for index, write_data_row in enumerate(write_data):
        for key,value in write_data.items():

                front_img_x = value[0]
                front_img_y = value[1]
                rear_img_x = value[2]
                rear_img_y = value[3]

                out_data = [key,front_img_x,front_img_y,rear_img_x,rear_img_y]
                targetWriter.writerow(out_data)

        outFile.close()



def log_process(file_path_all, channel_id):
        
        frame_id = "frame_id"
        channel = channel_id
 
        log_data_img_dict = dict()
        log_data_phy_dict = dict()
 
        with open(file_path_all, 'r') as file_read:
                while True:

                        line = file_read.readline() 

                        if not line:
                                break
                        # 1.judge channel_id
                        channel_flag  = check_channel(line, channel)
                        if(channel_flag == False):
                                continue
                        # 2. parse string
                        frame_id, front_img_x, front_img_y, rear_img_x, rear_img_y = front_rear_img_log(line)
                        frame_id, front_phy_x, front_phy_y, rear_phy_x, rear_phy_y = front_rear_phy_log(line)

                        #frame_id,img_x_detection,img_y_detection = num_split_log(line)
                        # 3.judge image coordinate == 0
                        if front_img_x == 0 and front_img_y == 0:
                                continue
                        # # 4. judge only one point
                        # front_rear_list = judge_front_rear_log(line)
                        # if front_rear_list[0] == 0 and front_rear_list[1] == 0:
                        #         continue

                        log_data_img_dict["{}".format(frame_id)] = [front_img_x, front_img_y, rear_img_x, rear_img_y]
                        log_data_phy_dict["{}".format(frame_id)] = [front_phy_x, front_phy_y, rear_phy_x, rear_phy_y]

        file_read.close()

        return log_data_img_dict, log_data_phy_dict


        
if __name__ == "__main__":

        src_log_path = "/home/xieyi/pic/zadas_tjp_01_data/tjp_car_capture2.log"
        img_csv_path = "/home/xieyi/pic/zadas_tjp_01_data/capture2_img.csv"
        phy_csv_path = "/home/xieyi/pic/zadas_tjp_01_data/capture2_phy.csv"
        channel_id = "front"

        img_file_head = ['frame_id',  'img_x_front', 'img_y_front','img_x_rear', 'img_y_rear']
        log_data_img_dict, log_data_phy_dict = log_process(src_log_path, channel_id)
        write_data_to_csv_short(img_csv_path, log_data_img_dict,img_file_head)

        img_file_head = ['frame_id',  'phy_x_front', 'phy_y_front','phy_x_rear', 'phy_y_rear']
        write_data_to_csv_short(phy_csv_path, log_data_phy_dict,img_file_head)



     

        
        
         
