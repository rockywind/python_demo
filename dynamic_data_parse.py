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
    #return frame_id, img_x, img_y
    #return frame_id, phy_x, phy_y

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

def log_process(file_path_all, channel_id):
        
        frame_id = "frame_id"
        channel = channel_id
 
        log_data_dict = dict()
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
                        frame_id, phy_x_detection, phy_y_detection,img_x_detection,img_y_detection = num_split_log(line)
                        #frame_id,img_x_detection,img_y_detection = num_split_log(line)
                        # 3.judge image coordinate == 0
                        if img_x_detection == 0 and img_y_detection == 0:
                                continue
                        # # 4. judge only one point
                        # front_rear_list = judge_front_rear_log(line)
                        # if front_rear_list[0] == 0 and front_rear_list[1] == 0:
                        #         continue

                        log_data_dict["{}".format(frame_id)] = [img_x_detection, img_y_detection]
                        log_data_phy_dict["{}".format(frame_id)] = [phy_x_detection, phy_y_detection]

        file_read.close()

        return log_data_dict, log_data_phy_dict

def csv_process(file_path_all):

        frame_id = "frame_id"
        csv_data_dict = dict()
        #x_key = 'pos_FRTire_x'
        #y_key = 'pos_FRTire_y'
        #with open(file_path_all,encoding='utf-8') as csvfile:
        with open(file_path_all) as csvfile:

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
                       
                        real_x = float(rows[x_index])
                        real_y = float(rows[y_index])

                        csv_data_dict["{}".format(frame_id)] = [real_x, real_y]
       
        return csv_data_dict

def csv_process_bak(file_path_all):

       
        csv_data_dict = dict()

        #with open(file_path_all,encoding='utf-8') as csvfile:
        with open(file_path_all) as csvfile:

                reader=csv.reader(csvfile)
                for i,rows in enumerate(reader):
                        # skip first row
                        if(i < 1):
                                continue

                        frame_id = rows[0]
                        real_x = float(rows[2])
                        real_y = float(rows[3])

                        csv_data_dict["{}".format(frame_id)] = [real_x, real_y]

        csvfile.close()
       
        return csv_data_dict



def merge_log(src_file_path, file_type,channel_id):

        for files in os.listdir(src_file_path):

                name_list = files.split(".")
                if(name_list[-1] == file_type ):
                        file_path = os.path.join(src_file_path, files)
                        log_data_dict, log_data_phy_dict = log_process(file_path, channel_id)
                

        return log_data_dict, log_data_phy_dict

def merge_csv(src_file_path, file_type):

        for files in os.listdir(src_file_path):

                name_list = files.split(".")

                if(name_list[-1] == file_type ):
                        file_path = os.path.join(src_file_path, files)
                        csv_data_dict = csv_process(file_path)
                
        return csv_data_dict



def match_data(log_data_dict,csv_data_dict):

        all_data = list()
        for key, value in log_data_dict.items():
                #check key in 2 data
                if key not in csv_data_dict.keys():
                        continue

                [real_x,real_y] = csv_data_dict[key]
                real_coordinate = [real_x,real_y]

                [img_x, img_y] = log_data_dict[key]
                img_coordinate = [img_x,img_y]
          
                single_data = [real_coordinate, img_coordinate]
                all_data.append(single_data)

        return all_data

def match_data_add_frame_id(log_data_dict,csv_data_dict):

        all_data = list()
        for key, value in log_data_dict.items():
                #check key in 2 data
                if key not in csv_data_dict.keys():
                        continue

                [real_x,real_y] = csv_data_dict[key]
                real_coordinate = [real_x,real_y]

                [img_x, img_y] = log_data_dict[key]
                img_coordinate = [img_x,img_y]
          
                single_data = [real_coordinate, img_coordinate, key]
                all_data.append(single_data)

        return all_data

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

def write_data_to_csv(file_name, write_data):

        outFile = open(file_name,"w")
        targetWriter = csv.writer(outFile)
        file_head = ['rtk_x', 'rtk_y', 'img_phy_x', 'img_phy_y']

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

                
                out_data = [phy_x, phy_y,img_x,img_y]
                targetWriter.writerow(out_data)

        outFile.close()

