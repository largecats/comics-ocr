import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from PIL import Image


# open image
imagePath = 'E:\\Fun\\Programming\\For fun\\croppedImages\\5.png'
#imagePath = 'E:\\Fun\\Programming\\For fun\\test 5.png'
image = Image.open(imagePath)
print(image.size)
script = pytesseract.image_to_string(image, lang='eng')
print(script)
print('hello')

# text_file = open("E:\\Fun\\Programming\\For fun\\Output.txt", "w")
# text_file.write("text: %s" % script)
# text_file.close()