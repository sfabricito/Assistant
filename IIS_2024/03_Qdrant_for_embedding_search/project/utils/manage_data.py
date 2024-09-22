import os
import sys
import time
from dotenv import load_dotenv
from .read_data import read_data
from .system.logger import logger
from .upload_data import upload_data

load_dotenv()
log = logger()

SLEEP_TIME = os.getenv('SLEEP_TIME')
SLEEP_TIME = int(SLEEP_TIME)
ROWS_CHUNK = os.getenv('ROWS_CHUNK')
ROWS_CHUNK = int(ROWS_CHUNK)
ROWS_TO_ITERATE = os.getenv('ROWS_TO_ITERATE')
ROWS_TO_ITERATE = int(ROWS_TO_ITERATE)

def manage_data(qdrant):
    try:
        log.info('Processing data')

        for i in range(0, ROWS_TO_ITERATE, ROWS_CHUNK):
            log.info(f'Processing data between rows {i} and {i + ROWS_CHUNK}')
            data = read_data(ROWS_CHUNK, i)
            upload_data(qdrant, data)
            time.sleep(SLEEP_TIME)

        log.info('Data processed')
    except Exception as e:
        log.error(f'An error has occurred while processing data". {e}')