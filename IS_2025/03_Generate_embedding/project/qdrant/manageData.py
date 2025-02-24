from utils.logger import logger
from project.qdrant.readData import readData
from project.qdrant.uploadData import uploadData

log = logger()

def manageData(qdrant, filename):
    try:
        log.info('Processing data for insert into Qdrant')

        data = readData(filename)
        uploadData(qdrant, data)

        log.info('Data processed and uploaded to Qdrant')
    except Exception as e:
        log.error(f'An error has occurred while processing data". {e}')