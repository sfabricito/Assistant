from .read_data import read_data
from .system.logger import logger
from .upload_data import upload_data

log = logger()

def manage_data(qdrant):
    try:
        log.info('Processing data')

        data = read_data()
        upload_data(qdrant, data)

        log.info('Data processed')
    except Exception as e:
        log.error(f'An error has occurred while processing data". {e}')