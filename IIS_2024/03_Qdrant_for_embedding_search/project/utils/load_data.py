from tqdm import tqdm
from qdrant_client.models import PointStruct

def load_data(qdrant, article_df):
    for k, v in tqdm(article_df.iterrows(), desc="Upserting articles", total=len(article_df)):
        try:
            qdrant.upsert(
                collection_name='Articles',
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
            print(f"Failed to upsert row {k}: {v}")
            print(f"Exception: {e}")