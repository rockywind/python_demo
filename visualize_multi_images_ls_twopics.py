import os
import cv2
import PIL
import numpy as np
from scipy import misc
import matplotlib.image as mpimg
import copy

def save_output_img(path, img):
    # Make it work for bin images too
    if len(img.shape) == 2:
        imgN = bin_to_rgb(img)
    else:
        imgN = img
    misc.imsave(path, imgN)


def bin_to_rgb(bin_image):
    return cv2.cvtColor(bin_image*255, cv2.COLOR_GRAY2RGB)
  
  

def compose_images(dst, src, nrows, ncols, num):
    assert 0 < num <= nrows * ncols

    if nrows > ncols:
        newH = int(dst.shape[0]/nrows)
        dim = (int(dst.shape[1] * newH/dst.shape[0]), newH)
    else:
        newW = int(dst.shape[1]/ncols)
        #dim = (newW, int(dst.shape[0] * newW/dst.shape[1]))
        dim =(480,600)
    # Make it work for bin images too
    if len(src.shape) == 2:
        srcN = bin_to_rgb(src)
    else:
        srcN = np.copy(src)

    img = cv2.resize(srcN, dim, interpolation = cv2.INTER_AREA)

    nr = (num - 1) // ncols
    nc = (num - 1) % ncols

    dst[nr * img.shape[0]:(nr + 1) * img.shape[0], nc * img.shape[1]:(nc + 1) * img.shape[1]] = copy.copy(img)

    return dst
  
  
  
  
  
