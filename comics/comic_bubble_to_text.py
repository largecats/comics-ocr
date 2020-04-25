##################################################
#                 import modules                 #
##################################################
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
import os
import csv

##################################################
#                helper functions                #
##################################################
# find all speech bubbles in the given comic page and return a list of cropped speech bubbles (with possible false positives)
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
        binary = cv2.threshold(imageGrayBlurCanny,235,255,cv2.THRESH_BINARY)[1]
    else:
        # recognizes only rectangular bubbles
        binary = cv2.threshold(imageGrayBlur,235,255,cv2.THRESH_BINARY)[1]
    # find contours
    contours = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]
    # get the list of cropped speech bubbles
    croppedImageList = []
    for contour in contours:
        rect = cv2.boundingRect(contour)
        [x, y, w, h] = rect
        # filter out speech bubble candidates with unreasonable size
        if w < 500 and w > 60 and h < 500 and h > 25:
            # uncomment to view the contour rectangles that are detected
            # cv2.rectangle(image, (x,y), (w+x,h+y), (0,255,0), 2)
            croppedImage = image[y:y+h, x:x+w]
            croppedImageList.append(croppedImage)
    
    # uncomment to view the contour rectangles that are detected
    # cv2.imshow("img", image)
    # cv2.waitKey(0)

    return croppedImageList

# apply the ocr engine to the given image and return the recognized script where illegitimate characters are filtered out
def tesseract(image):
    script = pytesseract.image_to_string(image, lang = 'eng')
    for char in script:
        if char not in ' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;\'':
            script = script.replace(char,'')
    
    return script

# loop through each file in the given directory, not including zip files
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

    return filePathList

# denoise the given image with n iterations
def denoise(image, n):
    i = 0
    while i < n:
        image = cv2.fastNlMeansDenoisingColored(image)
        i += 1

    return image 

# append image path and script to the output csv file
def write_script_to_csv(imagePath, script, outputFilePath):
    with open(outputFilePath, 'a', encoding = "utf-8", newline = "") as f:
        writer = csv.writer(f)
        newRow = [imagePath, script]
        writer.writerow(newRow)

##################################################
#                   main work                    #
##################################################
# set working directory
path = ""
os.chdir(path)

# output file path and directory to be looped through
outputFilePath = 'comic-script.csv'
rootDir = ''

# initialize output file
with open(outputFilePath, 'w',newline = "") as f:
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
        croppedImage = cv2.resize(croppedImage, (0,0), fx = 2, fy = 2)
        # denoise
        croppedImage = denoise(croppedImage, 2)
        kernel = np.ones((1, 1), np.uint8)
        croppedImage = cv2.dilate(croppedImage, kernel, iterations = 50)
        croppedImage = cv2.erode(croppedImage, kernel, iterations = 50)

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