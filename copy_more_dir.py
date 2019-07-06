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

def lookup_dir(src_path):

        flag = True
        data = [path]  # save dir list
        while flag:
                for dir1 in xrange(src_path): #
                        print("---")
def detect_walk(dir_path):
    dir_list = []tt
    for root, dirs, files in os.walk(dir_path):
        for filename in files:        
            print "file:%s\n" % filename
        for dirname in dirs:
            if os.path.isdir(dirname):
                    continue
        
            print "dir:%s\n" % dirname
            dir_list.append(dirname)

    return dir_list

def check_dir(dir_list):
        dir_list_new = list()

        for dir_name in dir_list:

                if len(dir_name) > 4:
                        continue

                dir_list_new.append(dir_list)

        return dir_list_new

def copy_dir(dir_list):









if __name__ == "__main__":

        src_file_path = '/media/xieyi/Elements/zwk/new_0625_jingtai/'
        save_file_path = '/media/xieyi/Elements/zwk/new_0625_jingtai/all_video/'
        mkdir(save_file_path)
        detect_walk(src_file_path)




        '''
        for root, dirs,files in os.walk(src_file_path, topdown=False):
        
                for name in files:

                        name_list = name.split(file_type)
                        if(len(name_list) <= 1):
                                continue
                        file_path = os.path.join(root, name)
        '''
                        
                
                      

                 

         
