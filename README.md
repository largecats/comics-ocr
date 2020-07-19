# comics-ocr
Tool for extracting script from comic pages using OCR engine Tesseract.

- [comics-ocr](#comics-ocr)
- [Installation](#installation)
  - [Install using pip](#install-using-pip)
  - [Install from source](#install-from-source)
- [Compatibility](#compatibility)
- [Usage](#usage)

# Installation

## Install using pip
TBD:
View package at https://test.pypi.org/project/comicsocr-largecats/.
```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps comicsocr-largecats
```
TBD:
```
pip install comicsocr
```

## Install from source
See [here](https://docs.python.org/2/install/index.html#splitting-the-job-up).
```
python setup.py install
```

# Compatibility
Supports Python 2.7 and 3.6+.

# Usage
```
usage: comicsocr [-h] [--paths PATHS [PATHS ...]] [--output-path OUTPUT_PATH]
                 [--config CONFIG]

Tool to extract scripts from comic pages.

optional arguments:
  -h, --help            show this help message and exit
  --paths PATHS [PATHS ...]
                        Paths to comic image files or directorys containing
                        comic image files.
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