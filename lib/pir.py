"""
Package for interfacing with Raspberry PI PIR motion sensor.
"""
from gpiozero import MotionSensor
import numpy as np
from scipy import ndimage

class MotionDetector:  # pylint: disable=too-few-public-methods
    """
    Class to interfaces with Raspberry PI PIR motion sensor module
    """

    def __init__(self, isCamera, sensibility, camera):
        self.base_dir = '/home/pi/Documents/RaspberryPi_home_surveillance/'
        self.pir = MotionSensor(4)
        self.isCamera = isCamera
        self.camera = camera
        self.sensibility = sensibility
        self.start()

    def start(self):
        if self.isCamera:
            ref_image_path = self.camera.take_photo(self.base_dir + 'tmp/ref.jpeg')
            self.ref_image = self.__read_image__(ref_image_path)
        
    def movement_detected(self):
        """
        Check if movement detected.
        :return: boolean
        """

        motion_detected = bool(self.pir.motion_detected)

        if (motion_detected & self.isCamera):
            #print('sensor detection!')
            current_image_path = self.camera.take_photo(self.base_dir + 'tmp/current.jpeg')
            current_image = self.__read_image__(current_image_path)
            return self.__check_motion__(current_image)
        else:
            return motion_detected

    def __read_image__(self, image_path):
        img = ndimage.imread(image_path)
        shape = img.shape
        x = shape[0]
        y = shape[1]
        image_reshaped_r = img[:,:,0].reshape(x*y,1)[:,0]
        image_reshaped_g = img[:,:,1].reshape(x*y,1)[:,0]
        image_reshaped_b = img[:,:,2].reshape(x*y,1)[:,0]
        image_reshaped_data = np.array([image_reshaped_r,image_reshaped_g,image_reshaped_b])
        image_reshaped_avg = np.average(image_reshaped_data, axis=0)
        return image_reshaped_avg

    def __check_motion__(self, curr_image):
        score = np.dot(self.ref_image, curr_image)/np.sum(self.ref_image**2)

        print('score: ' + str(score))
        if ( ((1-self.sensibility) < score) & (score < (1+self.sensibility)) ):
            return False
        else:
            return True
