import sys
import os
import csv
import configparser
import ast
import patoolib
import logging
import subprocess
import ntpath

from comicsocr.src.config import Config, DEFAULT_CONFIG_SECTION
from comicsocr.src.tokenizer import Tokenizer
from comicsocr.src.reader import Reader

logger = logging.getLogger(__name__)
log_formatter = '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_formatter)

IMAGE_EXTENSIONS = ['.jpg', '.png', '.bmp', '.tiff']
ARCHIVE_EXTENSIONS = ['.rar', '.cbr', '.zip']


def read_from_file(imagePath, outputPath=None, config=Config()):
    if type(config) == type(Config()):  # config is a Config() object
        reader = Reader(config=config)
    else:  # create Config() object from config
        if type(config) == str:
            if config.startswith('{'):  # config is a dictionary in string
                config = eval(config)
                reader = Reader(config=_create_config_from_dict(configDict=config))
        elif type(config) == dict:  # config is a dictionary
            reader = Reader(config=_create_config_from_dict(configDict=config))
        else:
            raise Exception('Unsupported config type')
    logger.info('Reading from file: ' + imagePath)
    script = reader.read(imagePath=imagePath)
    if outputPath:
        write_to_csv(imagePath=imagePath, script=script, outputPath=outputPath)
    else:
        return script


def write_to_csv(imagePath, script, outputPath):
    '''
    Write file path and extracted comic script to given output path.
    '''
    logger.info('Writing to: ' + outputPath)
    with open(outputPath, 'a', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for line in script:
            newRow = [imagePath, line]
            writer.writerow(newRow)


def read_from_archive_file(path, outputPath=None, config=Config()):
    logger.info('Reading from archive file: ' + path)
    patoolib.test_archive(path, verbosity=1)  # test integrity of archive
    parentDir = os.path.dirname(path)
    tempDir = os.path.join(parentDir, 'tmp')
    logger.info('Extracting from ' + path + ' to ' + tempDir)
    patoolib.list_archive(path)
    subprocess.call('mkdir -p "%s"' % tempDir, shell=True)  # create temporary directory
    patoolib.extract_archive(path, outdir=tempDir)  # extract archive files to temporary directory
    results = read_from_directory(directory=tempDir, config=config)
    if outputPath:
        for imageTempPath, script in results.items():
            imagePath = path + '/' + _get_file_name(path=imageTempPath)
            write_to_csv(imagePath=imagePath, script=script, outputPath=outputPath)
    logger.info('Removing temporary directory: ' + tempDir)
    subprocess.call('rm -rf "%s"' % tempDir, shell=True)  # remove temporary directory
    return results


def _get_file_name(path):
    # from https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def read_from_directory(directory, outputPath=None, config=Config()):
    '''
    Read script from all image files in given directory recursively.
    '''
    logger.info('Reading from directory: ' + directory)
    results = {}
    for subDir, dirs, files in os.walk(directory):
        for file in files:
            fileName, fileExten = os.path.splitext(file)
            imagePath = os.path.join(subDir, file)
            if fileExten in IMAGE_EXTENSIONS:
                script = read_from_file(imagePath=imagePath, outputPath=outputPath, config=config)
                results[imagePath] = script
            elif fileExten in ARCHIVE_EXTENSIONS:
                archiveFileResults = read_from_archive_file(path=imagePath, outputPath=outputPath, config=config)
                results.update(archiveFileResults)
    return results


def _create_config_from_dict(configDict, defaultConfigSection=DEFAULT_CONFIG_SECTION):
    '''
    Create Config() object from dictionary.

    Parameters
    configDict: dict
        A dictionary of configurations specified in key-value pairs.
    defaultConfigSection: string
        The top-level config section that needs to be added on top of the configDict before feeding to configParser.read_dict(), default to 'sparksqlformatter'.
    
    Return: sparksqlformatter.src.config.Config() object
        The Config() object created from configDict.
    '''
    configParser = configparser.ConfigParser()
    configParser.optionxform = str  # makes the parser case-sensitive
    if defaultConfigSection not in configDict:
        configDict = {defaultConfigSection: configDict}  # add top-level section
    configParser.read_dict(configDict)  # configParser assumes the existence of a top-level section
    args = _parse_args_in_correct_type(configParser, defaultConfigSection)
    config = Config(**args)
    return config


def _parse_args_in_correct_type(configParser, defaultConfigSection=DEFAULT_CONFIG_SECTION):
    '''
    Parse paramters in config with special handling to convert boolean values converted from string back to boolean type.

    Parameters
    configParser: a configParser.ConfigParser() object
        Parser for config files.
    defaultConfigSection: string
        The top-level config section that needs to be added on top of the configDict before feeding to configParser.read_dict(), default to 'sparksqlformatter'.
    
    Return: dict
        A dictionary of configuration key-value pairs where values are of correct type.
    '''
    args = {}
    for key in configParser[defaultConfigSection]:
        args[key] = ast.literal_eval(configParser[defaultConfigSection][key])
    return args
