import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
import logging
import sys

from comicsocr.src.config import Config
from comicsocr.src.tokenizer import Tokenizer

logger = logging.getLogger(__name__)
log_formatter = '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_formatter)


class Reader:
    '''
    Optical character reader.
    '''
    def __init__(self, config=Config()):
        '''
        Parameters
        config: Config() object
        '''
        self.config = config
        self.tokenizer = Tokenizer(config=config)

    def denoise(self, image, n):
        '''
        Denoise the given image with n iterations.
        '''
        for i in range(n):
            image = cv2.fastNlMeansDenoisingColored(image)

        return image

    def read(self, imagePath):
        '''
        Apply the ocr engine to the given image and return the extracted scripts where illegitimate characters are filtered out.

        Parameters
        imagePath: string
            Path to the comic page image.
        
        Return: list
            Strings of comic script extracted from the image.
        '''
        tokens = self.tokenizer.tokenize(imagePath=imagePath)
        scripts = []
        for token in tokens:
            # enlarge
            token = cv2.resize(token, (0, 0), fx=2, fy=2)
            # denoise
            token = self.denoise(image=token, n=2)
            kernel = np.ones((1, 1), np.uint8)
            token = cv2.dilate(token, kernel, iterations=50)
            token = cv2.erode(token, kernel, iterations=50)
            # turn gray
            tokenGray = cv2.cvtColor(token, cv2.COLOR_BGR2GRAY)
            # Gaussian filter
            tokenGrayBlur = cv2.GaussianBlur(tokenGray, (5, 5), 0)
            # edge detection
            tokenGrayBlurLaplacian = cv2.Laplacian(tokenGrayBlur, cv2.CV_64F)
            # adjust contrast and brightness
            tokenGrayBlurLaplacian = np.uint8(np.clip((10 * tokenGrayBlurLaplacian + 10), 0, 255))
            script = pytesseract.image_to_string(tokenGrayBlurLaplacian, lang='eng')
            if len(script) == 0 or script.isspace():
                continue
            for char in script:  # remove illegitimate characters
                if char not in self.config.charsAllowed:
                    script = script.replace(char, '')
            logger.info(repr(script))
            scripts.append(script)
        return scripts
