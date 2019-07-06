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

def frame_id_txt_parse(frameid_file_path):
        i = 0

        frame_id_dict = {}
        with open(frameid_file_path, 'r') as file_read:

                while True:
                        line = file_read.readline() 

                        if not line:
                                break
                        
                        line_data = line.split(" ")
                        frame_id = line_data[0]

                        img_x_float = float(line_data[1][1:-1])
                        img_y_float = float(line_data[2][:-2])
                        img_x = "%6f" % (img_x_float)
                        img_y = "%6f" % (img_y_float)
                        i = i + 1


                        frame_id_dict["{}/{}".format(img_x, img_y)] = [frame_id]     

        file_read.close()

        return frame_id_dict

def zadas_file_parse(zadas_file_path):
        num_len = -2
        zadas_data_dict = {}
        with open(zadas_file_path, 'r') as file_read:

                while True:
                        line = file_read.readline()
                        if not line:
                                break
                        
                        line_data_ori = line.split(" ")
                        line_data = line_data_ori[2]

                        #real_data_x = line_data.split(",")[0][1:]
                        #real_data_y = line_data.split(",")[1][:-1]

                        img_data_x = line_data.split(",")[0][1:]
                        img_data_y = line_data.split(",")[1][:-1]
                        
                        line_write = line[:-1]
                        zadas_data_dict["{}/{}".format(img_data_x, img_data_y)] = [line_write]
        

        file_read.close()

        return zadas_data_dict

def write_data_to_txt(file_name, frame_id_dict, zadas_data_dict):

        file_write = open(file_name,"w+")

        for key, value in frame_id_dict.items():
                #check key in 2 data
                if key not in zadas_data_dict.keys():
                        print("---key--",key)
                        continue

                write_line = str(zadas_data_dict[key]) + "," + "frame_id = " + str((frame_id_dict[key])) + '\n'
               
                file_write.write(write_line)

        file_write.close()

                

        


if __name__ == "__main__":

        zadas_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0001_corret_add_frameid/20190624_rtk_ori_v1_01.txt'
        frameid_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0001_corret_add_frameid/20190626_dynamic_0001_label_img_frame_id.txt'
        add_frame_id_file_path = '/home/xieyi/pic/projection_error/all_txt/dynamic_data_correct/0001_corret_add_frameid/20190626_dynamic_0001_add_frame_id.txt'
        
        frame_id_dict = frame_id_txt_parse(frameid_file_path)
        zadas_data_dict = zadas_file_parse(zadas_file_path)
        write_data_to_txt(add_frame_id_file_path, frame_id_dict, zadas_data_dict)

           
                                        






                                        


