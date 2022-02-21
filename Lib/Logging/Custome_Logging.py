import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

DEFAULT_INPUT_PATH = './log/'
os.makedirs(DEFAULT_INPUT_PATH, exist_ok=True)

def Logger():
    """
    Logger Custome
    :return:
    """

    # print(str(DEFAULT_INPUT_PATH))

    logger = logging.getLogger()
    # ---
    # logger.setLevel(logging.WARN)
    logger.setLevel(logging.INFO)
    # ---

    # formatter = logging.Formatter('%(asctime)s |  %(filename)s | %(levelname)s | %(message)s')
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    Log_File_Size = 10 * 1024 * 1024
    # Log_File_Size = 1
    file_handler = RotatingFileHandler(str(DEFAULT_INPUT_PATH) + 'logs.log', mode='a', maxBytes=Log_File_Size, backupCount=10, encoding=None, delay=0)

    # file_handler = logging.FileHandler('logs.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger