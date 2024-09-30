import os
from tqdm import tqdm
from dotenv import load_dotenv
from .system.logger import logger
from qdrant_client.models import PointStruct

load_dotenv()
log = logger()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')
BATCH_SIZE = int(os.getenv('BATCH_SIZE'))

def upload_data(qdrant, article_df):
    log.info(f'Upserting {len(article_df)} cases of terrorism')
    batch = []
    
    for k, v in tqdm(article_df.iterrows(), desc="Upserting articles", total=len(article_df)):
        try:
            point = PointStruct(
                id=k,
                vector={
                    'location': v['location_vector'],
                    'attack_type': v['attack_type_vector'],
                    'target_type': v['target_type_vector'],
                    'corporation': v['corporation_vector'],
                    'target': v['target_vector'],
                    'orchestrating_group': v['orchestrating_group_vector'],
                    'weapon': v['weapon_vector'],
                    'notes': v['notes_vector'], 
                    'scite1': v['scite1_vector'], 
                    'scite2': v['scite2_vector'], 
                    'scite3': v['scite3_vector']
                },
                payload={
                    'id': v['id'],
                    'date': v['date'],
                    'location': v['location'],
                    'attack_type': v['attack_type'],
                    'target_type': v['target_type'],
                    'corporation': v['corporation'],
                    'target': v['target'],
                    'orchestrating_group': v['orchestrating_group'],
                    'weapon': v['weapon'],
                    'deceased': v['deceased'],
                    'notes': v['notes'], 
                    'scite1': v['scite1'], 
                    'scite2': v['scite2'], 
                    'scite3': v['scite3']
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