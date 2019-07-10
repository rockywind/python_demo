#!/usr/bin/env python
import cv2
import numpy as np

a = 1

# video_path = '/media/xieyi/Elements/zwk/video/middle/'
# save_video_path = '/media/xieyi/Elements/zwk/video/middle/right'
video_path = '/media/xieyi/Elements/zwk/video/left-1.8/'
save_video_path = '/media/xieyi/Elements/zwk/video/left-1.8/right'
vc=cv2.VideoCapture(video_path + 'right.avi')
c=1
num_limit = 300
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

	cv2.imwrite(save_video_path + '/' + b.zfill(6)+'.jpg',frame)
	cv2.waitKey(1)
vc.release()
