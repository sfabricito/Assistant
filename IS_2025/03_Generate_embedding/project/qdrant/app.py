import os
import time
import qdrant_client 
from dotenv import load_dotenv
from utils.logger import logger
from project.qdrant.manageData import manageData
from project.qdrant.createCollection import createCollection
from utils.tools.models import searchModel
from utils.tools.updateEnv import updateEnv

load_dotenv()
log = logger()

QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_PORT = os.getenv('QDRANT_PORT')

def main(distance, filename):
    log.info(f'Executing Program')
    start_time = time.perf_counter()

    model = searchModel(filename)
    updateEnv('EMBEDDING_MODEL', model['id'])
    updateEnv('DISTANCE', distance)

    log.info(f'Configuring Qdrant Client. Model: {model}')
    qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    createCollection(qdrant, distance,  model['vector_size'])

    manageData(qdrant, filename)
    # log.info(f'Program executed in {time.perf_counter() - start_time} seconds')

    # # print_query_results(query_qdrant(qdrant, "Black Nationalists", ['orchestrating_group'], 5))
    # # print_query_results(query_qdrant(qdrant, "Search for cases related with Dynamite and attacks to the government", ['weapon', 'target_type'], 5))
    # # print_query_results(query_qdrant(qdrant, "armed assault in a City in United States, like Chicago", ['attack_type', 'location'], 5))
    # print_query_results(query_qdrant(qdrant, "Soldier related with political Violence", ['notes', 'scite1', 'scite2', 'scite3'], 5))