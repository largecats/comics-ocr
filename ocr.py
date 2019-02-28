import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import os
import zipfile
import csv
import scipy.misc
import numpy as np

# finds all speech bubbles in the given comic page and returns a list of cropped speech bubbles (with possible false positives)
def findSpeechBubbles(imagePath, method = 'simple'):
    # read image
    image = cv2.imread(imagePath)
    # gray scale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # filter noise
    imageGrayBlur = cv2.GaussianBlur(imageGray,(3,3),0)
    if method != 'simple':
        # recognizes more complex bubble shapes
        imageGrayBlurCanny = cv2.Canny(imageGrayBlur,50,500)
        ret, binary = cv2.threshold(imageGrayBlurCanny,235,255,cv2.THRESH_BINARY)
    else:
        # recognizes only rectangular bubbles
        ret, binary = cv2.threshold(imageGrayBlur,235,255,cv2.THRESH_BINARY)
    
    binary, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    croppedImageList = []
    for contour in contours:
        rect = cv2.boundingRect(contour)
        [x, y, w, h] = rect
        if w < 500 and w > 60 and h < 500 and h > 25:
            croppedImage = image[y:y+h, x:x+w]
            croppedImageList.append(croppedImage)

    return croppedImageList

# function that applies the ocr engine to the given image and returns the recognized script where illegitimate characters are filtered out
def tesseract(image):
    script = pytesseract.image_to_string(image, lang='eng')
    #print(script)
    for char in script:
        if char not in ' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;\'':
            script = script.replace(char,'')
    
    return script

# function that loops thru each file in the given directory, not including zip files
def looper(rootDir):
    fileNameList = []
    filePathList = []
    for subDir, dirs, files in os.walk(rootDir):
        for file in files:
            fileInfo = file.split('.')
            fileName, fileExten = fileInfo[0], fileInfo[-1]
            filePath = os.path.join(subDir, file)
            if fileExten == 'jpg' or fileExten == 'png' or fileExten == '.bmp':
            # if fileExten != 'zip':
                if fileName not in fileNameList:
                    fileNameList.append(fileName)
                    filePathList.append(filePath)
            # else:
            #     z = zipfile.ZipFile(file, 'r')
            #     zippedFileList = z.namelist()
            #     for zippedFile in zippedFileList:
            #         zippedFileInfo = zippedFile.split('.')
            #         zippedFileName, zippedFileExten = zippedFileInfo[0], zippedFileInfo[-1]
            #         zippedFilePath = os.path.join(subDir, file, zippedFile)
            #         if zippedFileName not in fileNameList:
            #             fileNameList.append(zippedFileName)
            #             filePathList.append(zippedFilePath)
    
    return filePathList

# function that denoises the given image with n iterations
def denoise(image, n):
    i = 0
    while i < n:
        image = cv2.fastNlMeansDenoisingColored(image)
        i += 1

    return image 

# function that appends image path and script to the output csv file
def write_script_to_csv(imagePath, script, outputFilePath):
    with open(outputFilePath, 'a', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        newRow = [imagePath, script]
        writer.writerow(newRow)

# output file path and directory to be looped thru
outputFilePath = 'E:\\Fun\\TFComicScript.csv'
rootDir = 'E:\\Fun\\Transformers Comics folders'
#rootDir = 'E:\\Fun\\Programming\\For fun\\test'

# initializes output file
with open(outputFilePath, 'w',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['filePath', 'script'])

# for each image in the given directory, process each speech bubble found and feed it to the ocr engine
for imagePath in looper(rootDir):
    print(imagePath)
    # find speech bubbles in each image
    try:
        croppedImageList = findSpeechBubbles(imagePath, method = 'simple')
    except:
        continue
    scriptList = []
    for croppedImage in croppedImageList:
        # enlarge
        croppedImage = cv2.resize(croppedImage, (0,0), fx=2, fy=2)
        # denoise
        croppedImage = denoise(croppedImage, 2)
        kernel = np.ones((1, 1), np.uint8)
        croppedImage = cv2.dilate(croppedImage, kernel, iterations=50)
        croppedImage = cv2.erode(croppedImage, kernel, iterations=50)

        # turn gray
        croppedImageGray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        # Gaussian filter
        croppedImageGrayBlur = cv2.GaussianBlur(croppedImageGray,(5,5),0)
        # edge detection
        croppedImageGrayBlurLaplacian = cv2.Laplacian(croppedImageGrayBlur,cv2.CV_64F)
        # adjust contrast and brightness
        croppedImageGrayBlurLaplacian = np.uint8(np.clip((10 * croppedImageGrayBlurLaplacian + 10), 0, 255))

        # pass cropped image to the ocr engine
        script = tesseract(croppedImageGrayBlurLaplacian)
        if script != '' and script not in scriptList:
            scriptList.append(script)
            print(script)
            # append image path and script to the output csv file
            write_script_to_csv(imagePath, script, outputFilePath)