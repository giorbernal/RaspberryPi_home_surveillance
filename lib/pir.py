"""
Package for interfacing with Raspberry PI PIR motion sensor.
"""
import logging
from gpiozero import MotionSensor
from lib.utils.Helper import ImageChecker

class MotionDetector:  # pylint: disable=too-few-public-methods
    """
    Class to interfaces with Raspberry PI PIR motion sensor module
    """

    def __init__(self, isCamera, sensibility, camera):
        self.base_dir = '/home/pi/Documents/RaspberryPi_home_surveillance/'
        self.pir = MotionSensor(4)
        self.isCamera = isCamera
        self.camera = camera
        self.ic = ImageChecker(sensibility)
        self.start()

    def start(self):
        if self.isCamera:
            ref_image_path = self.camera.take_photo(self.base_dir + 'tmp/ref.jpeg')
            ref_image = self.ic.read_image(ref_image_path)
            self.ic.setRefImage(ref_image)
        
    def movement_detected(self):
        """
        Check if movement detected.
        :return: boolean
        """

        motion_detected = bool(self.pir.motion_detected)

        if (motion_detected & self.isCamera):
            logging.info('unchecked motion detected!')
            current_image_path = self.camera.take_photo(self.base_dir + 'tmp/current.jpeg')
            current_image = self.ic.read_image(current_image_path)
            motion_image_detected = self.ic.check_motion(current_image)
            if (motion_image_detected):
                 logging.info('motion image detected!')
                 self.start()
            return motion_image_detected
        else:
            return motion_detected
