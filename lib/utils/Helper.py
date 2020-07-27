import logging
import numpy as np
from scipy import ndimage

class ImageChecker:

    def __init__(self, sensibility, split_factor=5, v_area_check=[], h_area_check=[]):
        self.sensibility = sensibility
        self.split_factor = split_factor
        self.v_area_check = v_area_check if len(v_area_check)!=0 else np.arange(split_factor).tolist()
        self.h_area_check = h_area_check if len(h_area_check)!=0 else np.arange(split_factor).tolist()
        
    def __unroll_image__(self, image):
        shape = image.shape
        x = shape[0]
        y = shape[1]
        image_reshaped_r = image[:,:,0].reshape(x*y,1)[:,0]
        image_reshaped_g = image[:,:,1].reshape(x*y,1)[:,0]
        image_reshaped_b = image[:,:,2].reshape(x*y,1)[:,0]
        image_reshaped_data = np.array([image_reshaped_r,image_reshaped_g,image_reshaped_b])
        image_reshaped_avg = np.average(image_reshaped_data, axis=0)
        return image_reshaped_avg
        
    def read_image(self, image_path):
        img = ndimage.imread(image_path)
        imgSplitted = [np.hsplit(x, self.split_factor) for x in np.vsplit(img, self.split_factor)]
        imgSplittedUnrolled = p = [[self.__unroll_image__(y) for y in x] for x in imgSplitted] 
        return np.array(imgSplittedUnrolled)

    def setRefImage(self, ref_image):
        self.ref_image = ref_image

    def check_motion(self, curr_image):
        count = 0
        for i in self.v_area_check:
            for j in self.h_area_check:
                score = np.dot(self.ref_image[i,j,:], curr_image[i,j,:])/np.sum(self.ref_image[i,j,:]**2)
                logging.info('  score(' + str(i) + ',' + str(j) + '): ' + str(score))
                if ( ( score < (1-self.sensibility)) | ( (1+self.sensibility) < score) ):
                    count=count+1
        logging.debug('split positives: ' + str(count))
        if count > 1:
            return True
        else: 
            return False

