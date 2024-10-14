import os
import time
import qdrant_client 
from dotenv import load_dotenv
from utils.system.logger import logger
from utils.manage_data import manage_data
from utils.query import query_qdrant, print_query_results
from utils.create_collection import create_collection

load_dotenv()
log = logger()

QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_PORT = os.getenv('QDRANT_PORT')

if __name__=="__main__":
    log.info(f'Executing Program')
    start_time = time.perf_counter()

    log.info('Configuring Qdrant Client')
    qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    # create_collection(qdrant)

    #manage_data(qdrant)
    log.info(f'Program executed in {time.perf_counter() - start_time} seconds')

    # print_query_results(query_qdrant(qdrant, "Black Nationalists", ['orchestrating_group'], 5))
    # print_query_results(query_qdrant(qdrant, "Search for cases related with Dynamite and attacks to the government", ['weapon', 'target_type'], 5))
    # print_query_results(query_qdrant(qdrant, "armed assault in a City in United States, like Chicago", ['attack_type', 'location'], 5))
    print_query_results(query_qdrant(qdrant, "Soldier related with political Violence", ['notes', 'scite1', 'scite2', 'scite3'], 5))