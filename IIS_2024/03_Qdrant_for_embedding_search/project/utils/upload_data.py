import os
from tqdm import tqdm
from dotenv import load_dotenv
from .system.logger import logger
from qdrant_client.models import PointStruct

load_dotenv()
log = logger()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def upload_data(qdrant, article_df):
    log.info(f'Upserting {len(article_df)} articles')
    for k, v in tqdm(article_df.iterrows(), desc="Upserting articles", total=len(article_df)):
        try:
            #log.info(f'Upserting article number {len(article_df.iterrows())}')
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=k,
                        vector={'title': v['title_vector'], 'content': v['content_vector']},
                        payload={
                            'id': v['id'],
                            'title': v['title'],
                            'url': v['url']
                        }
                    )
                ]
            )
        except Exception as e:
            log.error(f"Failed to upsert row {k}: {v}. Exception: {e}")