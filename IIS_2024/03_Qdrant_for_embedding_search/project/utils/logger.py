import sys
import logging

def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('{time:%(asctime)s, level:%(levelname)s, module:%(name)s, message:%(message)s}')
    
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.INFO) 
    file_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    file_handler.setFormatter(formatter)
    
    error_file_handler = logging.FileHandler("logs/error.log")
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(stream_handler)
    
    return logger