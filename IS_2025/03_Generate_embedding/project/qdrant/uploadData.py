import os
from tqdm import tqdm
from dotenv import load_dotenv
from utils.logger import logger
from qdrant_client.models import PointStruct

load_dotenv()
log = logger()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')
BATCH_SIZE = int(os.getenv('BATCH_SIZE'))

def uploadData(qdrant, article_df):
    log.info(f'Upserting {len(article_df)} cases of terrorism')
    batch = []
    
    for k, v in tqdm(article_df.iterrows(), desc="Upserting articles", total=len(article_df)):
        log.info(k)
        try:
            point = PointStruct(
                id=k,
                vector={
                    'text': v['text_vector']
                },
                payload={
                    'id': v['id'],
                    'date': v['date'],
                    'location': v['location'],
                    'attack_type': v['attack_type'],
                    'target_type': v['target_type'],
                    'target': v['target'],
                    'orchestrating_group': v['orchestrating_group'],
                    'motive': v['motive'],
                    'weapon': v['weapon'],
                    'deceased': v['deceased'], 
                    'comments': v['comments'], 
                    'syntheticData': v.get('syntheticData', 'false'), 
                    'text': v['text']
                }
            )
            batch.append(point)
            
            if len(batch) == BATCH_SIZE:
                qdrant.upsert(collection_name=COLLECTION_NAME, points=batch)
                batch = []
            
        except Exception as e:
            log.error(f"Failed to upsert row {k}. Exception: {e}")
    if batch:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=batch)
    log.info(f'Inserted {len(article_df)} cases of terrorism')