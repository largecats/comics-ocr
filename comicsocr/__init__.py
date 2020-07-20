# -*- coding: utf-8 -*-
from __future__ import print_function  # for print() in Python 2
import os
import sys
import argparse
import configparser
import logging
import codecs
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import comicsocr.src.api as api


def main(argv):
    '''
    Main function that enables formatting file from command-line.

    Parameters
    argv: list
        List of arguments in sys.argv, excluding the first argument which is the script itself.
    '''
    args = get_arguments(argv)
    config = args['config']
    paths = args['paths']
    outputPath = args['output_path']
    if config:
        for path in paths:
            name, extension = os.path.splitext(path)
            if os.path.isdir(path):
                api.read_from_directory(directory=path, outputPath=outputPath, config=config)
            elif extension in api.IMAGE_EXTENSIONS:
                api.read_from_file(imagePath=path, outputPath=outputPath, config=config)
            elif extension in api.ARCHIVE_EXTENSIONS:
                api.read_from_archive_file(path=path, outputPath=outputPath, config=config)
    else:
        for path in paths:
            name, extension = os.path.splitext(path)
            if os.path.isdir(path):
                api.read_from_directory(directory=path, outputPath=outputPath)
            elif extension in api.IMAGE_EXTENSIONS:
                api.read_from_file(imagePath=path, outputPath=outputPath)
            elif extension in api.ARCHIVE_EXTENSIONS:
                api.read_from_archive_file(path=path, outputPath=outputPath)


def get_arguments(argv):
    '''
    Get arguments passed via command-line in dictionary.

    Paramters:
    argv: list
        List of arguments in sys.argv, including the first argument which is the script itself.
    
    Returns: dict
        A dictionary containing arguments for the formatter.
    '''
    parser = argparse.ArgumentParser(description='Tool to extract scripts from comic pages.')

    parser.add_argument('--paths',
                        type=str,
                        nargs='+',
                        help='''
                        Paths to comic image files, archive files or directories containing comic image files. 
                        Supported file formats (Windows and Unix): .jpg, .png, .bmp, .tiff.
                        Supported archive file formats (Unix only): .rar, .cbr, .zip.
                        ''')

    parser.add_argument('--output-path',
                        type=str,
                        help='Path to write the comic scripts to. Recommended format is .csv.')

    parser.add_argument('--config', type=str, default=None, help="Configurations.")

    args = vars(parser.parse_args(argv[1:]))

    return args


def run_main():
    '''
    Entry point for console_scripts in setup.py
    '''
    main(sys.argv)


if __name__ == '__main__':
    run_main()