inter1 = 0
inter2 = 0
def main():
    
    
    img_dir = './result2/'
    
    #print 'img_dir+++++', img_dir
    seg_dir = './top_view_black/' 
    #point_dir = '\\\\lzding\\share_lz2\\08_mask_rcnn\\04_test\\20190116\\image_test\\right_2/'
    #blend_dir = 'missImage/'
    save_dir = './result/'
    im_names = list(os.walk(img_dir))[0][2]
    
    print 'img_dir.shape++++',np.array(img_dir).shape
    print 'img_dir+++++', img_dir
    for im_name in im_names:
        #im_name = name[0:6]
        src_front_dir = img_dir + im_name
        #src_rear_dir = img_rear_dir + im_name

        index = im_name.split('.')
        index0 = index[0]
        index_num_left = int(index0[-6:]) + inter1
        str_index_left = str(index_num_left).zfill(6)
        src_left_dir = seg_dir + index0[0:-6] + str_index_left + '.jpg'
	   

        #index_num_right = int(index0[-6:]) + inter2
        #str_index_right = str(index_num_right).zfill(6)
        #src_right_dir = point_dir + index0[0:-6] + str_index_right + '.jpg'


        #ori_img_path = img_dir + name
        #seg_path = seg_dir + name
        #point_path = point_dir + name 
        #blend_path = blend_dir + name
        save_path = save_dir + im_name

        image = mpimg.imread(src_front_dir)   	
        seg_im = mpimg.imread(src_left_dir)    	
        #point_im = mpimg.imread(src_right_dir)    	
        #blend_im = mpimg.imread(blend_path)
    

        #resImg = np.zeros((720*2,1280*2,3))
        #resImg = np.zeros((360+640,720,3))
        #resImg = np.zeros((720,720,3))
        #image = cv2.resize(image, (720, 360))
        #seg_im = cv2.resize(seg_im, (360, 360))
        resImg = np.zeros((600,960,3))#vertical first,horizon after
        image = cv2.resize(image, (480, 600))#horizon first, verticalafter
        seg_im = cv2.resize(seg_im, (480, 600))#horizon first, verticalafter
        #point_im = cv2.resize(point_im, (360, 360))
        print 'image.shape = ', image.shape
        #resImg[0:360,0:720,:] = image[:,:,:]
        #resImg[360:720,0:360,:] = seg_im[:,:,:]
        #resImg[360:720,360:720,:] = point_im[:,:,:]
        resImg[:,0:480,:] = image[:,:,:]#vertical first,horizon after
        resImg[:,480:960,:] = seg_im[:,:,:]#vertical first,horizon after
        #resImg[360:720,360:720,:] = point_im[:,:,:]
    
        
        '''
        resImg[0:720,(720-640):(720+640),:] = image[:,:,:]
        
        print 'seg_im.shape', seg_im.shape
        a = resImg[720:2000,0:720,:]
        print 'a.shape', a.shape
        print 'resImg.shape=', resImg.shape
        resImg[720:1440,0:720,:] = seg_im[:,:,:]
        #resImg[0:720,720:,:] = seg_im[:,:,:]
        resImg[720:,720:,:] = point_im[:,:,:]
        '''

        #compose_images(resImg, image, 2, 2, 1)
        #compose_images(resImg, seg_im, 2, 2, 2)
        #--------------------------------------------------------------------------------------------------------------
        save_output_img(save_path, resImg)
     
        #compose_images(resImg, point_im, 1, 3, 2)
     
        #compose_images(resImg, blend_im, 1, 3, 3)
    		
        #resImg = np.zeros_like(image)
        #resImg = np.zeros([683,,3])
    	
        #resImg[0:301,:,:] = resImg_2[0:301,:,:]
        #resImg[301:602,:,:] = blend_im[:,:,:]
    		
        #compose_images(resImg, resImg_2, 2, 1, 1)
       
    	#compose_images(resImg, blend_im, 2, 1, 2)
    	#print "--------type--------",type(resImg)
    	#resImg[int(h/2):int(h/2)+50,int(w/2):(int(w/2)+50),:] = 0
    	#save_output_img(save_path, resImg)
    
    	#save_output_img(save_path, point_im)	
    	#break
    	#w,h = image.shape[1], image.shape[0]
    	#resImg[int(h/2):int(h/2)+30,int(w/2):(int(w/2)+260),0] = 0
    	#resImg[int(h/2):int(h/2)+30,int(w/2):(int(w/2)+260),1] = 255
           #resImg[int(h/2):int(h/2)+30,int(w/2):(int(w/2)+260),2] = 0
    
    	#cv2.putText(resImg, "Zadas Result" , (60, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 0], 1)
    	#cv2.putText(resImg, "Wrong Slots" , (240+60, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 0], 1)
     	#cv2.putText(resImg, "Miss Slots" , (240*2+60, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 0], 1)
     	# cv2.putText(resImg, "Safe region and" , (700, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 0], 1)
     	#cv2.putText(resImg, "forward vehicle detection" , (700, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 0], 1)
     	#   cv2.putText(resImg, "Safe region, free space and forward vehicle detection", (20, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255, 255, 0], 1)
     	#cv2.putText(resImg, "Right Curvature: %.2f m" % (self.right_curverad), (int(w/2) + 20, int(h/4) + 2*40 + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 255, 255], 2)
    
    
    	#--------------------------------------------------------------------------------------------------------------
    	# point
        '''
    	point = [24, int(h/2)+30]
    	thickness = -1
    	cv2.circle(resImg, tuple(point), 3, (0, 0, 255),thickness);
           cv2.putText(resImg, "----left down point" , (28, int(h/2)+34), cv2.FONT_HERSHEY_SIMPLEX, 0.4, [255, 255,255], 1)
    
    
    	point = [24, int(h/2)+40]
           thickness = -1
           cv2.circle(resImg, tuple(point), 3, (255, 0, 255),thickness);
           cv2.putText(resImg, "----left up point" , (28, int(h/2)+44), cv2.FONT_HERSHEY_SIMPLEX, 0.4, [255, 255,255], 1)
    
           point = [24, int(h/2)+50]
           thickness = -1
           cv2.circle(resImg, tuple(point), 3, (255, 0, 0),thickness);
           cv2.putText(resImg, "----right up point" , (28, int(h/2)+54), cv2.FONT_HERSHEY_SIMPLEX, 0.4, [255, 255,255], 1)
    
           point = [24, int(h/2)+60]
           thickness = -1
           cv2.circle(resImg, tuple(point), 3, (0, 255, 0),thickness);
           cv2.putText(resImg, "----right down point" , (28, int(h/2)+64), cv2.FONT_HERSHEY_SIMPLEX, 0.4, [255, 255,255], 1)
    	'''
  

if __name__ == '__main__':
    main()  
