import os
import time
import qdrant_client 
from dotenv import load_dotenv
from utils.system.logger import logger
from utils.manage_data import manage_data
from utils.download_data import download_data
from utils.create_collection import create_collection

load_dotenv()
log = logger()

QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_PORT = os.getenv('QDRANT_PORT')

if __name__=="__main__":
    start_time = time.perf_counter()
    # download_data()
    
    log.info('Configuring Qdrant Client')
    qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    create_collection(qdrant)

    manage_data(qdrant)
    log.info(f'Program executed in {time.perf_counter() - start_time} seconds')