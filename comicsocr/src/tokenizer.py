import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import csv
import imutils

from comicsocr.src.config import Config


class Tokenizer:
    '''
    Class for finding comic speech bubbles.
    '''
    def __init__(self, config=Config()):
        '''
        Parameters
        speechBubbleSize: dict
            Length and width ranges for the speech bubbles. 
            Default to {'h': [25, 500], 'w': [60, 500]}.
        method: string
            Config.SIMPLE - recognizes only rectangular bubbles.
            Config.COMPLEX - recognizes more complex bubble shapes.
        '''
        self.config = config

    def tokenize(self, imagePath):
        '''
        Find all speech bubbles in the given comic image file.

        Parameters
        imagePath: string
            Path to the comic page image.
        show: boolean
            If true, will show contour rectangles detected while running.
            Note: May not be available in Python's interactive terminal and may require special handling to show on Unix systems.
        
        Return: list
            Cropped speech bubbles (with possible false positives).
        '''
        image = cv2.imread(imagePath)  # read image
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # gray scale
        imageGrayBlur = cv2.GaussianBlur(imageGray, (3, 3), 0)  # filter noise
        if self.config.method == Config.SIMPLE:
            # recognizes only rectangular bubbles
            binary = cv2.threshold(imageGrayBlur, 235, 255, cv2.THRESH_BINARY)[1]
        else:
            # recognizes more complex bubble shapes
            imageGrayBlurCanny = cv2.Canny(imageGrayBlur, 50, 500)
            binary = cv2.threshold(imageGrayBlurCanny, 235, 255, cv2.THRESH_BINARY)[1]
        # find contours
        contourResult = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contourResult[1] if imutils.is_cv3() else contourResult[0]
        # get the list of cropped speech bubbles
        croppedImageList = []
        for contour in contours:
            rect = cv2.boundingRect(contour)
            [x, y, w, h] = rect
            # filter out speech bubble candidates with unreasonable size
            if ((w >= self.config.speechBubbleSize['width'][0] and w <= self.config.speechBubbleSize['width'][1]) and
                (h >= self.config.speechBubbleSize['height'][0] and h <= self.config.speechBubbleSize['height'][1])):
                if self.config.show:
                    # add the contour rectangle detected in green color to image
                    cv2.rectangle(image, (x, y), (w + x, h + y), (0, 255, 0), 2)
                croppedImage = image[y:y + h, x:x + w]
                croppedImageList.append(croppedImage)
        if self.config.show:
            # view all contour rectangles that are detected
            image = Tokenizer.resize(image=image,
                                     width=self.config.showWindowSize.get('width'),
                                     height=self.config.showWindowSize.get('height'))
            cv2.imshow("window", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return croppedImageList

    @staticmethod
    def resize(image, width=None, height=None):
        (h, w) = image.shape[:2]  # current height and width

        if width is None and height is None:
            return image
        else:
            if width is None:  # resize by height
                ratio = height / h
                dim = (int(w * ratio), height)
            else:  # resize by width
                ratio = width / w
                dim = (width, int(h * ratio))
            return cv2.resize(image, dim)
