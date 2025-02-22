import sys
import uuid
import logging
import os

def logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(str(uuid.uuid4()))
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('{time:%(asctime)s, level:%(levelname)s, message:"%(message)s"}')
    
    file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
    file_handler.setLevel(logging.INFO) 
    file_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    file_handler.setFormatter(formatter)
    
    error_file_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    
    # Stream handler only logs WARNING and above (no INFO messages in console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.WARNING)  # Change level to WARNING
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(stream_handler)
    
    return logger
