import os
import zipfile
import requests
from dotenv import load_dotenv
from .system.logger import logger

load_dotenv()
log = logger()

FILE_URL = os.getenv('FILE_URL')
ZIP_NAME = os.getenv('ZIP_NAME')

def download_data():
    try:
        log.error(f'Downloading and unzipping file "{ZIP_NAME}".')
        response = requests.get(FILE_URL, verify=True)
        with open(ZIP_NAME, 'wb') as file:
            file.write(response.content)

        with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
            zip_ref.extractall("../data")
        log.info(f'File "{ZIP_NAME}" downloaded and unzipped correctly.')
    except Exception as e:
        log.error(f'An error has occurred while downloading and unzipping file "{ZIP_NAME}". {e}')