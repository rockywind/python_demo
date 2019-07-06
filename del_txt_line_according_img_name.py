import numpy as np
import os
import scipy.misc as sm
#import cv2

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'


def read_txt(file_name):

        txt_data_dict = {}

        with open(src_file_path, 'r') as file_read:


                while True:

                        line = file_read.readline() 

                        if not line:
                                break
                        
                        line = line.strip() # del none line,judge it is empty line
                        if(len(line) == 0):
                                continue

                        line_ori = line.split(" ")
                          
                        frame_id = line_ori[0][1:-1]
                        # img_x = float(line_ori[1][1:])
                        # img_y = float(line_ori[2][:-1])

                        img_x = line_ori[1][1:]
                        img_y = line_ori[2][:-1]

                        txt_data_dict["{}".format(frame_id)] = [img_x,img_y]  
        file_read.close()

        return txt_data_dict

def read_img_name(file_path, file_suffix):

        frame_id_list = list()

        for file_name in os.listdir(file_path):

                img_name_no_suffix = file_name.split(file_suffix)

                if len(img_name_no_suffix)<=1:
                        continue

                img_name_tmp = img_name_no_suffix[0].split("_")
                frame_id = img_name_tmp[1]
                frame_id_list.append(frame_id)

        return frame_id_list

def write_txt(save_file_path, write_data_dict):

        file_write = open(save_file_path,"w+")
        
        for key, value in txt_data_dict.items():

                write_line = '[' + key + ']'  + ' ' \
                        '[' + value[0] + ' ' + value[1] + ']' +  '\n'

                file_write.write(write_line)
                

        file_write.close()
        


if __name__ == "__main__":

        file_suffix = ".bmp"                       
        # src_file_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_0-9100.txt'
        # src_img_path = '/media/xieyi/Elements/zwk/20190704/rtk_video_det/capure_1_draw_img_select/'
        # save_file_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_0-9100_select.txt'

        src_file_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_front_capture1.txt'
        src_img_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/select_03/'
        save_file_path = '/home/xieyi/pic/projection_error/all_txt/rtk_check/20190705_capture_1/red_point_front_capture1_64.txt'
        
        frame_id_list = read_img_name(src_img_path, file_suffix)
        txt_data_dict = read_txt(src_file_path)

        for key, value in txt_data_dict.items():
                if(key not in frame_id_list):
                        txt_data_dict.pop(key)

        write_txt(save_file_path, txt_data_dict)

        



                






                        



         
