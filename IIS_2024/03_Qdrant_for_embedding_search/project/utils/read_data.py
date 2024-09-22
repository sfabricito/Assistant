import os
import pandas as pd
from ast import literal_eval
from dotenv import load_dotenv
from .system.logger import logger

load_dotenv()
log = logger()

FILE_NAME = os.getenv('FILE_NAME')

def read_data(rows, skip_rows=0):
    try:
        log.info(f'Reading rows from {skip_rows} to {skip_rows + rows}')
        csv_file_path = f'./data/{FILE_NAME}'
        
        article_df = pd.read_csv(csv_file_path, nrows=rows, skiprows=range(1, skip_rows+1))

        article_df['title_vector'] = article_df['title_vector'].apply(literal_eval)
        article_df['content_vector'] = article_df['content_vector'].apply(literal_eval)
        article_df['vector_id'] = article_df['vector_id'].apply(str)  
        return article_df
    except Exception as e:
        log.error(f'Exception while reading rows from {skip_rows} to {skip_rows + rows}. {e}')
