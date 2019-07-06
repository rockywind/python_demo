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


src_image_path = '/home/xieyi/pic/tjp_frontoutput/'
save_image_path = '/home/xieyi/pic/tjp_frontoutput_rename/'
mkdir(save_image_path)
imgae_type = 'bmp'
new_image_type = 'bmp'
#image_num = 1200
image_num = 0
for index ,file_name in enumerate(os.listdir(src_image_path)):

    if file_name.split('.')[-1] == imgae_type:
        
        old_path = src_image_path + file_name
        #image_data = cv2.imread(old_path)
        new_name_1 = str(file_name.split('.')[0])

        new_name_2 = new_name_1[-12:]
        #new_name_3 = int(new_name_2) - image_num
        #index = new_name_3
        index = image_num
        image_num = image_num + 1
        image_data = np.array(sm.imread(old_path))
        #image_data = sm.imresize(image_data, [192, 320])
        image_data = sm.imresize(image_data, [384, 640])
        new_name = str(index).zfill(6) + '.' + new_image_type
        new_path = save_image_path + new_name
        sm.imsave(new_path, image_data)
        #cv2.imwrite(new_path, image_data)
        #os.rename(old_path, new_path)
