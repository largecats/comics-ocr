import sys
import os
import csv
import configparser
import ast

from comicsocr.src.config import Config, DEFAULT_CONFIG_SECTION
from comicsocr.src.tokenizer import Tokenizer
from comicsocr.src.reader import Reader


def read_from_file(imagePath, outputPath=None, config=Config()):
    if type(config) == type(Config()):  # config is a Config() object
        reader = Reader(config=config)
    else:  # create Config() object from config
        if type(config) == str:
            if config.startswith('{'):  # config is a dictionary in string
                config = eval(config)
                reader = Reader(config=_create_config_from_dict(config))
        elif type(config) == dict:  # config is a dictionary
            reader = Reader(config=_create_config_from_dict(config))
        else:
            raise Exception('Unsupported config type')
    script = reader.read(imagePath=imagePath)
    if outputPath:
        write_to_csv(imagePath=imagePath, script=script, outputPath=outputPath)
    else:
        return script


def write_to_csv(imagePath, script, outputPath):
    '''
    Write file path and extracted comic script to given output path.
    '''
    with open(outputPath, 'a', encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for line in script:
            newRow = [imagePath, line]
            writer.writerow(newRow)


def read_from_archive_file():
    pass


def read_from_folder(folderPath, outputPath=None, config=Config()):
    '''
    Read script from all image files in given folder recursively.
    '''
    results = {}
    for subDir, dirs, files in os.walk(folderPath):
        for file in files:
            fileInfo = file.split('.')
            fileName, fileExten = fileInfo[0], fileInfo[-1]
            imagePath = os.path.join(subDir, file)
            if fileExten in ['jpg', 'png', 'bmp']:
                script = read_from_file(imagePath=imagePath, config=config)
                results[imagePath] = script
            elif fileExten in ['rar', 'cbr', 'zip']:
                scripts = read_from_archive_file(imagePath=imagePath, config=config)
                for tarimagePath, script in scripts:
                    results[tarimagePath] = script
    if outputPath:
        for imagePath, script in results.items():
            write_to_csv(imagePath=imagePath, script=script, outputPath=outputPath)
    return imagePath


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
