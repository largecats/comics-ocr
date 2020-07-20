# comics-ocr
Tool for extracting script from comic pages using OCR engine Tesseract. Inspired by motion comic [Rewind's last message](https://www.youtube.com/watch?v=1LBFR90f6rg) (or alternative link [here](https://www.bilibili.com/video/av2786047)). Useful for making something like [page 18~19 of The Transformers: More than Meets the Eye #16](https://www.transformers.kiev.ua/index.php?pageid=idw) (or alternative link in Chinese [here](http://www.tfg2.com/read.php?tid-45122.html)). 

* Supports image file formats `.jpg`, `.png`. `.bmp`, `.tiff` formats on Windows and Unix systems. 
* Supports archive file formats `.rar`, `.cbr`, `.zip` on Unix systems.
* The OCR engine Tesseract that is used is not trained, but it can be if needed.

- [comics-ocr](#comics-ocr)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Compatibility](#compatibility)
- [Usage](#usage)
  - [Using as command-line tool](#using-as-command-line-tool)
  - [Using as Python library](#using-as-python-library)
  - [Configurations](#configurations)

# Prerequisites
* [Tesseract](https://github.com/tesseract-ocr/tessdoc/blob/master/Home.md)
* [patool](https://github.com/wummel/patool)
* [opencv-python](https://pypi.org/project/opencv-python/)

# Installation

```
python setup.py install
```

# Compatibility
Supports Python 2.7 and 3.6+.


# Usage
See [here](https://largecats.github.io/2019/06/20/ocr-with-comics/) for more detailed example (using a simplified version of the tool).
## Using as command-line tool
```
usage: comicsocr [-h] [--paths PATHS [PATHS ...]] [--output-path OUTPUT_PATH] [--config CONFIG]

Tool to extract scripts from comic pages.

optional arguments:
  -h, --help            show this help message and exit
  --paths PATHS [PATHS ...]
                        Paths to comic image files, archive files or directories containing comic image files. Supported file formats (Windows and Unix):
                        .jpg, .png, .bmp, .tiff. Supported archive file formats (Unix only): .rar, .cbr, .zip.
  --output-path OUTPUT_PATH
                        Path to write the comic scripts to.
  --config CONFIG       Configurations.
```
E.g.,
```
[2020-07-20 22:47:58,252] INFO [api.py:54:read_from_file] Reading from file: C:\Users\largecats\Fun\programming\personal-projects\comics-ocr\test\test.jpg
[2020-07-20 22:47:59,299] INFO [reader.py:72:read] 'a ela a'
[2020-07-20 22:48:02,704] INFO [reader.py:72:read] 'THE LAW GAYS THISSORT OF THING HAS TOBE DECLARED ON-SITE.FORMALITIES.'
[2020-07-20 22:48:04,556] INFO [reader.py:72:read] "I DON'T UNDERSTAND WHYWE HAVE TO BE HERE. CAN'TWE FUST... PUSH A BUTTONAND BE DONE VUITH IT?"
[2020-07-20 22:48:05,359] INFO [reader.py:72:read] 'MINING OUTPOST C-12.'
[2020-07-20 22:48:06,166] INFO [reader.py:72:read] 'LONG AGO. PEACETIME.'
[2020-07-20 22:48:07,025] INFO [reader.py:72:read] 'THE CYBERTRON SYSTEM.Zs'
[2020-07-20 22:48:10,287] INFO [reader.py:72:read] 'Pinto d 3 ABO adieSoa an eee'
[2020-07-20 22:48:10,288] INFO [api.py:74:write_to_file] Writing to: C:\Users\largecats\Fun\programming\personal-projects\comics-ocr\test\result.txt
```

## Using as Python library
Call `api.read_from_file`, `api.read_from_archive_file`, or `api.read_from_directory` to read from a single image file, a single archive file, or a directory containing image files or archive files of images.

E.g.,
```
>>> from comicsocr import api
>>> api.read_from_file(imagePath=r'C:\Users\largecats\Fun\programming\personal-projects\comics-ocr\test\test.jpg')
[2020-07-20 23:15:35,071] INFO [api.py:54:read_from_file] Reading from file: C:\Users\largecats\Fun\programming\personal-projects\comics-ocr\test\test.jpg
[2020-07-20 23:15:36,128] INFO [reader.py:72:read] 'a ela a'
[2020-07-20 23:15:39,436] INFO [reader.py:72:read] 'THE LAW GAYS THISSORT OF THING HAS TOBE DECLARED ON-SITE.FORMALITIES.'
[2020-07-20 23:15:41,286] INFO [reader.py:72:read] "I DON'T UNDERSTAND WHYWE HAVE TO BE HERE. CAN'TWE FUST... PUSH A BUTTONAND BE DONE VUITH IT?"
[2020-07-20 23:15:42,058] INFO [reader.py:72:read] 'MINING OUTPOST C-12.'
[2020-07-20 23:15:42,867] INFO [reader.py:72:read] 'LONG AGO. PEACETIME.'
[2020-07-20 23:15:43,761] INFO [reader.py:72:read] 'THE CYBERTRON SYSTEM.Zs'
[2020-07-20 23:15:47,045] INFO [reader.py:72:read] 'Pinto d 3 ABO adieSoa an eee'
['a ela a', 'THE LAW GAYS THISSORT OF THING HAS TOBE DECLARED ON-SITE.FORMALITIES.', "I DON'T UNDERSTAND WHYWE HAVE TO BE HERE. CAN'TWE FUST... PUSH A BUTTONAND BE DONE VUITH IT?", 'MINING OUTPOST C-12.', 'LONG AGO. PEACETIME.', 'THE CYBERTRON SYSTEM.Zs', 'Pinto d 3 ABO adieSoa an eee']
```

## Configurations
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
 |          Note: This feature may require special handling on Unix systems.
 |          Default to False.
 |      showWindowSize: dict
 |          Size of the window when displaying the image being processed.
 |          E.g., {'height': 768} means scale the image to height 768 with the same aspect ratio.
 |          Default to {'height': 768}.
```