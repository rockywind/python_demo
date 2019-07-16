#!/usr/bin/env python
import cv2
import numpy as np
import os

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.mkdir(path)
    else: 
        print 'the floder is exist'

a = 1


# video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/right/'
# save_video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/right_right/'
# fixed_str = 'right'

# video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/left/'
# save_video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/left_front/'
# fixed_str = 'front'

video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/left/'
save_video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/left_left/'
fixed_str = 'left'


mkdir(save_video_path)

for root, dirs,files in os.walk(video_path, topdown=False):

	video_path_all = root + '/'+ fixed_str +'.avi'    
        
	#vc=cv2.VideoCapture(video_path + 'front.avi')
	vc=cv2.VideoCapture(video_path_all)

	c=1
	num_limit = 10
	num_max = 11
	if vc.isOpened():
		rval,frame=vc.read()
	else:
		rval=False
	while rval:
		rval,frame=vc.read()
		b = str(c)
		
		
		c=c+1
		if(c<num_limit):
			continue
		if(c>num_max):
			break

		#cv2.imwrite(save_video_path + '/' + b.zfill(6)+'.jpg',frame)
		img_name = root.split("/")[-1]
		if(img_name == ''):
				img_name = video_path.split("/")[-2]
		cv2.imwrite(save_video_path + '/' + img_name+'.jpg',frame)

		cv2.waitKey(1)
	vc.release()
