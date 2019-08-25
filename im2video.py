import cv2
from cv2 import VideoWriter,VideoWriter_fourcc,imread,resize
import os
import glob

im_path = "/home/xieyi/save_img/img_12/0822/save_all/"
images = sorted(glob.glob(im_path + '*.bmp'))
#Edit each frame's appearing time!
fps = 20
fourcc = VideoWriter_fourcc(*"MJPG")
#videoWriter = cv2.VideoWriter("3d_box_0927.avi",fourcc,fps,(330,810))
#videoWriter = cv2.VideoWriter("beiqi_demo.avi",fourcc,fps,(240,300))
#videoWriter = cv2.VideoWriter("beiqi_demo.avi",fourcc,fps,(720,2080))

#videoWriter = cv2.VideoWriter("TJP_demo_03.avi",fourcc,fps,(2080,1150))
videoWriter = cv2.VideoWriter("TJP_demo_no_red_point_20fps.avi",fourcc,fps,(1360,720))
# cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
#videoWriter = cv2.VideoWriter("test_0920.mp4",fourcc('M', 'J', 'P', 'G'),fps,(330,810))

for im in images:
    #print im
	frame = cv2.imread(im)
	videoWriter.write(frame)
	
videoWriter.release()