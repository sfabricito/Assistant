import sys
import uuid
import logging
import os

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.relative_path = os.path.relpath(record.pathname, start=os.getcwd())
        return super().format(record)

def logger():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(str(uuid.uuid4()))
    logger.setLevel(logging.DEBUG)
    
    formatter = CustomFormatter(
        '{time:%(asctime)s, level:%(levelname)s, file:"%(relative_path)s", line:%(lineno)d, message:"%(message)s"}'
    )
    
    file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
    file_handler.setLevel(logging.INFO)
    file_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    file_handler.setFormatter(formatter)
    
    error_file_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    
    stream_handler = logging.FileHandler(os.path.join(log_dir, "warning.log"))
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(stream_handler)
    
    return logger
