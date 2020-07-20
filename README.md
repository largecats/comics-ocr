# comics-ocr
Tool for extracting script from comic pages using OCR engine Tesseract. Inspired by motion comic [Rewind's last message](https://www.youtube.com/watch?v=1LBFR90f6rg) (or alternative link [here](https://www.bilibili.com/video/av2786047)). Useful for making something like [page 18~19 of The Transformers: More than Meets the Eye #16](https://www.transformers.kiev.ua/index.php?pageid=idw) (or alternative link in Chinese [here](http://www.tfg2.com/read.php?tid-45122.html)). Supports image file formats `.jpg`, `.png`. `.bmp`, `.tiff` formats on windows and unix systems. Supports archive file formats `.rar`, `.cbr`, `.zip` on unix systems.

- [comics-ocr](#comics-ocr)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Compatibility](#compatibility)
- [Usage](#usage)
- [Example](#example)

# Prerequisites
* [OCR engine Tesseract](https://github.com/tesseract-ocr/tessdoc/blob/master/Home.md)
* [patool](https://github.com/wummel/patool)
* [opencv-python](https://pypi.org/project/opencv-python/)

# Installation

```
python setup.py install
```

# Compatibility
Supports Python 2.7 and 3.6+.


# Usage
```
usage: comicsocr [-h] [--paths PATHS [PATHS ...]] [--output-path OUTPUT_PATH] [--config CONFIG]

Tool to extract scripts from comic pages.

optional arguments:
  -h, --help            show this help message and exit
  --paths PATHS [PATHS ...]
                        Paths to comic image files, archive files or directories containing comic image files. Supported file formats (windows and unix):
                        .jpg, .png, .bmp, .tiff. Supported archive file formats (unix only): .rar, .cbr, .zip.
  --output-path OUTPUT_PATH
                        Path to write the comic scripts to.
  --config CONFIG       Configurations.
```
**Configurations**
```
Help on class Config in module comicsocr.src.config:

class Config(builtins.object)
 |  Class for configurations.
 |
 |  Methods defined here:
 |
 |  __init__(self, speechBubbleSize={'width': [60, 500], 'height': [25, 500]}, show=False, showWindowSize={'height': 768}, charsAllowed=' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;\'', method=None)
 |      Parameters
 |      speechBubbleSize: dict
 |          Height and width ranges for the speech bubbles.
 |          Default to {'width': [60, 500],'height': [25, 500]}.
 |      charsAllowed: string
 |          Legitimate characters when reading from image.
 |          Default to ' -QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.?!1234567890"":;''.
 |      method: string
 |          Config.SIMPLE - recognizes only rectangular bubbles.
 |          Config.COMPLEX - recognizes more complex bubble shapes.
 |          Default to Config.SIMPLE.
 |      show: boolean
 |          If True, will show the image being processed with recognized contours.
 |          Note: This feature may require special handling on unix systems.
 |          Default to False.
 |      showWindowSize: dict
 |          Size of the window when displaying the image being processed.
 |          E.g., {'height': 768} means scale the image to height 768 with the same aspect ratio.
 |          Default to {'height': 768}.
```
# Example
Example use case can be found [here](https://largecats.github.io/2019/06/20/ocr-with-comics/).