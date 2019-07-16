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

# video_path = '/media/xieyi/Elements/zwk/video/middle/'
# save_video_path = '/media/xieyi/Elements/zwk/video/middle/right'
video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/capture_[350,400]/'
save_video_path = '/media/xieyi/Elements/zwk/0713src/changan0713/'

mkdir(save_video_path)

vc=cv2.VideoCapture(video_path + 'front.avi')
c=1
num_limit = 10
num_max = 302
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
	img_name = video_path.split("/")[-1]
	if(img_name == ''):
			img_name = video_path.split("/")[-2]
	cv2.imwrite(save_video_path + '/' + img_name+'.jpg',frame)

	cv2.waitKey(1)
vc.release()
