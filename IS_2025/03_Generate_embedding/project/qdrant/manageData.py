from utils.logger import logger
from project.qdrant.readData import readData
from project.qdrant.uploadData import uploadData
import os
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()

log = logger()

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')

def manageData(qdrant, filename, synthetic_filename='./data/syntheticData/data.json'):
    try:
        log.info('Processing data for insert into Qdrant')

        # Read the main dataset
        data = readData(filename)

        # Load synthetic data if provided and convert it to DataFrame
        syntheticData = pd.DataFrame()  # Default to empty DataFrame
        if synthetic_filename:
            with open(synthetic_filename, 'r', encoding='utf-8') as f:
                synthetic_json = json.load(f)
                syntheticData = pd.DataFrame(synthetic_json)
                
                # Vectorize the 'text' column in syntheticData
                log.info('Vectorizing text column in synthetic data')
                model = SentenceTransformer(EMBEDDING_MODEL)  # Puedes cambiar por otro modelo si lo prefieres
                
                # Asegúrate de que la columna 'text' existe
                if 'text' in syntheticData.columns:
                    # Vectoriza todos los textos en la columna
                    texts = syntheticData['text'].tolist()
                    embeddings = model.encode(texts)
                    
                    # Añade la nueva columna con los vectores
                    syntheticData['text_vector'] = list(embeddings)
                    log.info('Text vectorization completed')
                else:
                    log.warning("Column 'text' not found in synthetic data")

        # Concatenate DataFrames
        combinedData = pd.concat([data, syntheticData], ignore_index=True)
        log.info('Data concatenation completed: ' + EMBEDDING_MODEL)
        #Upload to Qdrant
        uploadData(qdrant, combinedData)

        log.info('Data processed and uploaded to Qdrant')
    except Exception as e:
        log.error(f'An error has occurred while processing data: {e}')