def write_frame_id_to_txt(file_name, write_data):

        file_write = open(file_name,"w+")

        for key, value in write_data.items():
        
                
                #roi filter
                flag = phy_coordinate_filter(value)
                if(flag == False):
                        continue

                write_line = key + '\n'
                file_write.write(write_line)

        file_write.close()

def write_frame_id_to_txt_dict(file_name, frame_id_img_dict, frame_id_phy_dict):

        file_write = open(file_name,"w+")

        for key, value in frame_id_phy_dict.items():
        
                #roi filter
                flag = phy_coordinate_filter(value)
                if(flag == False):
                        continue
                img_data = frame_id_img_dict[key]
                write_line = key + ' ' + str(img_data) + '\n'
                file_write.write(write_line)

        file_write.close()

                        
def parse_data(phy_img_data):

         label_data_ori = np.array(phy_img_data)[:,0,:]
         label_data = label_data_ori * 100
         img_phy_data = np.array(phy_img_data)[:,1,:]

         return label_data, img_phy_data

def plot_data(label_data, img_phy_data, save_path):

        label_data_x = label_data[:,0]
        label_data_y = label_data[:,1]
        x = range(len(label_data_y))
        

        img_phy_data_x = img_phy_data[:,0]
        img_phy_data_y = img_phy_data[:,1]

        plt.figure()

        plt.plot(x, label_data_x, marker='*', mfc='w',label=u'rtk_data')
        plt.plot(x, img_phy_data_x, marker='.', mfc='w',label=u'img_data')

        plt.legend()
        plt.xlabel(u"id") 
        plt.ylabel("x coordiante") 

        # gcf: Get Current Figure
        fig = plt.gcf()
        fig.savefig(save_path + 'error_x_plot.png', dpi=1000)
        plt.show()


        
if __name__ == "__main__":
        
        # src_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data/'
        # #save_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label/20190620_dynamic_label.txt'
        # save_img_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label/20190626_dynamic_0001_label_img.txt'
        # save_phy_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label/20190626_dynamic_0001_label_phy.txt'
        # save_frame_id_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label/20190626_dynamic_0001_frame_id.txt'
        # #save_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label/20190620_dynamic_label.csv'

        # src_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data/rtk_100hz_0629/'
        # save_img_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label5/20190626_dynamic_0001_label_img.txt'
        # save_phy_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label5/20190626_dynamic_0001_label_phy.txt'
        # save_frame_id_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label5/20190626_dynamic_0001_frame_id.txt'

        src_file_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190704_rtk_100hz/rtk_100hz_dynamic_data/'
        save_img_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label6/20190626_dynamic_0001_label_img.txt'
        save_phy_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label6/20190626_dynamic_0001_label_phy.txt'
        save_frame_id_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_label6/20190626_dynamic_0001_frame_id.txt'
       

        file_log = 'log'
        file_csv = 'csv'
        channel_id = "front"
        
        log_data_dict, log_data_phy_dict = merge_log(src_file_path, file_log, channel_id)
        csv_data_dict = merge_csv(src_file_path, file_csv)

        # phy_img_data = match_data(log_data_dict,csv_data_dict)
        # write_data_to_txt(save_img_file_path, phy_img_data)

        phy_img_data = match_data_add_frame_id(log_data_dict,csv_data_dict)
        write_data_to_txt_add_frame_id(save_img_file_path, save_frame_id_file_path,phy_img_data)

        # phy_img_phy_data = match_data(log_data_phy_dict,csv_data_dict)
        # write_data_to_txt(save_phy_file_path, phy_img_phy_data)
        #write_data_to_csv(save_file_path, phy_img_data)

        # frame_id_dict = get_frame_id(log_data_dict,csv_data_dict)
        # write_frame_id_to_txt(save_frame_id_file_path, frame_id_dict)

        # frame_id_dict = get_frame_id_and_phy(log_data_dict,csv_data_dict)
        # write_frame_id_to_txt_dict(save_frame_id_file_path, frame_id_dict)

        # frame_id_img_dict, frame_id_phy_dict = get_frame_id_and_img(log_data_dict,csv_data_dict)
        # write_frame_id_to_txt_dict(save_frame_id_file_path, frame_id_img_dict, frame_id_phy_dict)

        #label_data, img_phy_data = parse_data(phy_img_data)
        #plot_data(label_data, img_phy_data, save_file_path)


        
        
         
