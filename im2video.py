import cv2
from cv2 import VideoWriter,VideoWriter_fourcc,imread,resize
import os
import glob

im_path = ".\\slot_detection\\"
images = sorted(glob.glob(im_path + '*.bmp'))
#Edit each frame's appearing time!
fps = 30
fourcc = VideoWriter_fourcc(*"MJPG")
#videoWriter = cv2.VideoWriter("3d_box_0927.avi",fourcc,fps,(330,810))
videoWriter = cv2.VideoWriter("beiqi_demo.avi",fourcc,fps,(240,300))
# cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')
#videoWriter = cv2.VideoWriter("test_0920.mp4",fourcc('M', 'J', 'P', 'G'),fps,(330,810))

for im in images:
    #print im
	frame = cv2.imread(im)
	videoWriter.write(frame)
	
videoWriter.release()